# 数据结构（guide_data.js）

攻略采用**数据 / 引擎分离**：`assets/template.html` 是固定引擎（样式 + 全部渲染函数），
每趟旅行只写一份 `guide_data.js`——一段纯 JavaScript，由若干顶层 `var NAME = …` 组成，
构建时整段替换模板里的占位注释 `/*__GUIDE_DATA__*/`。

> 数据文件是 **JS 不是 JSON**：可写注释、可不加键引号、可内联 base64 图片。
> 但所有变量名、字段名必须与本文一致，引擎按名字读取。

## 变量清单（32 个）

| 变量 | 作用 |
| --- | --- |
| `META` | 封面 / 标题 / 页脚信息 |
| `PLACES` | 全部地点主数据（含介绍、拍照姿势） |
| `CAT` | 地点类型覆盖（默认按景点处理） |
| `DISHES` / `ALTFOOD` | 餐厅推荐菜 / 备份餐厅 |
| `STATIONS` / `ROADS_BK` / `ROADS_PK` | 交通站点 / 街道肌理 |
| `FLIGHTS` / `HOTELS` | 已出票航班 / 已订酒店 |
| `DAYS` | 逐日行程（核心） |
| `MOVE_TXT` / `DAY_MOVE` | 交通方式文案 / 每段交通方式 |
| `TODO_GROUPS` / `TIPS` | 待办清单 / 实用贴士 |
| `EVENTS` | 倒计时事件源 |
| `GEO_BK` / `GEO_PK` | 城市海岸线 / 轮廓环 |
| `VIEW` | 地图取景框 |
| `EDGE_OV` / `EDGE_DAY` | 离群点意向化坐标 |
| `RIVER` / `DASH` | 河流 / 虚线样式 |
| `BK_LINES` / `PK_LINES` | 总览路线连线 |
| `AIRPORTS` / `HOTEL_COLOR` / `MINOR` | 机场标记 / 酒店配色 / 次要地点 |
| `LABEL_ADJ` / `DAY_LBL` / `MFACT` | 标签偏移 / 快速事实 |
| `XHS_DATA` | 拍照参考（含内联图） |
| `WX_CITIES` | 天气城市配置 |

---

## META

```js
var META={
 docTitle:"曼谷 × 普吉 双城旅行手册 · YY & BB",  // document.title
 title:"曼谷 × 普吉<br>双城旅行手册",            // 封面 H1，可用 <br>
 kicker:"THAILAND · 6 DAYS 5 NIGHTS",            // 封面眉标
 dates:"2026.10.03 – 10.09", duration:"6 天 5 晚", who:"YY & BB",
 tz:"泰国 UTC+7（比北京慢 1 小时）",
 footer:"曼谷 × 普吉双城手册 · 仅供同行朋友查看"};
```

## PLACES

每个地点一个 key，字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `n` | 是 | 全名（弹窗标题、时间轴） |
| `sn` | 是 | 短名（地图标签） |
| `e` | 是 | 英文名 / 当地名 |
| `lat` / `lng` | 是 | **Google Maps 核对过的精确坐标**（小数） |
| `why` | 景点必填 | 为什么值得来：历史背景 + 地位 + 特色，3–5 句、有信息量 |
| `see` | 景点必填 | 能看到什么：逐一列具体看点 / 藏品 / 建筑 |
| `exp` | 是 | 体验贴士：开放时间、门票、着装、用时、注意事项 |
| `pose` | 景点 | 拍照姿势数组，见下 |

机场 / 酒店 / 餐厅 / SPA 的 `why`/`see` 可简短（讲清用途即可），
**只有景点（sight）需要详尽的 why/see**。餐厅的推荐菜放 `DISHES`，不写进 `see`。

`pose` 数组每项：

| 字段 | 说明 |
| --- | --- |
| `t` | 机位标题（如「东廊壁画前回眸」） |
| `spot` | 具体机位位置 |
| `pose` | 姿势 / 动作指导 |
| `time` | 最佳拍摄时段、光线 |
| `gear` | 镜头 / 构图建议 |
| `tip` | 可选，额外提示 |
| `img` | 可选，`[{u:图片URL,l:标签}]` 参考图（外链，非内联） |

## CAT

不写 `CAT` 的地点一律按**景点 sight** 渲染（详尽介绍 + 拍照姿势）。
需要覆盖类型时：

