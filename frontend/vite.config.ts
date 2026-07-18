import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  root: ".",
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": process.env.VITE_API_URL || "http://127.0.0.1:5000",
    },
  },
  build: {
    // Disable sourcemaps to save memory and CPU during build
    sourcemap: false,
    // Slightly reduces memory usage during the minification phase
    cssCodeSplit: true,
    chunkSizeWarningLimit: 1000,
  },
});
