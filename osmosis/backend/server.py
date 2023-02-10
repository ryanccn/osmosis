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

        self.model = OsmosisModel()

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
            return {
                "model": {"type": self.model.type, "name": self.model.name},
                "models": load_models(),
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

            print(f"Loaded model {model_internal_id}")

        @self.sio.on("add_model")
        def add_model(data):
            model_type = "diffusers"

            new_internal_id = uuid4().hex[:10]

            if model_type == "diffusers":
                model_id = data["model_id"]

                prev_models = load_models()
                prev_models[new_internal_id] = {"type": "diffusers", "id": model_id}
                save_models(prev_models)

        @self.sio.on("txt2img")
        def txt2img(data):
            output = self.model.txt2img(data, sio=self.sio)

            file_name = save_image(output["image"], output["metadata"])

            self.sio.emit("txt2img:done", file_name)
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
