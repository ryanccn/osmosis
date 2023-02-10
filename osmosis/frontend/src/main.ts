import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import "./styles.css";
import { setupStoreListeners } from "@/lib/store";
import { router } from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);
setupStoreListeners();

app.mount("#app");