```js
var CAT={
 BKK:'airport', DMK:'airport', HKT:'airport',
 debtida:'hotel', courtyard:'hotel',
 kruaapsorn:'food', thipsamai:'food',
 preme:'spa', absothai:'spa'};
```

取值：`airport` / `hotel` / `food` / `spa`。

## DISHES / ALTFOOD

```js
var DISHES={
 kruaapsorn:["蟹肉炒长豆角","炸鸡翅","莲花茎咖喱","蟹肉炒蛋"],
 onechun:["蟹肉咖喱","臭豆炒虾","普吉叻沙","蕉叶蒸鱼"]};

var ALTFOOD={
 onechun:["Raya Restaurant｜普吉镇蟹肉咖喱老店","Tu Kab Khao｜米其林南泰菜老宅","Blue Elephant 蓝象｜殖民风高端泰菜"]};
```

- `DISHES`：key 为 food 地点，值为**推荐菜品**数组（4 个左右，用当地通用写法）。
- `ALTFOOD`：同片区、步行可达的**备份餐厅**，每项「店名｜一句话说明」，用于排队 / 售罄时兜底。

## STATIONS / ROADS_*

```js
var STATIONS=[
 {n:'BTS Asok',lat:13.7380,lng:100.5612,line:'bts'},
 {n:'MRT Sam Yan',lat:13.7325,lng:100.5265,line:'mrt'},
 {n:'ARL Makkasan',lat:13.7510,lng:100.5450,line:'arl'}];

var ROADS_BK=[
 {w:2.4,pts:[[100.5115,13.7668],[100.5085,13.7625], /* …[lng,lat]… */]}];
```

- `STATIONS`：`line` 取 `bts` / `mrt` / `arl`，当日地图上画站点小图标。
- `ROADS_BK` / `ROADS_PK`：示意街道网，`w` 为线宽、`pts` 为 `[lng,lat]` 折线，只画主要干道做肌理。

## FLIGHTS / HOTELS

```js
var FLIGHTS=[
 {no:'VZ3719',air:'泰国越捷',
  dep:{t:'01:15',d:'10.3',city:'北京大兴 PKX'},
  arr:{t:'05:00',d:'10.3',city:'曼谷素万那普 BKK'},
  anchor:{d:'2026-10-03',t:'01:15',tz:8},
  note:'红眼航班 · 出发前3天填 TDAC'}];

var HOTELS=[
 {place:'debtida',inD:'10.3',outD:'10.4',nights:1,meals:'含 10.4 双早',note:'早上先寄存行李，14:00 入住'}];
```

- `FLIGHTS.anchor` 是**倒计时锚点**：`d` 用完整 `YYYY-MM-DD`、`t` 为当地起飞时间、`tz` 为出发地时区（北京 8 / 泰国 7）。
- `HOTELS.place` 引用 `PLACES` 的 key（酒店需先在 PLACES 建好）。
- 航班是排行程的锚：**时间对不上就整体重排，不硬塞**。

## DAYS（核心）

```js
var DAYS=[
 {no:1,d:'10.3',wk:'周六',color:'var(--c1)',city:'曼谷',mapCity:'bk',hotel:'debtida',
  route:['debtida','grandpalace','watpho','kruaapsorn', /* …按到访顺序… */],
  items:[
   {t:'08:35',p:'grandpalace',title:'大皇宫 + 玉佛寺',fee:'500铢',book:true,
    desc:'8:30开门、8:35进场；需长裤/过膝裙、有袖，门口可租借'},
   /* … */
  ]},
 /* … */
];
```

| 字段 | 说明 |
| --- | --- |
| `no` | 第几天（1 起） |
| `d` | 日期 `M.D`（如 `10.3`） |
| `wk` | 星期（周X） |
| `color` | 当天主题色，用 `var(--c1)`…`var(--c6)` |
| `city` | 当天所在城市（可写「曼谷 → 普吉」） |
| `mapCity` | 用哪座城市的地图底图：`bk` / `pk`（可多城市时扩展） |
| `hotel` | 当晚住宿的 PLACES key；**最后一天无住宿填 `null`** |
| `route` | 当日到访地点 key，**按顺序**，驱动当日地图连线 |
| `items` | 时间轴，见下 |
| `feature` | 可选，专题标记，如 `'hike'`（徒步）触发专题介绍块 |
| `cut` | 可选，意向化切点：route 中该 index 之后的点用虚线 / 飞机符号表达 |
| `flySeg` / `flyPlane` | 可选，控制转场飞行段的画法 |

