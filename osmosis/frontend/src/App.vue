<script setup lang="ts">
import { useOsmosisStore } from "@/lib/store";
import LoadingScreen from "@/components/LoadingScreen.vue";
import TopBar from "@/components/TopBar.vue";
import ProgressBar from "@/components/ProgressBar.vue";

const store = useOsmosisStore();
</script>

<template>
  <Transition>
    <LoadingScreen v-if="!store.connected" />
  </Transition>

  <div class="w-screen z-0 flex flex-col">
    <TopBar />
    <ProgressBar />
    <RouterView />
  </div>
</template>

<style>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
