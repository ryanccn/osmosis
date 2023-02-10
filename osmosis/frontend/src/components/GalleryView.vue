<script setup lang="ts">
import { useOsmosisStore } from "@/lib/store";

const store = useOsmosisStore();
</script>

<template>
  <div class="flex flex-col gap-y-2 h-full">
    <div class="flex gap-x-2 items-center p-4">
      <!-- <button class="bg-red-500 text-white osmosis danger button">
        Delete
      </button> -->
    </div>

    <div class="grid grid-cols-3 gap-4 p-4 overflow-y-scroll">
      <button
        v-for="name in store.gallery"
        :key="name"
        @click="store.gallerySelected = name"
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
