<script setup lang="ts">
import { useOsmosisStore } from "@/lib/store";

const store = useOsmosisStore();
</script>

<template>
  <div
    class="fixed top-0 max-w-[100vw] overflow-hidden z-[60] h-1 block bg-accent shadow-md shadow-accent/50 transition-all"
    :style="{
      width: `${(store.progress.data[0] / store.progress.data[1]) * 100}%`,
    }"
    v-if="store.progress.type === 'determinate'"
  />
  <div
    class="fixed top-0 max-w-[100vw] overflow-hidden z-[60] h-1 block bg-accent shadow-md shadow-accent/50 w-[25%] animate-progress-indeterminate"
    v-if="store.progress.type === 'indeterminate'"
  />
</template>

<style>
.animate-progress-indeterminate {
  animation: progress-indeterminate 1s infinite ease-in-out;
}

@keyframes progress-indeterminate {
  from {
    transform: translateX(-100%);
  }

  to {
    transform: translateX(100vw);
  }
}
</style>
