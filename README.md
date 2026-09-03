# zero-to-tech · Next.js 版（模块 4.5 终点 + 5.5 前端联调）

《零到全栈》课程主线项目的当前形态，一句话介绍：

> **双页面个人站点在 Next.js 框架下的样子**（个人主页 + 文字实验室），并且已经接上了模块 5 搭的后端 API——前端一半已完成前后端联调，后端一半在 `backend/`（FastAPI，模块 5 一路搭的）。

它同时承担两个课程阶段的角色：

- **模块 4.5 终点成品**：把 4.4 的 React 项目（Vite + 手搓 `useRoute`）整体搬到 Next.js App Router。网站长相不变；变的是路由层（`app/` 文件夹即路由）和入口（没有 `index.html` / `main.jsx` / `App.jsx` 了）。
- **已包含 5.5 的前端替换文件**：四个组件（`HomeView` / `TextLabView` / `InputCard` / `ResultCard`）都已从「写死数据」改成「去调后端 API」，并配好了 `.env.local`。

## 技术栈

| 依赖 | 版本 | 用途 |
| --- | --- | --- |
| `next` | ^15.0.0 | App Router 框架（文件夹=路由、预渲染） |
| `react` / `react-dom` | ^19.2.6 | UI 库 |
| `animejs` | ^4.4.1 | 卡片入场 / 分数滚动动画 |
| 语言 | 纯 `.jsx`（无 TypeScript） | — |

## 快速开始

```bash
npm install
npm run dev        # http://localhost:3000（Next 默认端口）
```

打开两个页面：

- `/` — 个人主页（座右铭、正在学习、作品入口）
- `/text-lab` — 文字实验室（贴一段中文 → 分析拼音与情感）

### 生产构建（静态导出）

`next.config.mjs` 里开了 `output: "export"`——构建产物是**纯静态 HTML**，不需要常驻 Node 服务器：

```bash
npm run build      # 产物输出到 out/
npx serve out      # 任意静态服务器预览都行
```

> 注意：静态导出模式下 `next start` 不可用（没有服务器可起），用上面的方式预览。
> 两个 API 请求都发生在**浏览器端**（组件全部是客户端组件），所以静态托管后后端照常生效。

## 连接后端（模块 5 线）

- **地址配置**：`.env.local` 里写 `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`。
  - `NEXT_PUBLIC_` 前缀的意思：这个变量会被打进浏览器代码，改地址**只动这一个文件**，组件代码一个字不用碰。
- **接口约定**（前端按这两个接口写的）：

| 接口 | 方法 | 请求 | 返回 |
| --- | --- | --- | --- |
| `/api/profile` | GET | — | `{ heroTitle, heroSubtitle, featuredWork: {…}, identity: {…} }` |
| `/api/analyze` | POST | `{ "text": "…" }` | `{ text, pinyin, score, label }` |

- **后端没跑时不会崩**：页面先拿 `data/site.js` 的打底数据渲染，请求失败被 `try/catch` 接住、错误只打到控制台。
- **需要后端开 CORS**：跨端口（前端 3000 → 后端 8000）要被后端允许才行，这是模块 5.5 课件里后端那一半的内容。
- 目前 `pinyin` / `score` / `label` 还是后端占位/粗略值，模块 6 换真的。

## 项目结构

```
zero-to-tech/
├─ app/                        # 文件夹 = 路由
│  ├─ layout.jsx               # 全站外壳：<html>/<body> + import 8 个 css + metadata
│  ├─ page.jsx                 # /            → 渲染 <HomeView />
│  └─ text-lab/
│     └─ page.jsx              # /text-lab     → 渲染 <TextLabView />
├─ components/
│  ├─ Nav.jsx                  # 顶部品牌 + 导航（<Link> + usePathname 高亮）
│  ├─ HomeView.jsx             # 首页：site.js 打底 → fetch /api/profile 覆盖
│  ├─ TextLabView.jsx          # 实验室页：状态提升 result
│  ├─ InputCard.jsx            # 输入区：POST /api/analyze
│  ├─ ResultCard.jsx           # 结果区：显示 result（分数数字滚动动画）
│  ├─ PageHeading.jsx          # 大标题 + 副标题（纯展示，服务端组件）
│  └─ AnimatedCardGrid.jsx     # 卡片网格 + animejs 错峰入场动画
├─ css/                        # 8 个样式文件（见下方清单）
├─ data/site.js                # 网站内容集中地（数据与界面分离）
├─ .env.local                  # NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
└─ next.config.mjs             # output: "export"（静态导出）
```

### 组件边界：谁需要 `"use client"`

Next.js 里组件默认在服务器上渲染（服务端组件）；一旦用到浏览器能力（`useState` / `useEffect` / 事件 / `usePathname`），就要在文件顶部写 `"use client"`：

| 组件 | 用了什么 | 组件类型 |
| --- | --- | --- |
| `PageHeading` | 纯展示 | 服务端组件 |
| `Nav` | `usePathname` | 客户端 |
| `HomeView` / `TextLabView` | `useState` + `useEffect`（fetch） | 客户端 |
| `InputCard` / `ResultCard` / `AnimatedCardGrid` | state / animejs | 客户端 |

### 两条数据流（5.5 的核心）

1. **首页实时化**：`HomeView` 先用 `site.js` 的 `home` 打底，`useEffect` 里 `GET /api/profile`，成功后 `setData` 覆盖界面。
2. **状态提升**：`InputCard` 负责发请求、`ResultCard` 负责显示，两个兄弟组件要共享同一份 `result`，就把它提级到共同的父组件 `TextLabView` 里，用 `onResult={setResult}` 传下去。

## 与模块 4.4 的对比（迁移时变了什么）

| 4.4（React / Vite） | 4.5（Next.js） |
| --- | --- |
| `index.html` + `src/main.jsx` + `src/App.jsx` | `app/layout.jsx`（全站外壳） |
| 手搓 `useRoute()` + `navigate()` + 监听 popstate | `app/` 文件夹路由 + `<Link>` + `usePathname` |
| 页面调 `navigate("/text-lab")` | 页面用 `<Link href="/text-lab">` |
| 组件没有 `"use client"` 概念 | 涉及浏览器能力的组件要标 `"use client"` |
| Vite dev server | `next dev`（端口 3000） |

## CSS 体系（8 个文件）

| 文件 | 职责 |
| --- | --- |
| `reset.css` | 浏览器默认样式清零 |
| `variables.css` | 设计变量（颜色 / 间距 / 字体） |
| `layout.css` | 页面外壳（app-shell / page-shell / page-content） |
| `hero.css` | 每页顶部 hero 区 |
| `nav.css` | 顶部导航条 |
| `cards.css` | 卡片面板（动画入口） |
| `lab.css` | 文字实验室专属（输入区 / 结果区 / 徽章） |
| `responsive.css` | 响应式（窄屏适配） |

## 命令速查

```bash
npm install        # 装依赖
npm run dev        # 开发模式 → http://localhost:3000
npm run build      # 构建（output: export → out/）
npx serve out      # 预览静态产物
```