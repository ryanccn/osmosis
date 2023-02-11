<script setup lang="ts">
// import { ref } from "vue";
import { Switch } from "@headlessui/vue";

const props = defineProps<{ modelValue: boolean; description?: string }>();
const $emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
}>();

const onClick = (v: boolean) => $emit("update:modelValue", v);
</script>

<template>
  <Switch
    :model-value="props.modelValue"
    @update:model-value="onClick"
    :class="
      props.modelValue ? 'bg-accent' : 'bg-surface hover:bg-surface-hover'
    "
    class="relative inline-flex h-5 w-8 items-center rounded-full transition"
  >
    <span class="sr-only" v-if="description">{{ description }}</span>
    <span
      :class="props.modelValue ? 'translate-x-4' : 'translate-x-1'"
      class="inline-block h-3 w-3 transform rounded-full bg-white transition"
    />
  </Switch>
</template>
