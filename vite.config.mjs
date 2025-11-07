import { defineConfig } from 'vite'
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./assets"),
    assetsDir: '',
    ssr: true,
    rollupOptions: {
      input: {
        'index': resolve('./static/vite_index.html'),
        'app': resolve('./static/css/app.css'),
        // 'annual': resolve('./static/js/annual.mjs'),
        // 'categorize': resolve('./static/js/categorize.mjs')
      }
    }
  },
  plugins: [
    tailwindcss()
  ]
})