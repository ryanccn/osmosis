<script setup lang="ts">
import { ref } from "vue";
import { useOsmosisStore } from "@/lib/store";
import { multiplesOf64, schedulers } from "@/lib/utils";

import { onKeyStroke } from "@vueuse/core";
import GalleryView from "@/components/GalleryView.vue";
import Switch from "@/components/Switch.vue";

const store = useOsmosisStore();

const prompt = ref("");
const negativePrompt = ref("");

const width = ref(512);
const height = ref(512);

const steps = ref(40);
const scheduler = ref("LMSDiscrete");
const seed = ref(0);
const seedRandom = ref(true);

const upscale = ref(false);
const upscaleScale = ref(2);

const faceRestoration = ref(false);

const generate = () => {
  store.txt2img({
    prompt: prompt.value,
    negativePrompt: negativePrompt.value,
    width: width.value,
    height: height.value,
    steps: steps.value,
    scheduler: scheduler.value,
    seed: seedRandom.value ? -1 : seed.value,
    upscale: upscale.value ? upscaleScale.value : null,
    faceRestoration: faceRestoration.value ? 0.5 : null,
  });
};

const stopGenerate = () => {
  store.halt();
};

onKeyStroke("Enter", (e) => {
  if (e.metaKey) {
    e.preventDefault();
    generate();
  }
});
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-[1fr_2fr_1fr] h-osmosis-content">
    <div
      class="border-surface border-r-2 flex flex-col gap-y-6 p-5 h-osmosis-content overflow-y-scroll"
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
          v-model="negativePrompt"
        ></textarea>
      </label>

      <button
        class="osmosis primary button my-4"
        @click="generate"
        v-if="!store.txt2imgProgress?.type"
        :disabled="!store.model || !prompt.length"
      >
        Generate
      </button>
      <button class="osmosis danger button my-4" @click="stopGenerate" v-else>
        Stop
      </button>

      <div class="grid grid-cols-2 gap-x-6 gap-y-5 mb-4">
        <div class="flex flex-col gap-y-2 w-full">
          <h2 class="text-sm font-semibold">Width</h2>

          <select class="osmosis form input" v-model="width">
            <option :key="size" :value="size" v-for="size in multiplesOf64">
              {{ size }}
            </option>
          </select>
        </div>

        <div class="flex flex-col gap-y-2 w-full">
          <h2 class="text-sm font-semibold">Height</h2>

          <select class="osmosis form input" v-model="height">
            <option :key="size" :value="size" v-for="size in multiplesOf64">
              {{ size }}
            </option>
          </select>
        </div>

        <div class="flex flex-col gap-y-2">
          <span class="text-sm font-semibold">Steps</span>
          <div
            class="flex flex-row gap-x-2 items-center w-full align-middle grow"
          >
            <input
              type="range"
              min="1"
              max="100"
              v-model.number="steps"
              class="grow"
            />
            <span class="text-sm">{{ steps }}</span>
          </div>
        </div>

        <div class="flex flex-col gap-y-2">
          <span class="text-sm font-semibold">Scheduler</span>
          <select class="osmosis form input" v-model="scheduler">
            <option v-for="s in schedulers" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>
      </div>

      <div class="flex flex-col gap-y-3">
        <div class="flex flex-row items-center justify-between">
          <span class="text-sm font-semibold">Seed</span>
          <label class="flex flex-row gap-x-1 items-center self-end">
            <Switch v-model="seedRandom" />
            <span class="font-medium text-sm">Random</span>
          </label>
        </div>
        <input
          type="number"
          class="osmosis form input"
          min="0"
          v-model="seed"
          :disabled="seedRandom"
        />
      </div>

      <div class="flex flex-col gap-y-2">
        <h2 class="flex flex-row items-center gap-x-2">
          <Switch v-model="upscale" />
          <span class="text-lg font-semibold">Upscale</span>
        </h2>

        <select
          class="osmosis form input"
          v-model.number="upscaleScale"
          :disabled="!upscale"
        >
          <option value="2">2x</option>
          <option value="4">4x</option>
        </select>
      </div>

      <div class="flex flex-col gap-y-2">
        <h2 class="flex flex-row items-center gap-x-2">
          <Switch v-model="faceRestoration" />
          <span class="text-lg font-semibold">Face restoration</span>
        </h2>
      </div>
    </div>

    <div class="flex items-center w-full h-osmosis-content p-2 bg-surface">
      <div class="flex flex-row gap-x-3"></div>

      <img
        :src="store.progress.image"
        class="block rounded-lg object-contain max-w-full max-h-full mx-auto"
        v-if="store.progress.image"
      />
      <img
        :src="`/outputs/${store.gallerySelected}`"
        class="block rounded-lg object-contain max-w-full max-h-full mx-auto"
        v-else-if="store.gallerySelected"
      />
    </div>

    <GalleryView />
  </div>
</template>