`items` 每项：

| 字段 | 说明 |
| --- | --- |
| `t` | 时间 `HH:MM`（24 小时） |
| `p` | 所在地点 key（引用 PLACES） |
| `title` | 事件标题 |
| `fee` | 可选，费用 / 门票（如 `500铢`、`已出票`、`免费`） |
| `book` | 可选，`true` 表示**需要提前预订**，时间轴上高亮标记 |
| `desc` | 这一步的说明（含衔接方式、用时、备注） |

## MOVE_TXT / DAY_MOVE

```js
var MOVE_TXT={car:'打车 Grab',train:'BTS/MRT 轨道交通',tuk:'嘟嘟车',walk:'步行',boat:'渡船/游船',plane:'飞机'};

var DAY_MOVE={
 1:{item:['','car','walk', /* 每个 item 一项，与 items 等长 */],
    seg:['walk','boat','car', /* route 相邻点之间，长度 = route-1 */],
    fly:[ /* 转场段，无则空数组 */ ]},
 /* … */
};
```

- 取值：`car` / `train` / `tuk` / `walk` / `boat` / `plane`，不需要图标处填 `''`。
- `item`：每个时间轴条目的**到达方式**（数组长度与当天 items 一致）。
- `seg`：route 中相邻两点之间的交通方式（长度 = route 点数 − 1），画在当日地图线段上。
- `fly`：跨城 / 飞行转场段。

## TODO_GROUPS / TIPS

```js
var TODO_GROUPS=[
 {g:'入境与证件',items:[
  {t:'护照有效期 6 个月以上、至少 2 页空白页'},
  {t:'入境前 3 天内填 TDAC 并保存确认页',s:'tdac.immigration.go.th · 免费'}]}];

var TIPS=[
 {h:'入境与时差',ic:'pass',li:[
  '<b>中国护照免签</b>入境，提前3天填 TDAC 并截图',
  '泰国比北京<b>慢 1 小时</b>']}];
```

- `TODO_GROUPS[].items[]`：`t` 为待办正文，`s` 可选为备注 / 网址。勾选状态存浏览器 localStorage（key 由引擎 `STORE` 决定），「此刻关注」里显示第一条未完成项。
- `TIPS[]`：`h` 标题、`ic` 图标名（用引擎 IC 里的 key，如 `pass`/`plane`/`cash`/`temple`/`shield`/`call`）、`li` 为 HTML 字符串数组（可用 `<b>`、`<span class="num">`）。

## EVENTS

```js
var EVENTS=[
 {d:'2026-10-03',t:'01:15',tz:8,label:'北京 → 曼谷 · VZ3719',sub:'大兴 PKX 起飞'}];
```

倒计时事件源。引擎取**当前时间之后最近的一个**显示在「此刻关注」。通常把航班起飞、
重要活动接车 / 开场都列入。`d` 完整日期、`tz` 为事件所在地时区。

## 地图地理数据

```js
var GEO_BK=[[[lng,lat], /* 闭合海岸线/轮廓环，首尾点相同 */]];
var GEO_PK=[ /* 可含多个环：主岸线 + 离岛 */ ];

var VIEW={
 bk:{W:1000,H:467,pad:30,latMin:13.726,latMax:13.767,lngMin:100.483,lngMax:100.580},
 pk:{W:760,H:1490,pad:22,latMin:7.755,latMax:8.215,lngMin:98.245,lngMax:98.475}};

var EDGE_OV={ bk:{DMK:[900,64],BKK:[905,300]}, pk:{mayabay:[668,1248]} };
var EDGE_DAY={ 3:{mayabay:1,courtyard:1} };
var RIVER=[[lat,lng], /* 河流折线 */];
var DASH=[6,7];

var BK_LINES=[
 {c:'var(--c1)',ids:['debtida','grandpalace','watpho','debtida']},
 {c:'var(--c2)',ids:['museumsiam','watpaknam'],dash:DASH}];
var PK_LINES=[ /* 同结构 */ ];

var AIRPORTS={BKK:1,DMK:1,HKT:1};
var HOTEL_COLOR={debtida:'var(--c1)',courtyard:'var(--c2)'};
var MINOR={spa:1,karon:1,chalong:1};

var LABEL_ADJ={ grandpalace:[-14,-4,'end'], /* 总览标签 [dx,dy,anchor] */ };
var DAY_LBL={ mgallery:[0,-12,'middle'], /* 当日图标签 */ };
var MFACT={ grandpalace:['建议 1.5–2 小时','门票 500 铢','08:30 开门'] };
```

