---
name: travel-handbook
description: 旅行攻略手册网页生成器。当用户想把一次即将到来的旅行做成可发布、可分享的在线手册/行程攻略网页，或提到「旅行手册、行程单、双城攻略、倒计时、旅行网页、朋友拿到链接就能看」时使用。用户只需陆续提供机票、酒店、门票、活动的 PDF/截图（无需打字录入），即可产出零依赖、可离线的响应式单页：此刻关注卡片（下一个行程+每秒跳动的大号倒计时+当前待办+实时天气）、手绘 SVG 行程总览地图（按天配色、标出每晚住宿）、已确认机票/酒店卡片、逐日可折叠行程（已结束折叠、今天及以后展开）、待办清单与进度、实用贴士；每个地点可一键唤起 Google 导航、点击名称弹出中文介绍、拍照参考与备份美食。模板与构建/地图/弹窗/倒计时/天气引擎固定，每趟只换一份 guide_data.js。
---

# Travel Handbook

把一次**将来时**的旅行做成功能型、手账感的单页手册。核心是**数据 / 引擎分离**：
`assets/template.html`（样式 + 全部渲染引擎）不变，每趟只写一份 `guide_data.js`，
用户整理成本最低，且与 `travel-memory-book`（过去时纪念册）形成一对。

## 用户给什么

- 机票 / 酒店 / 门票 / 活动的 **PDF 或截图**，可陆续发；信息由助手提取，不让用户打字。
- 天数、人数、城市；未出票活动先记为待办。
- 若要拍照参考，需要时由用户扫码 / 登录小红书协助采集。

## 端到端流程（精简）

1. **等用户发完**订单 → 输出信息确认表，逐项核对后再动手。
2. 提取订单、建 `PLACES`，**逐一核对 Google 坐标**。
3. **以已出票航班为锚**排 `DAYS/items`，时间对不上整体重排。
4. 核对闭馆日 / 节假日售罄 / 需预约点 / 车程船程 / 是否顺路。
5. 准备城市地理数据与拍照参考，写 `guide_data.js`。
6. 构建：`python scripts/build_guide.py --template assets/template.html --data guide_data.js --out ./site/index.html`。
7. 双端自检：`python scripts/verify_guide.py ./site` + 人工逐张看截图。
8. 发布：`lark-cli apps +deploy --dir ./site`，轮询到 finished 交付链接。

完整命令、口径与核对清单见 [references/workflow.md](references/workflow.md)。

## 何时读哪份参考

- 填写 / 核对数据结构、字段与写作口径 → [references/data_schema.md](references/data_schema.md)。
- 制作总览 / 当日地图（投影、取景、意向化、防遮挡、增减城市）→ [references/map_guide.md](references/map_guide.md)。
- 配色、昼夜主题、字体、卡片版式、响应式 → [references/visual_spec.md](references/visual_spec.md)。
- 完整流程、核对清单、双端自检、发布与隐私红线 → [references/workflow.md](references/workflow.md)。

## 交付前自检要点

桌面 + 手机双端确认：控制台无 error；**倒计时每秒跳动**、当前待办与天气正常；
总览图每城完整不裁切、当日图放大且点位 / 标签**互不遮挡**，远机场 / 离岛意向化、
焦点是当天核心点；地点可一键 Google 导航、弹窗中文介绍完整；已结束日期折叠、
今天及以后展开；无横向溢出。改后重新 build 并全量复检。

## 硬约束

- 以已出票航班为锚排行程；数字（门票、用时、车程、坐标）有依据、不编造。
- 景点 why/see 具体（年代、人物、建筑、看点），不写空话；餐厅给推荐菜与备份。
- 证件号、护照号、票号、PNR、确认号、订单号、房间号、酒店电话不进公开页；
  账号 / 密码 / token 不写产物或记忆。
- 页面保持终稿，无版本说明 / 修改日志；交付前电脑端与手机端必须都可用。
