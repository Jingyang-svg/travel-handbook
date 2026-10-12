# 工作流程

把一次旅行从「订单截图」做成「可分享的在线手册」的完整流程。
核心原则：**不让用户打字录入订单**，信息从 PDF / 截图提取；**先确认再动手**；
交付前**桌面 + 手机双端都可用**。

## 开工前（硬规则）

- 用户会陆续发机票、酒店、门票、路书等 PDF / 截图。**在用户说「发完了」之前不开始做页面。**
- 发完后，先输出一份**信息确认表**（航班、酒店、活动、天数 / 人数 / 城市），
  与用户逐项核对无误，再进入制作。
- 页面是公开网址，确认表阶段就剔除一切敏感信息（见隐私红线）。

## 阶段 A：收集与提取

1. 读全部附件：PDF 用 pdf 工具 / 解析，截图直接看图，**逐份提取**：
   - 航班：航司、航班号、日期、起降时间 / 机场、航站楼；
   - 酒店：店名、入离日期、晚数、是否含早、地址；
   - 活动 / 门票：名称、日期、场次时间、地点、是否已出票。
2. 汇总成确认表交用户核对。航班时间是排行程的**锚**。
3. 已出票 / 已确认的才进「确认卡片」；未出票的活动进待办，不假装已订。

## 阶段 B：建地点、核坐标

1. 在 `PLACES` 为每个机场 / 酒店 / 餐厅 / SPA / 景点建一个 key。
2. **每个点的 lat/lng 用 Google Maps 逐一核对**（搜地点、读坐标），错一个导航就错。
3. 写 `n/sn/e`；按 `CAT` 标注非景点类型（不写即景点）。
4. 景点写详尽 `why/see`（年代、人物、建筑、藏品、看点），`exp` 写开放时间 / 门票 / 着装 / 用时。
5. 餐厅在 `DISHES` 写推荐菜、`ALTFOOD` 写同片区备份餐厅。

## 阶段 C：以航班为锚排行程

1. 先把每个航班的起降时间固定，再在其前后填当天 items（`t/p/title/fee/book/desc`）。
2. **时间对不上就整体重排，不硬塞**；跨城转场天预留足够车程 / 船程 / 值机时间。
3. 每天设 `route`（按到访顺序）、`color`、`mapCity`、`hotel`；末日 hotel 为 null。
4. 大跨度转场（去机场、离岛）设 `cut`，让当日图聚焦核心点。
5. 填 `DAY_MOVE`：每段 / 每条目的交通方式；`FLIGHTS/HOTELS/EVENTS/TODO_GROUPS/TIPS` 补齐。

## 阶段 D：核对（逐项，见核对清单）

闭馆日、节假日 / 周末售罄、需预约的免费点、各段车程 / 船程、路线是否顺路、坐标是否准确。
有问题就调整顺序或换确定方案，不把不合理的安排留在页面里。

## 阶段 E：城市地理与拍照参考

1. 按 map_guide 准备 `VIEW/GEO/ROADS/STATIONS/RIVER/LINES/EDGE/LABEL_ADJ/DAY_LBL/MFACT`。
2. 拍照参考 `XHS_DATA`：用浏览器登录小红书，按景点采集 4 条（2 景 + 2 人），
   保存原帖链接与配图（图压缩后内联 base64）。登录 / 扫码请用户协助，不替用户注册。
3. 城市数与默认双城不同时，按 map_guide「新增 / 改变城市数量」改模板那几处。

## 阶段 F：构建（零依赖）

```bash
python scripts/build_guide.py --template assets/template.html --data guide_data.js --out ./site/index.html
```

构建器只用 Python 标准库做占位替换，无第三方依赖、无网络。

## 阶段 G：双端自检

1. 自动脚本（桌面 1440 / 手机 390，动态定位景点与城市）：

