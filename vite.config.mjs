// vite.config.mjs — Vite 构建配置
//
// 本配置的核心作用：声明项目的【多页面入口】。
// 项目有两个页面 index.html 和 text-lab.html，
// 不配置的话 Vite 默认只处理 index.html，text-lab.html 不会出现在 dist 里。
import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        // main = 首页（个人主页）
        main: resolve(import.meta.dirname, "index.html"),
        // lab = 文字实验室页
        lab: resolve(import.meta.dirname, "text-lab.html"),
      },
    },
  },
});