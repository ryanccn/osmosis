<script setup lang="ts">
const props = defineProps<{
  description: string;
  modelValue: string;
  placeholder?: string;
}>();

const $emit = defineEmits<{ (ev: "update:modelValue", value: string): void }>();

const update = (ev: Event) => {
  $emit("update:modelValue", (ev.target as HTMLInputElement).value);
};
</script>

<template>
  <label class="flex flex-col gap-y-1 w-full">
    <span class="text-sm font-semibold">{{ description }}</span>
    <input
      type="text"
      class="osmosis form input w-full"
      :value="props.modelValue"
      :placeholder="placeholder"
      @input="update"
    />
  </label>
</template>