```bash
python scripts/verify_guide.py ./site
# 云端浏览器装在用户目录时：
PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/ms-pw python scripts/verify_guide.py ./site
```

   要求：console 无 error、地图与天数正确、弹窗含 why、**倒计时秒数每秒跳动**、
   导航 URL 正确、确认卡片已渲染。
2. **人工看截图**（脚本输出在 `site/_shots/`），逐张核对：
   - 总览图每城完整、不被裁切；当日图放大、点位 / 标签**互不遮挡**；
   - 远机场 / 离岛已意向化（虚线 + 图标），焦点是当天核心点；
   - 弹窗内容完整、菜品 / 备份 / 必看 / 拍照参考齐全；
   - 手机端布局正常、无横向溢出。
3. 任一不过：改数据 → 重新 build → **全量复检**（不接受只看改的那一处）。

## 阶段 H：发布

**主路径 · lark-cli 一键发布（无需 Git / 命令行配置）**：

```bash
# 路径相对当前目录，先 cd 到产物所在层
lark-cli apps +deploy --dir ./site
# 返回 release_id 后轮询：
lark-cli apps +release-get --app-id <app_id> --release-id <release_id>
# status=finished 后读 online_url
```

复发布更新同一应用时带 `--app-id app_xxx`（首次返回的 app_id 要记住）。

**备选 · Cloudflare Workers + GitHub（push 即上线）**：把 `site/index.html` 放入仓库，
用 Workers 静态资源 / Pages 连接 GitHub；需要用户在网页完成的授权步骤一次性列清楚，
不让用户装命令行工具。Skill 源码本身也用 Git 管理（见下）。

## 后续新增 / 修改活动

- 新增一个活动：在 `PLACES` 加地点（核坐标）→ 当天 `route` 插入 key →
  `items` 加一条（设时间 / fee / book）→ 更新 `DAY_MOVE` → build → 双端复检 → 发布。
- 已结束的日期保持折叠；只动今天及以后，不改已发生的安排。
- 活动临时改时间：以新时间重排当天 items，冲突就整体顺延。

---

## 核对清单（阶段 D 逐项打勾）

- [ ] 每个景点**开放时间 / 闭馆日**已核对（博物馆常周一 / 周二闭馆）。
- [ ] 周末 / 节假日的**售罄 / 限流风险**已评估，热门活动 / 餐厅提示提前订。
- [ ] **免费但需预约**的景点已标出预约方式。
- [ ] 相邻点之间的**车程 / 船程 / 步行时长**合理，且与时间轴留的余量匹配。
- [ ] 当天路线**顺路**、不往返折返；不顺就调整顺序。
- [ ] 每个点 **Google 坐标准确**（抽查导航落点）。
- [ ] 国际 / 国内航班的值机提前量、机场 / 航站楼正确（尤其同城多机场别走错）。

## 隐私红线（公开页面）

**绝不写进页面 / 数据文件**：确认号、证件号、护照号、票号、PNR、订单号、
房间号、酒店电话、银行卡号；账号 / 密码 / token 不写进产物，也不写进长期记忆。
需要本人核对的敏感信息只在对话里确认，不落页面。页面保持终稿，无版本说明 / 修改日志。

## Git 管理 Skill 源码

在 skill 目录用 Git 管理并推送 GitHub（与 `travel-memory-book` 并列）：

```bash
git init -b main
git add .
git -c user.name=Jingyang-svg -c user.email=yinjingyang585658@gmail.com commit -m "feat: travel handbook skill"
# 创建公开仓库并推送（需有效 GitHub 凭据 / gh 已登录）：
gh repo create travel-handbook --public --source=. --remote=origin --push
```

无有效凭据时：请用户提供有 `repo` 权限的 PAT（classic）或 fine-grained token
（Contents 读写 + Administration 可建仓），或让用户在网页建好空仓库后，用
`https://<token>@github.com/Jingyang-svg/travel-handbook.git` 推送；推送后把 remote
改回不含 token 的干净 URL。token 用后不保存到仓库 / 记忆。
