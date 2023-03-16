<script setup lang="ts">
import { useOsmosisStore } from "@/lib/store";

const store = useOsmosisStore();

const setNewGallerySelected = async (name: string) => {
  store.setGallerySelected(name);
};
</script>

<template>
  <div class="flex flex-col gap-y-2 p-4 h-osmosis-content">
    <div class="grid grid-cols-3 gap-4 p-4 overflow-y-scroll">
      <button
        v-for="name in store.gallery"
        :key="name"
        @click="setNewGallerySelected(name)"
      >
        <img
          :src="`/outputs/${name}`"
          class="block rounded transition-all"
          :class="{
            'ring ring-accent ring-offset-2 ring-offset-bg':
              store.gallerySelected === name,
          }"
          loading="lazy"
          decoding="async"
        />
      </button>
    </div>
  </div>
</template>
