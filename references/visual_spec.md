# 视觉规范

旅行手册是**功能型、纸质手账感**的单页：温暖的米纸底色、衬线标题、手绘地图、
圆角卡片。视觉为信息服务——让朋友一眼看到「现在该干嘛 / 下一个行程 / 今天怎么走」。

## 昼夜双主题（自动跟随系统）

用 `@media (prefers-color-scheme: dark)` 自动切换，**无需手动开关**。两套都定义在 `:root`：

浅色（默认）：

| token | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#f4f0e6` | 页面米纸底 |
| `--surface` | `#fffdf7` | 卡片底 |
| `--surface-2` | `#f1ecdf` | 内嵌块 / 倒计时格 |
| `--ink` / `--ink-soft` | `#22312e` / `#5d6a65` | 正文 / 次要文字 |
| `--line` | `#ddd6c5` | 描边、分隔 |
| `--accent` | `#0e7c7b` | 主强调（Teal，按钮 / 链接 / 进度） |
| `--book` | `#c8632a` | **需预订**标记（暖橙） |
| `--free` | `#3f7d49` | 免费 / 已出票（绿） |

深色：底 `#0e161a`、卡片 `#152127`、强调提亮为 `#54bdae`、预订色 `#e08a52`，
阴影改为黑色半透明。地图色也整体调暗（见下）。

**每日配色**（`--c1`–`--c6`，总览路线 / 当日图 / 时间轴点）：

```
--c1 #d9772f 橙   --c2 #3d7fc0 蓝   --c3 #159a93 青
--c4 #8a6bb0 紫   --c5 #53a14f 绿   --c6 #c75642 砖红
```

地图色：`--map-bg` / `--sea` / `--land` / `--coast` / `--river` / `--road` /
`--map-fly`（意向化段统一灰）/ `--map-fly`。深色下逐一调暗。

## 字体（完全离线）

**不引入任何网络字体 / 字体文件**，用系统字体栈，保证离线、秒开：

- 正文：`-apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Segoe UI", sans-serif`
- 标题（h1/h2/h3、day 标题、now 事件）：`Georgia, "Times New Roman", "Songti SC", "STSong", serif`
- 数字（倒计时、费用、电话）：`.num` 用 Helvetica/Arial + `font-variant-numeric: tabular-nums`（等宽数字，跳动不抖动）。

基础字号 15.5px、行高 1.65；内容列 `max-width:760px` 居中。

## 版式骨架

- `.wrap`：max-width 760、左右 16px、底部 70px。
- **Hero**：kicker（大字距小字）→ H1（38px，桌面 44px）→ meta（日期 / 天数 / 人数）。
- **区块** `.sec`：`sec-head`（编号 `sec-no` + H2 + hint），上间距 40px。
- **卡片** `.card`：圆角 15、1px `--line` 描边、柔和阴影；`.card-pad` 统一内边距。

## 各模块要点

**此刻关注 #now**：顶部 4px accent 边；事件名衬线 19px；倒计时四格等宽
（`.cd-unit`，数字 27px），每秒跳动；「当前待办」用 accent-soft 底胶囊，全部完成时转灰。

**地图**：`.map-box` 圆角卡片，SVG `width:100%`；海滨城市总览（如普吉）用
`max-width:470px` 居中保持正方形不裁剪；标签带 `--surface-2` 描边（`paint-order:stroke`）
保证压在底图上仍清晰；指北针、图例在底部。

**确认卡片**：桌面两列、手机一列；左 38px 图标方块 + 标题 / 明细 / 虚线分隔备注。

**逐日行程**：每天一张 `.day` 卡片；头部为日期徽章（当天色块，含 D 几 + 日期）、
衬线标题、城市副标题、旋转箭头；展开体含当日 facts 四格（手机两格）、当日地图、
两个工具按钮（全天多点导航 primary / 折叠）、时间轴。
时间轴左 52px 时间 + 中轴圆点连线 + 右内容；标签 tag：
需预订 `tag-book` 橙、免费 `tag-free` 绿、费用 `tag-fee` 灰、交通 `tag-move`。

**待办**：顶部进度卡（渐变进度条 + 已完成 x/y），分组列出，点击勾选、划线变灰。

**贴士**：桌面两列；每卡标题带图标，列表内可用 `<b>` 与 `.num`。

**弹窗 modal**：移动端**底部抽屉**（贴底、上滑动画、圆角仅上方），
桌面端居中对话框；含英文名、快速事实 chips、为什么来 / 能看到什么 / 体验重点、
菜品 chips、备份餐厅、必看清单、拍照参考（可折叠 `<details class="m-det">`）、
底部导航按钮。长内容可滚（max-height 88vh）。

## 纹理

全站铺一层极轻噪点（`body::after`，SVG `feTurbulence`，浅色 multiply `.05`、
深色 screen `.045`），把纯平底色变成「印刷纸」质感。`pointer-events:none` 不挡点击。

## 响应式断点

| 断点 | 变化 |
| --- | --- |
| `min-width:600px` | 确认卡 / 贴士两列，H1 放大 |
| `max-width:560px` | day-facts 两列，地图标签字号缩小，当日图主带占 74% |
| `max-width:380px` | 倒计时数字缩小，时间轴时间列收窄 |

使用 `viewport-fit=cover` 与 `env(safe-area-inset-bottom)` 适配刘海屏；
弹窗按钮内边距加 safe-area。

## 不要做（slop 红线）

- 不引网络字体、不引地图 / 图表 CDN、不用 Google Maps 底图（保持单文件离线）。
- 不做毛玻璃 / 发光描边 / 粒子网 / 紫蓝渐变 / 卡片 hover 上浮。
- 不给每个元素加入场动画；仅弹窗上滑、折叠展开、箭头旋转、进度条 / 倒计时为动态。
- 不用 emoji 当功能图标；功能图标一律用引擎 IC 里的内联 SVG。
- 配色与每日色已固定，换旅行时**沿用同一套 token**，保持系列一致性。
