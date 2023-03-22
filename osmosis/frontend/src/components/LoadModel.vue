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
import LoadModelTextInput from "./LoadModelTextInput.vue";
import Switch from "./Switch.vue";

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
const diffusersRevision = ref("");
const diffusersHalf = ref(false);

const mlpackagesDir = ref("");

const modelTypeToReadable = (str: string) => {
  if (str === "diffusers") return "Diffusers";
  else if (str === "coreml") return "CoreML";
  else if (str === "checkpoint") return "Checkpoint";
  return "Unknown";
};

const loadModel = (internalId: string) => {
  store.loadModel(internalId).then(() => {
    emit("close");
  });
};

const addDiffusersModel = () => {
  if (!diffusersModelId.value) return;

  store
    .addModel({
      type: "diffusers",
      id: diffusersModelId.value,
      revision: diffusersRevision.value,
      half: diffusersHalf.value,
    })
    .then(() => {
      tab.value = Tabs.INDEX;
    });
};

const addCheckpointModel = () => {
  if (!diffusersModelId.value || !mlpackagesDir.value) return;

  store
    .addModel({
      type: "checkpoint",
      path: diffusersModelId.value,
      half: diffusersHalf.value,
    })
    .then(() => {
      tab.value = Tabs.INDEX;
    });
};

const addCoreMLModel = () => {
  if (!diffusersModelId.value || !mlpackagesDir.value) return;

  store
    .addModel({
      type: "coreml",
      path: diffusersModelId.value,
      mlpackages: mlpackagesDir.value,
    })
    .then(() => {
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
                class="flex w-full justify-between text-2xl font-bold mb-4"
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
                  class="px-6 py-4 flex flex-col items-start text-left gap-y-2 bg-surface hover:bg-surface-hover transition-all rounded-md w-full"
                  @click="loadModel(model[0])"
                  v-for="model in Object.entries(store.availableModels)"
                  :key="model[0]"
                >
                  <p class="text-lg font-bold">
                    {{ model[1].displayName ?? model[1].id
                    }}<span class="text-gray-400" v-if="model[1].revision"
                      >#{{ model[1].revision }}</span
                    >
                  </p>
                  <p class="text-sm">
                    {{ modelTypeToReadable(model[1].type) }}
                  </p>
                </button>
              </template>

              <template v-else-if="tab === Tabs.ADD">
                <button class="add-model-btn" @click="tab = Tabs.DIFFUSERS">
                  Diffusers
                </button>
                <button
                  class="add-model-btn"
                  @click="tab = Tabs.COREML"
                  v-if="store.coreMLAvailable"
                >
                  CoreML model
                </button>
                <button class="add-model-btn" @click="tab = Tabs.CKPT">
                  Checkpoint file
                </button>
              </template>

              <template v-else-if="tab === Tabs.DIFFUSERS">
                <LoadModelTextInput
                  description="Model ID on Hugging Face"
                  v-model="diffusersModelId"
                />
                <LoadModelTextInput
                  description="Revision (optional)"
                  v-model="diffusersRevision"
                  placeholder="main"
                />
                <div class="flex flex-row items-center gap-x-2">
                  <Switch v-model="diffusersHalf" />
                  <span>Half precision?</span>
                </div>
                <button
                  class="osmosis primary button"
                  @click="addDiffusersModel()"
                >
                  Add
                </button>
              </template>
              <template v-else-if="tab === Tabs.COREML">
                <LoadModelTextInput
                  description="Model ID on Hugging Face"
                  v-model="diffusersModelId"
                />
                <LoadModelTextInput
                  description="Converted directory with .mlpackages"
                  v-model="mlpackagesDir"
                />

                <button
                  class="osmosis primary button"
                  @click="addCoreMLModel()"
                >
                  Add
                </button>
              </template>
              <template v-else-if="tab === Tabs.CKPT">
                <LoadModelTextInput
                  description="Path to ckpt or safetensors"
                  v-model="diffusersModelId"
                />
                <div class="flex flex-row items-center gap-x-2">
                  <Switch v-model="diffusersHalf" />
                  <span>Half precision?</span>
                </div>
                <button
                  class="osmosis primary button"
                  @click="addCheckpointModel()"
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

<style scoped>
.add-model-btn {
  @apply w-full px-4 py-3 text-lg font-medium bg-surface hover:bg-surface-hover transition-all rounded-md;
  @apply focus:outline-none focus:ring focus:ring-accent/50;
  @apply disabled:opacity-75;
}
</style>
