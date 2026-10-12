# -*- coding: utf-8 -*-
"""
verify_guide.py — 旅行手册双端自检（桌面 1440 / 手机 390）。
动态从数据里取第一个景点、城市列表与第一天，不写死 key，换旅行可直接跑。

用法：
  python verify_guide.py <构建站点目录>
  # 站点目录下需有 index.html；截图输出到 <站点>/_shots/

云端若 Playwright 浏览器装在用户目录，运行前带：
  PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/ms-pw python verify_guide.py <site>
"""
import os, sys
from playwright.sync_api import sync_playwright

SITE = sys.argv[1] if len(sys.argv) > 1 else "./site"
URL = "file://" + os.path.abspath(os.path.join(SITE, "index.html"))
SHOTS = os.path.abspath(os.path.join(SITE, "_shots"))
os.makedirs(SHOTS, exist_ok=True)

# 页面里动态定位：第一个景点（CAT 未覆盖）、城市、第一天
LOCATE = r"""()=>({
  sight:(function(){var ks=Object.keys(PLACES);
    for(var i=0;i<ks.length;i++){if(!CAT[ks[i]])return ks[i];}return ks[0];})(),
  cities:Object.keys(VIEW),
  day1:DAYS[0].no
})"""

def run(vp, tag):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport=vp)
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.goto(URL)
        pg.wait_for_timeout(3500)  # 等天气 fetch

        loc = pg.evaluate(LOCATE)
        sight, cities, day1 = loc["sight"], loc["cities"], loc["day1"]

        info = pg.evaluate(r"""(s)=>({
          title: document.getElementById('hk-title').innerHTML,
          doc: document.title,
          footer: document.getElementById('hk-footer').innerHTML,
          map: document.querySelectorAll('#overview-map svg').length,
          days: document.querySelectorAll('.day').length,
          openDays: document.querySelectorAll('.day.open').length,
          confirmed: document.getElementById('confirmed').innerHTML.length,
          todos: document.getElementById('todos').innerHTML.length,
          tips: document.getElementById('tips').innerHTML.length,
          navUrl: navUrl(s),
          multi: multiNav(DAYS[0].route).slice(0,60)
        })""", sight)

        # 弹窗
        pg.evaluate("openModal('%s')" % sight); pg.wait_for_timeout(400)
        modal = pg.evaluate(r"""()=>{const m=document.getElementById('modal');
          return {disp:getComputedStyle(document.getElementById('modal-mask')).display,
                  why:/为什么|值得/.test(m.innerHTML), len:m.innerHTML.length};}""")
        pg.locator("#modal").screenshot(path=os.path.join(SHOTS, tag+"_modal.png"))
        pg.evaluate("closeModal()")

        # 倒计时：注入未来事件，读两次确认秒数跳动
        cd1 = pg.evaluate(r"""()=>{CUR_NX={dt:new Date(Date.now()+90061000),e:{label:'测试',sub:''}};
          var root=document.getElementById('now');
          if(!root.querySelector('.countdown')){var d=document.createElement('div');d.className='countdown';
            root.insertBefore(d,root.querySelector('.now-todo'));}
          paintCd();return root.querySelector('.countdown').textContent;}""")
        pg.wait_for_timeout(1100)
        cd2 = pg.evaluate("document.querySelector('#now .countdown').textContent")

        pg.locator(".hero").screenshot(path=os.path.join(SHOTS, tag+"_hero.png"))
        pg.locator("#now").screenshot(path=os.path.join(SHOTS, tag+"_now.png"))

        # 逐城总览地图
        for c in cities:
            tab = pg.locator('.map-tab[data-city="%s"]' % c)
            if tab.count():
                tab.first.click(); pg.wait_for_timeout(450)
            pg.locator("#overview-map").screenshot(path=os.path.join(SHOTS, tag+"_map_"+c+".png"))

        # 第一天当日路线图
        pg.locator('.day[data-day="%s"] .day-head' % day1).click(); pg.wait_for_timeout(300)
        pg.locator('.day[data-day="%s"] [data-daymap]' % day1).click(); pg.wait_for_timeout(900)
        pg.locator('.day[data-day="%s"] .day-map' % day1).screenshot(
            path=os.path.join(SHOTS, tag+"_daymap.png"))
        b.close()

    print("== %s %s ==" % (tag, vp["width"]))
    print("  console errors:", errs if errs else "NONE")
    print("  sight:", sight, "| cities:", cities)
    print("  META title:", info["title"][:30], "| doc:", info["doc"][:30])
    print("  map svg:", info["map"], "| days:", info["days"], "| open(now):", info["openDays"])
    print("  confirmed/todos/tips >0:", info["confirmed"] > 0, info["todos"] > 0, info["tips"] > 0)
    print("  nav url:", info["navUrl"])
    print("  modal:", modal["disp"], "why?", modal["why"], "len", modal["len"])
    print("  countdown tick:", repr(cd1), "->", repr(cd2), "| changed:", cd1 != cd2)
    ok = (not errs) and info["map"] >= 1 and info["days"] >= 1 and modal["disp"] != "none" \
          and modal["why"] and cd1 != cd2 and info["confirmed"] > 0
    print("  RESULT:", "PASS" if ok else "FAIL")
    return ok

r1 = run({"width": 1440, "height": 900}, "desktop")
r2 = run({"width": 390, "height": 844}, "mobile")
print("GUIDE VERIFY:", "PASS" if (r1 and r2) else "FAIL")
sys.exit(0 if (r1 and r2) else 1)
