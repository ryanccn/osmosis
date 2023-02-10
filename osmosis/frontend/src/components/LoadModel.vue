<script setup lang="ts">
import { ref } from "vue";
import { useOsmosisStore } from "@/lib/store";

import {
  TransitionRoot,
  Dialog,
  TransitionChild,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

const emit = defineEmits(["close"]);
const props = defineProps<{ isOpen: boolean }>();

const enum Tabs {
  INDEX,
  ADD,
  DIFFUSERS,
  COREML,
  CKPT,
}

const store = useOsmosisStore();

const tab = ref(Tabs.INDEX);
const diffusersModelId = ref("");

const loadModel = (internalId: string) => {
  store.loadModel(internalId).then(() => {
    emit("close");
  });
};

const addDiffusersModel = (id: string) => {
  store.addModel("diffusers", id).then(() => {
    tab.value = Tabs.INDEX;
  });
};
</script>

<template>
  <TransitionRoot
    appear
    :show="props.isOpen"
    as="template"
    @after-leave="tab = Tabs.INDEX"
  >
    <Dialog as="div" @close="$emit('close')" class="relative z-10">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-bg text-fg p-8 flex flex-col items-start gap-y-4 shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="flex w-full justify-between text-2xl font-bold mb-2"
              >
                <span>Load model</span>
                <button
                  class="osmosis primary button self-end"
                  @click="tab = Tabs.ADD"
                  v-if="tab === Tabs.INDEX"
                >
                  + Add new
                </button>
              </DialogTitle>

              <template v-if="tab === Tabs.INDEX">
                <button
                  class="px-4 py-3 text-lg bg-surface hover:bg-surface-hover transition-all rounded-md w-full"
                  @click="loadModel(model[0])"
                  v-for="model in Object.entries(store.availableModels)"
                  :key="model[0]"
                >
                  {{ model[1].id }}
                </button>
              </template>
              <template v-else-if="tab === Tabs.ADD">
                <button
                  class="w-full px-4 py-3 text-lg font-medium bg-surface hover:bg-surface-hover transition-all rounded-md"
                  @click="tab = Tabs.DIFFUSERS"
                >
                  Diffusers
                </button>
                <button
                  class="w-full px-4 py-3 text-lg font-medium bg-surface hover:bg-surface-hover transition-all rounded-md"
                  @click="tab = Tabs.COREML"
                  disabled
                >
                  CoreML model (macOS)
                </button>
                <button
                  class="w-full px-4 py-3 text-lg font-medium bg-surface hover:bg-surface-hover transition-all rounded-md"
                  @click="tab = Tabs.CKPT"
                  disabled
                >
                  Checkpoint file
                </button>
              </template>
              <template v-else-if="tab === Tabs.DIFFUSERS">
                <input
                  type="text"
                  class="osmosis form input w-full"
                  v-model="diffusersModelId"
                />
                <button
                  class="osmosis primary button"
                  @click="addDiffusersModel(diffusersModelId)"
                >
                  Add
                </button>
              </template>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
