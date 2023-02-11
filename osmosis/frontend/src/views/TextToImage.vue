<script setup lang="ts">
import { ref } from "vue";
import { useOsmosisStore } from "@/lib/store";

import GalleryView from "@/components/GalleryView.vue";

const store = useOsmosisStore();

const prompt = ref("");
const negativePrompt = ref("");
const seed = ref(-1);

const upscale = ref(false);
const upscaleScale = ref(2);

const faceRestoration = ref(false);

const generate = () => {
  store.txt2img(
    prompt.value,
    negativePrompt.value,
    seed.value,
    upscale.value ? upscaleScale.value : null,
    faceRestoration.value ? 0.5 : null
  );
};

const stopGenerate = () => {
  console.warn("ASDF THIS ISN'T IMPLEMENTED YET AAAAAAA");
};
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-[1fr_2fr_1fr] grow overflow-hidden">
    <div
      class="border-surface border-r-2 flex flex-col gap-y-4 p-5 overflow-y-scroll"
    >
      <label class="flex flex-col gap-y-2">
        <span class="text-sm font-semibold">Prompt</span>
        <textarea
          class="osmosis form input text-sm min-h-[10rem] resize-none"
          v-model="prompt"
        ></textarea>
      </label>
      <label class="flex flex-col gap-y-2">
        <span class="text-sm font-semibold">Negative prompt</span>
        <textarea
          class="osmosis form input text-sm min-h-[5rem] resize-none"
        ></textarea>
      </label>

      <label class="flex flex-col gap-y-2">
        <span class="text-sm font-semibold">Seed</span>
        <input
          type="number"
          class="osmosis form input"
          placeholder="Random"
          min="-1"
        />
      </label>

      <div class="flex flex-col gap-y-2">
        <h2 class="flex flex-row items-center gap-x-2">
          <input type="checkbox" v-model="upscale" class="p-2" />
          <span class="text-lg font-semibold">Upscale</span>
        </h2>

        <select
          class="osmosis form input"
          v-model="upscaleScale"
          :disabled="!upscale"
        >
          <option value="2">2x</option>
          <option value="4">4x</option>
        </select>
      </div>

      <div class="flex flex-col gap-y-2">
        <h2 class="flex flex-row items-center gap-x-2">
          <input type="checkbox" v-model="faceRestoration" class="p-2" />
          <span class="text-lg font-semibold">Face restoration</span>
        </h2>
      </div>

      <button
        class="osmosis primary button mt-4"
        @click="generate"
        v-if="!store.txt2imgProgress?.type"
        :disabled="!store.model"
      >
        Generate
      </button>
      <button class="osmosis danger button mt-4" @click="stopGenerate" v-else>
        Stop
      </button>
    </div>

    <div class="grid place-content-center">
      <img
        v-if="store.gallerySelected"
        :src="`/outputs/${store.gallerySelected}`"
        class="block"
      />
      <span v-else>Generate an image!</span>
    </div>

    <GalleryView />
  </div>
</template>