- `GEO_*`：陆地 / 海岸线闭合环，坐标 `[lng,lat]`；可多环（主岸 + 离岛）。
- `VIEW`：每城画布 `W/H`、内边距 `pad`、经纬度取景范围。**新增城市照此加一组。**
- `EDGE_OV` / `EDGE_DAY`：离群点在图缘的固定像素坐标 `[x,y]`，用虚线引线（见 map_guide）。
- `RIVER`：河流折线（`[lat,lng]`，注意与 GEO 的 `[lng,lat]` 相反）。
- `DASH`：虚线 dasharray；`LINES[].dash` 可引用或自定义。
- `BK_LINES` / `PK_LINES`：总览路线，`c` 颜色、`ids` 按顺序连点、`dash` 可选（意向化段用虚线）。
- `MINOR`：不常驻文字标签的次要地点（点 marker 仍可点），用于减少遮挡。
- `LABEL_ADJ` / `DAY_LBL`：标签相对 marker 的偏移 `[dx,dy,anchor]`，anchor 取 `start`/`middle`/`end`。
- `MFACT`：地点快速事实 chips（门票、用时、开放时间等短词）。

## XHS_DATA

```js
var XHS_DATA={
 "grandpalace":[
  {"t":"scene","s":"构图描述","l":"https://www.xiaohongshu.com/explore/笔记id","i":"data:image/jpeg;base64,/9j/4AAQ…"},
  {"t":"person","s":"人物姿势描述","l":"https://www.xiaohongshu.com/explore/…","i":"data:image/jpeg;base64,…"}
 ],
 /* 每个景点 4 条：2 景 + 2 人 */
};
```

- key 为景点 PLACES key；`t` 取 `scene`（景色 / 机位）或 `person`（人物姿势）。
- `s` 中文描述、`l` 小红书原帖链接（点击「参考小红书」可直达）、`i` **内联 jpeg base64**（离线可看）。
- 这是数据文件体积的主要来源（图建议压缩到宽 ~700–900px、JPEG 质量 70–80）。
- 采集方式见 workflow；非景点（机场 / 餐厅 / 酒店 / SPA）不需要。

## WX_CITIES

```js
var WX_CITIES=[
 {key:'bkk',n:'曼谷',en:'Bangkok',lat:13.75,lng:100.50,tz:7,
  range:[new Date(2026,9,3),new Date(2026,9,4,20,45)],
  range2:[new Date(2026,9,7,23,35),new Date(2026,9,8,19,35)]},
 {key:'hkt',n:'普吉',en:'Phuket',lat:13/*应为普吉纬度~7.9*/,lng:98.34,tz:7,
  range:[new Date(2026,9,4,22,15),new Date(2026,9,7,22,5)]}];
```

天气城市。`range` 为在该城市的时间区间（`new Date(年,月-1,日,时,分)`），
引擎据此高亮「你在这里」；同一城市分段（如返程又回曼谷）用 `range2`。
天气由引擎调用 Open-Meteo（免费无 key），天气码翻译表 `WX_CODE` 在引擎内。

---

## 写作口径与红线

- **坐标必须准确**：每个地点用 Google Maps 逐一核对 lat/lng，错一个导航就错；填完抽查。
- 景点 `why`/`see` 要具体（年代、人物、建筑、藏品、数字），不写「非常美丽 / 值得一去」这类空话；参考权威资料与公开攻略。
- 时间安排以**已出票航班为锚**，并核对：景点闭馆日、节假日 / 周末售罄、需预约的免费点、各段车程 / 船程是否合理。
- 数字（门票、用时、车程）要有依据，不编造；不确定就标注或换确定的方案。
- **绝不写进页面**：确认号、证件号、护照号、票号、PNR、订单号、房间号、酒店电话；账号密码不写进数据文件或记忆。
- 页面保持终稿，无版本说明 / 修改日志。
