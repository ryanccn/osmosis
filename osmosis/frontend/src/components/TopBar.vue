<script setup lang="ts">
import { ref } from "vue";
import { useOsmosisStore } from "@/lib/store";
import LoadModel from "@/components/LoadModel.vue";

const store = useOsmosisStore();
const loadModelIsOpen = ref(false);
</script>

<template>
  <div
    class="flex items-center justify-between px-6 py-3 border-b-2 border-surface shrink-0 h-osmosis-top-bar"
  >
    <div class="flex gap-x-6 items-center">
      <h1 class="font-extrabold text-2xl tracking-tight mr-4">Osmosis</h1>
      <RouterLink
        class="text-sm font-medium hover:text-accent transition-all"
        to="/txt2img"
        active-class="text-accent"
      >
        Text to image
      </RouterLink>
      <span class="text-sm font-medium opacity-50 select-none">
        Image to image
      </span>
      <span class="text-sm font-medium opacity-50 select-none">Training</span>
      <span class="text-sm font-medium opacity-50 select-none">
        Convert models
      </span>
    </div>

    <button
      class="bg-surface hover:bg-surface-hover transition px-4 py-2 font-medium text-sm rounded focus:outline-none focus:ring focus:ring-accent/50"
      @click="loadModelIsOpen = true"
    >
      {{ store.model ? store.model.name : "No model loaded" }}
    </button>
  </div>

  <LoadModel :isOpen="loadModelIsOpen" @close="loadModelIsOpen = false" />
</template>
