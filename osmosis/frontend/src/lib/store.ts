import { defineStore } from "pinia";
import { ws } from "./ws";

export const useOsmosisStore = defineStore("osmosis", {
  state: () => {
    return {
      connected: false,
      model: null as null | { type: "diffusers" | "coreml"; name: string },
      availableModels: {} as {
        [internalId: string]: { type: "diffusers" | "coreml"; id: string };
      },
      progress: {
        type: null as "determinate" | "indeterminate" | null,
        task: "",
        data: [0, 0],
      },
      gallery: [] as string[],
      gallerySelected: null as string | null,
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

    addModel(type: "diffusers" | "coreml", id: string) {
      return new Promise<void>((resolve) => {
        ws.emit("add_model", { model_type: type, model_id: id }, () => {
          resolve();
        });
      });
    },

    txt2img(
      prompt: string,
      negativePrompt: string,
      seed: number,
      upscale: { model: string; scale: number } | null
    ) {
      return new Promise<void>((resolve) => {
        ws.emit("txt2img", {
          prompt,
          negative_prompt: negativePrompt || null,
          seed,
          upscale,
        });

        this.progress.type = "indeterminate";
        this.progress.task = "txt2img";

        ws.once("txt2img:done", async () => {
          this.progress.type = null;
          this.progress.task = "";
          await this.refreshGallery();
          this.gallerySelected = this.gallery[0];
          resolve();
        });
      });
    },

    refreshGallery() {
      return new Promise<void>((resolve) => {
        ws.emit("gallery", ({ files }: { files: string[] }) => {
          this.gallery = files;
          resolve();
        });
      });
    },
  },
});

export const setupStoreListeners = () => {
  ws.on("connect", () => {
    ws.emit(
      "info",
      async ({
        model,
        models,
      }: {
        model: { type: "diffusers" | "coreml"; name: string };
        models: any;
      }) => {
        const store = useOsmosisStore();

        store.model =
          model.type === null ? null : { type: model.type, name: model.name };
        store.availableModels = models;

        await store.refreshGallery();
        store.gallerySelected = store.gallery[0];

        store.connected = true;
      }
    );
  });

  ws.on("disconnect", () => {
    useOsmosisStore().connected = false;
  });

  ws.on("progress", ([now, full]: [number, number]) => {
    useOsmosisStore().progress.type = "determinate";
    useOsmosisStore().progress.data = [now, full];
  });
};
