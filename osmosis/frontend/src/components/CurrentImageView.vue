<script setup lang="ts">
import { useOsmosisStore } from "@/lib/store";
import { ref } from "vue";
import { InfoIcon, TrashIcon, ClipboardCopyIcon } from "lucide-vue-next";

const store = useOsmosisStore();

const showingMetadata = ref(false);

const copyParameters = () => {
  if (!store.gallerySelectedMetadata) return;

  store.txt2imgParameters.prompt = store.gallerySelectedMetadata.image.prompt;
  store.txt2imgParameters.width = store.gallerySelectedMetadata.image.width;
  store.txt2imgParameters.height = store.gallerySelectedMetadata.image.height;
  store.txt2imgParameters.scheduler =
    store.gallerySelectedMetadata.image.sampler;
  store.txt2imgParameters.seed = store.gallerySelectedMetadata.image.seed;
  store.txt2imgParameters.seedRandom = false;
  store.txt2imgParameters.steps = store.gallerySelectedMetadata.image.steps;
};
</script>

<template>
  <div class="flex flex-col gap-y-6 w-full h-osmosis-content p-10 bg-surface">
    <div class="flex flex-row gap-x-3 justify-center">
      <button
        class="osmosis primary button"
        @click="showingMetadata = !showingMetadata"
        :disabled="!store.gallerySelected"
      >
        <InfoIcon class="block w-4 h-4" />
        <span>Metadata</span>
      </button>
      <button
        class="osmosis primary button"
        @click="copyParameters"
        :disabled="!store.gallerySelected"
      >
        <ClipboardCopyIcon class="block w-4 h-4" />
        <span>Use parameters</span>
      </button>
      <button
        class="osmosis danger button"
        @click="store.deleteGalleryImage(store.gallerySelected!)"
        :disabled="!store.gallerySelected"
      >
        <TrashIcon class="block w-4 h-4" />
        <span>Delete</span>
      </button>
    </div>

    <div class="relative flex items-center justify-center w-full h-full">
      <img
        :src="store.progress.image"
        class="object-contain w-auto max-w-full max-h-full absolute block rounded-lg"
        v-if="store.progress.image"
      />
      <img
        :src="`/outputs/${store.gallerySelected}`"
        class="object-contain w-auto max-w-full max-h-full absolute block rounded-lg"
        v-else-if="store.gallerySelected"
      />

      <div
        v-if="showingMetadata && store.gallerySelectedMetadata"
        class="absolute inset-0 bg-black/50 backdrop-blur-lg text-white p-10 flex flex-col gap-y-2 overflow-y-scroll"
      >
        <p>
          <span class="font-semibold">Model:</span>
          {{ store.gallerySelectedMetadata.model_weights }}
        </p>
        <p>
          <span class="font-semibold">Prompt:</span>
          {{ store.gallerySelectedMetadata.image.prompt }}
        </p>
        <p>
          <span class="font-semibold">Width:</span>
          {{ store.gallerySelectedMetadata.image.width }}
        </p>
        <p>
          <span class="font-semibold">Height:</span>
          {{ store.gallerySelectedMetadata.image.height }}
        </p>
        <p>
          <span class="font-semibold">Steps:</span>
          {{ store.gallerySelectedMetadata.image.steps }}
        </p>
        <p>
          <span class="font-semibold">Sampler:</span>
          {{ store.gallerySelectedMetadata.image.sampler }}
        </p>
        <p>
          <span class="font-semibold">Seed:</span>
          {{ store.gallerySelectedMetadata.image.seed }}
        </p>
        <p>
          <span class="font-semibold">CFG scale:</span>
          {{ store.gallerySelectedMetadata.image.cfg_scale }}
        </p>
      </div>
    </div>
  </div>
</template>
