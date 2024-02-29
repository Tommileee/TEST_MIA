import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tsconfigPaths from 'vite-tsconfig-paths'
import { generateSlug } from 'random-word-slugs'

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    __COMPILE_TIME__: Date.now(),
    __VERSION_SLUG__: JSON.stringify(generateSlug(3))
  },
  base: '/TBA-Berlin-FI/MIA/',
  build: {
    outDir: 'dist'
  },
  plugins: [svelte(), tsconfigPaths()],
})
