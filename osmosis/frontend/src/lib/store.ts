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

        ws.emit("load_model", internalId, () => {
          const internalRepresentation = this.availableModels[internalId];
          this.model = {
            name: internalRepresentation.id,
            type: internalRepresentation.type,
          };

          this.progress.type = null;
          this.progress.task = "";
          resolve();
        });
      });
    },

    addModel(
      data:
        | { type: "diffusers"; id: string; revision?: string; half: boolean }
        | { type: "coreml"; id: string; mlpackages: string }
    ) {
      return new Promise<void>((resolve) => {
        ws.emit(
          "add_model",
          {
            model_type: data.type,
            model_id: data.id,
            ...(data.type === "coreml"
              ? { mlpackages_dir: data.mlpackages }
              : { revision: data.revision || null, half: data.half }),
          },
          () => {
            this.refreshInfo();
            resolve();
          }
        );
      });
    },

    refreshInfo() {
      ws.emit(
        "info",
        async ({
          model,
          models,
          coreml_available,
        }: {
          model: { type: "diffusers" | "coreml"; name: string };
          models: any;
          coreml_available: boolean;
        }) => {
          const store = useOsmosisStore();

          store.model =
            model.type === null ? null : { type: model.type, name: model.name };
          store.availableModels = models;

          store.coreMLAvailable = coreml_available;

          await store.refreshGallery();
          if (!store.gallerySelected) {
            store.gallerySelected = store.gallery[0];
            store.gallerySelectedMetadata = await this.getImageMetadata(
              store.gallerySelected
            );
          }

          store.connected = true;
        }
      );
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

    txt2img({
      prompt,
      negativePrompt,
      width,
      height,
      steps,
      scheduler,
      seed,
      upscale,
      faceRestoration,
    }: {
      prompt: string;
      negativePrompt: string;
      width: number;
      height: number;
      steps: number;
      scheduler: string;
      seed: number;
      upscale: number | null;
      faceRestoration: number | null;
    }) {
      return new Promise<void>((resolve) => {
        ws.emit("txt2img", {
          prompt,
          negative_prompt: negativePrompt || null,
          width,
          height,
          steps,
          seed,
          scheduler,

          upscale,
          face_restoration: faceRestoration,
        });

        this.progress.type = "indeterminate";
        this.progress.task = "txt2img";

        ws.once("txt2img:done", async () => {
          this.progress.type = null;
          this.progress.task = "";
          this.progress.image = null;
          await this.refreshGallery();
          this.gallerySelected = this.gallery[0];
          resolve();
        });
      });
    },

    deleteGalleryImage(name: string) {
      return new Promise<void>((resolve) =>
        ws.emit("gallery:delete", name, () => {
          this.refreshGallery();
          this.gallerySelected = this.gallery[0];
          resolve();
        })
      );
    },

    refreshGallery() {
      return new Promise<void>((resolve) => {
        ws.emit("gallery", ({ files }: { files: string[] }) => {
          this.gallery = files;
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
