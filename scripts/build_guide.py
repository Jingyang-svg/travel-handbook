# -*- coding: utf-8 -*-
"""
build_guide.py — 把旅行数据注入引擎模板，产出单文件旅行手册 index.html

用法：
  python build_guide.py --template <template.html> --data <guide_data.js> --out <index.html>

数据文件 guide_data.js 内含全部行程变量（META / PLACES / DAYS / FLIGHTS /
HOTELS / EVENTS / TODO_GROUPS / TIPS / XHS_DATA 等），图片以 base64 内联其中。
模板里用占位注释 /*__GUIDE_DATA__*/ 标记注入位置。零第三方依赖。
"""
import argparse, io, os

PLACE = "/*__GUIDE_DATA__*/"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    tpl = io.open(a.template, encoding="utf-8").read()
    data = io.open(a.data, encoding="utf-8").read()
    if PLACE not in tpl:
        raise SystemExit("模板缺少注入占位 " + PLACE)
    out = tpl.replace(PLACE, data, 1)

    od = os.path.dirname(os.path.abspath(a.out))
    if od and not os.path.isdir(od):
        os.makedirs(od, exist_ok=True)
    io.open(a.out, "w", encoding="utf-8").write(out)
    print("built:", a.out, "| KB:", round(len(out.encode("utf-8"))/1024, 1))

if __name__ == "__main__":
    main()
