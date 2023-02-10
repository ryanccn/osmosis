import { createRouter, createWebHashHistory } from "vue-router";
import TextToImage from "./views/TextToImage.vue";

export const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", redirect: "/txt2img" },
    { path: "/txt2img", component: TextToImage },
  ],
});
