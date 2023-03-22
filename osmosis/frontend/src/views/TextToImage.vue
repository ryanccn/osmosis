<script setup lang="ts">
// import { ref } from "vue";
import { useOsmosisStore } from "@/lib/store";
import { multiplesOf64, schedulers } from "@/lib/utils";

import { onKeyStroke } from "@vueuse/core";

import GalleryView from "@/components/GalleryView.vue";
import CurrentImageView from "@/components/CurrentImageView.vue";
import Switch from "@/components/Switch.vue";

const store = useOsmosisStore();

const generate = () => {
  store.txt2img();
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
          v-model="store.txt2imgParameters.prompt"
        ></textarea>
      </label>
      <label class="flex flex-col gap-y-2">
        <span class="text-sm font-semibold">Negative prompt</span>
        <textarea
          class="osmosis form input text-sm min-h-[5rem] resize-none"
          v-model="store.txt2imgParameters.negativePrompt"
        ></textarea>
      </label>

      <button
        class="osmosis primary button my-4"
        @click="generate"
        v-if="!store.txt2imgProgress?.type"
        :disabled="!store.model || !store.txt2imgParameters.prompt.length"
      >
        Generate
      </button>
      <button class="osmosis danger button my-4" @click="stopGenerate" v-else>
        Stop
      </button>

      <div class="grid grid-cols-2 gap-x-6 gap-y-5 mb-4">
        <div class="flex flex-col gap-y-2 w-full">
          <h2 class="text-sm font-semibold">Width</h2>

          <select
            class="osmosis form input"
            v-model="store.txt2imgParameters.width"
          >
            <option :key="size" :value="size" v-for="size in multiplesOf64">
              {{ size }}
            </option>
          </select>
        </div>

        <div class="flex flex-col gap-y-2 w-full">
          <h2 class="text-sm font-semibold">Height</h2>

          <select
            class="osmosis form input"
            v-model="store.txt2imgParameters.height"
          >
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
              v-model.number="store.txt2imgParameters.steps"
              class="grow"
            />
            <span class="text-sm">{{ store.txt2imgParameters.steps }}</span>
          </div>
        </div>

        <div class="flex flex-col gap-y-2">
          <span class="text-sm font-semibold">Scheduler</span>
          <select
            class="osmosis form input"
            v-model="store.txt2imgParameters.scheduler"
          >
            <option v-for="(value, key) in schedulers" :key="key" :value="key">
              {{ value }}
            </option>
          </select>
        </div>
      </div>

      <div class="flex flex-col gap-y-3">
        <div class="flex flex-row items-center justify-between">
          <span class="text-sm font-semibold">Seed</span>
          <label class="flex flex-row gap-x-1 items-center self-end">
            <Switch v-model="store.txt2imgParameters.seedRandom" />
            <span class="font-medium text-sm">Random</span>
          </label>
        </div>
        <input
          type="number"
          class="osmosis form input"
          min="0"
          v-model="store.txt2imgParameters.seed"
          :disabled="store.txt2imgParameters.seedRandom"
        />
      </div>

      <div class="flex flex-col gap-y-2">
        <h2 class="flex flex-row items-center gap-x-2">
          <Switch v-model="store.txt2imgParameters.upscale" />
          <span class="text-lg font-semibold">Upscale</span>
        </h2>

        <select
          class="osmosis form input"
          v-model.number="store.txt2imgParameters.upscaleScale"
          :disabled="!store.txt2imgParameters.upscale"
        >
          <option value="2">2x</option>
          <option value="4">4x</option>
        </select>
      </div>

      <div class="flex flex-col gap-y-2">
        <h2 class="flex flex-row items-center gap-x-2">
          <Switch v-model="store.txt2imgParameters.faceRestoration" />
          <span class="text-lg font-semibold">Face restoration</span>
        </h2>
      </div>
    </div>

    <CurrentImageView />
    <GalleryView />
  </div>
</template>
