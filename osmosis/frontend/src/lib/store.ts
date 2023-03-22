import { defineStore } from "pinia";
import type { RawStableDiffusionMetadata } from "./types";
import { ws } from "./ws";

export const useOsmosisStore = defineStore("osmosis", {
  state: () => {
    return {
      connected: false,
      model: null as null | { type: "diffusers" | "coreml"; name: string },
      availableModels: {} as {
        [internalId: string]: {
          type: "diffusers" | "coreml";
          id: string;
          displayName?: string;
          revision?: string;
          half?: boolean;
        };
      },
      coreMLAvailable: false,
      progress: {
        type: null as "determinate" | "indeterminate" | null,
        task: "",
        data: [0, 0],
        image: null as string | null,
      },
      gallery: [] as string[],
      gallerySelected: null as string | null,
      gallerySelectedMetadata: null as RawStableDiffusionMetadata | null,
      txt2imgParameters: {
        prompt: "",
        negativePrompt: "",

        width: 512,
        height: 512,

        steps: 40,
        scheduler: "LMSDiscrete",
        seed: 0,
        seedRandom: true,

        upscale: false as false,
        upscaleScale: 2,

        faceRestoration: false,
      },
    };
  },

  getters: {
    loadModelProgress: (state) => {
      if (!state.progress.type) return null;
      if (state.progress.task !== "load_model") return null;

      return state.progress;
    },
    txt2imgProgress: (state) => {
      if (!state.progress.type) return null;
      if (state.progress.task !== "txt2img") return null;

      return state.progress;
    },
  },

  actions: {
    loadModel(internalId: string) {
      return new Promise<void>((resolve) => {
        this.progress.type = "indeterminate";
        this.progress.task = "load_model";

        ws.emit("load_model", internalId, async () => {
          await this.refreshInfo();

          this.progress.type = null;
          this.progress.task = "";
          resolve();
        });
      });
    },

    addModel(
      data:
        | { type: "diffusers"; id: string; revision?: string; half: boolean }
        | { type: "coreml"; path: string; mlpackages: string }
        | { type: "checkpoint"; path: string; half: boolean }
    ) {
      return new Promise<void>((resolve) => {
        const callback = () => {
          this.refreshInfo();
          resolve();
        };

        if (data.type === "diffusers") {
          ws.emit(
            "add_model",
            {
              model_type: data.type,
              model_id: data.id,

              revision: data.revision || null,
              half: data.half,
            },
            callback
          );
        } else if (data.type === "coreml") {
          ws.emit(
            "add_model",
            {
              model_type: data.type,
              path: data.path,
              mlpackages: data.mlpackages,
            },
            callback
          );
        } else if (data.type === "checkpoint") {
          ws.emit(
            "add_model",
            {
              model_type: data.type,
              path: data.path,
              half: data.half,
            },
            callback
          );
        }
      });
    },

    refreshInfo() {
      return new Promise<void>((resolve) => {
        ws.emit(
          "info",
          async ({
            model,
            models,
            coreml_available,
          }: {
            model: { type: "diffusers" | "coreml"; name: string };
            models: {
              [internalId: string]: {
                type: "diffusers" | "coreml";
                id: string;
                displayName: string;
              };
            };
            coreml_available: boolean;
          }) => {
            this.model =
              model.type === null
                ? null
                : { type: model.type, name: model.name };
            this.availableModels = models;

            this.coreMLAvailable = coreml_available;

            await this.refreshGallery();
            if (!this.gallerySelected) {
              this.gallerySelected = this.gallery[0];
              this.gallerySelectedMetadata = await this.getImageMetadata(
                this.gallerySelected
              );
            }

            this.connected = true;
            resolve();
          }
        );
      });
    },

    getImageMetadata(name: string) {
      return new Promise<RawStableDiffusionMetadata>((resolve) =>
        ws.emit(
          "gallery:metadata",
          name,
          (data: RawStableDiffusionMetadata) => {
            resolve(data);
          }
        )
      );
    },

    txt2img() {
      return new Promise<void>((resolve) => {
        ws.emit("txt2img", {
          prompt: this.txt2imgParameters.prompt,
          negative_prompt: this.txt2imgParameters.negativePrompt || null,
          width: this.txt2imgParameters.width,
          height: this.txt2imgParameters.height,
          steps: this.txt2imgParameters.steps,
          seed: this.txt2imgParameters.seedRandom
            ? -1
            : this.txt2imgParameters.seed,
          scheduler: this.txt2imgParameters.scheduler,

          upscale: this.txt2imgParameters.upscale
            ? this.txt2imgParameters.upscaleScale
            : null,
          face_restoration: this.txt2imgParameters.faceRestoration,
        });

        this.progress.type = "indeterminate";
        this.progress.task = "txt2img";

        ws.once("txt2img:done", async () => {
          this.progress.type = null;
          this.progress.task = "";
          this.progress.image = null;
          await this.refreshGallery();
          await this.setGallerySelected(this.gallery[0]);
          resolve();
        });
      });
    },

    deleteGalleryImage(name: string) {
      return new Promise<void>((resolve) =>
        ws.emit("gallery:delete", name, async () => {
          this.refreshGallery();
          await this.setGallerySelected(this.gallery[0]);
          resolve();
        })
      );
    },

    async setGallerySelected(name: string) {
      if (!this.gallery.includes(name)) return;
      this.gallerySelected = name;
      this.gallerySelectedMetadata = await this.getImageMetadata(
        this.gallerySelected
      );
    },

    refreshGallery() {
      return new Promise<void>((resolve) => {
        ws.emit("gallery", async ({ files }: { files: string[] }) => {
          this.gallery = files;
          if (
            !this.gallerySelected ||
            !this.gallery.includes(this.gallerySelected)
          ) {
            await this.setGallerySelected(this.gallery[0]);
          }
          resolve();
        });
      });
    },

    halt() {
      ws.emit("stop");
    },
  },
});

export const setupStoreListeners = () => {
  ws.on("connect", () => {
    useOsmosisStore().refreshInfo();
  });

  ws.on("disconnect", () => {
    useOsmosisStore().connected = false;
  });

  ws.on(
    "txt2img:progress",
    ({
      type,
      data,
      image,
    }: {
      type: string;
      data: [number, number];
      image: string;
    }) => {
      if (type === "main") {
        useOsmosisStore().progress.type = "determinate";
        useOsmosisStore().progress.data = data;
        useOsmosisStore().progress.image = image;
      } else if (type === "postprocessing") {
        useOsmosisStore().progress.type = "indeterminate";
      }
    }
  );
};
