from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import eventlet

from ..frontend import dist as frontend

from .model import OsmosisModel
from .config import Config
from .fs import save_image, load_models, save_models

import diffusers

from uuid import uuid4
import os
import platform
import packaging.version as semver


class OsmosisServer:
    app: Flask
    sio: SocketIO

    port: int

    model: OsmosisModel

    def __init__(self, port: int):
        self.port = port
        self.app = Flask(
            __name__, static_url_path="", static_folder=frontend.__path__[0]
        )
        self.sio = SocketIO(self.app)

        self.model = OsmosisModel(sio=self.sio)

        diffusers.logging.set_verbosity_warning()

        self.register_routes()
        self.register_ws_handlers()

    def register_routes(self):
        @self.app.route("/")
        def serve_index():
            return send_from_directory(self.app.static_folder, "index.html")

        @self.app.route("/outputs/<path:name>")
        def serve_outputs(name):
            return send_from_directory(Config.OUTPUTS_DIR, name)

    def register_ws_handlers(self):
        @self.sio.on("info")
        def info():
            coreml_available = False
            if platform.system() == "Darwin":
                macos_version = semver.parse(platform.mac_ver()[0])
                coreml_available = macos_version >= semver.parse("13.1")

            return {
                "model": {"type": self.model.type, "name": self.model.name},
                "models": load_models(),
                "coreml_available": platform.system() == "Darwin"
                and platform.mac_ver(),
            }

        @self.sio.on("load_model")
        def load_model(model_internal_id):
            print(f"Loading model {model_internal_id}")

            models = load_models()
            model = models.get(model_internal_id, None)

            if not model:
                print(f"Unknown model {model_internal_id}")
                return

            if model["type"] == "diffusers":
                self.model.load_diffusers(model["id"])
            elif model["type"] == "coreml":
                self.model.load_coreml(model["id"], model["mlpackages"])

            print(f"Loaded model {model_internal_id}")

        @self.sio.on("add_model")
        def add_model(data: dict):
            model_type = data.get("model_type", "diffusers")

            new_internal_id = uuid4().hex

            if model_type == "diffusers":
                model_id = data["model_id"]

                prev_models = load_models()
                prev_models[new_internal_id] = {"type": "diffusers", "id": model_id}
                save_models(prev_models)
            elif model_type == "coreml":
                model_id = data["model_id"]
                mlpackages_dir = data["mlpackages_dir"]

                prev_models = load_models()
                prev_models[new_internal_id] = {
                    "type": "coreml",
                    "id": model_id,
                    "mlpackages": mlpackages_dir,
                }
                save_models(prev_models)
            else:
                raise NotImplementedError()

        @self.sio.on("txt2img")
        def txt2img(data):
            print(data)
            output = self.model.txt2img(data)

            if output:
                save_image(output["image"], output["metadata"])

            self.sio.emit("txt2img:done")
            eventlet.sleep(0)

        @self.sio.on("gallery")
        def gallery():
            files = [
                name for name in os.listdir(Config.OUTPUTS_DIR) if name.endswith(".png")
            ]

            files.sort(
                key=lambda x: os.path.getmtime(os.path.join(Config.OUTPUTS_DIR, x))
            )
            files.reverse()

            return {"files": files}

    def start(self):
        print(f"Server started on http://localhost:{self.port}/")
        self.sio.run(self.app, port=self.port, debug=os.environ.get("DEBUG") == "1")
