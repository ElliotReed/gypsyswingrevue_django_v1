// vite.config.js
import { defineConfig } from "vite"
import path from "path"

export default defineConfig({
  root: path.resolve(__dirname, "assets"),
  // 2. Must match Django's STATIC_URL exactly
  base: "/static/",

  build: {
    manifest: true,       // Generates manifest.json Django needs
    outDir: path.resolve("./static"),  // Where compiled assets go
    emptyOutDir: true,
    rollupOptions: {
      input: {
        app: "js/app.js",  // Your entry point

        frontPage: "js/pages/frontPage.js",
        store: "js/pages/store.js",
      }
    },
  },
  server: {
    host: "localhost",
    port: 5173,
    open: false,
    watch: {
      // 5. Explicitly ignores your Python virtual environment and Django folders
      ignored: ["**/venv/**", "**/.venv/**", "**/migrations/**", "**/*.py"],
      usePolling: false,
    },
    hmr: {
      host: "localhost",
    },
  },
})