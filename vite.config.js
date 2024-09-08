import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/"
  // !!! base !!!
  // 这个键值影响了build项目之后访问网页的根目录
  // 如果设置错误，访问index.html会导致大量静态资源404
})


