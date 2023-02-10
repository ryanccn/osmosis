import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig(({ mode }) => ({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    proxy:
      mode === "development"
        ? {
            "/outputs": {
              target: "http://127.0.0.1:26538/",
              changeOrigin: true,
            },
            "/socket.io": {
              target: "ws://127.0.0.1:26538",
              ws: true,
            },
          }
        : undefined,
  },
}));
