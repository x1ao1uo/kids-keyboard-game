#!/usr/bin/env python3
"""从 microsoft/fluentui-emoji 下载 16 种水果的 Color SVG 到 imgs/fruits/。

许可:MIT (microsoft/fluentui-emoji)
仓库:https://github.com/microsoft/fluentui-emoji
路径:assets/<Fruit Folder>/Color/<name>_color.svg  (矢量,viewBox 0 0 32 32,任意尺寸不糊)
注:Fluent Emoji 没有 Orange 水果条目,用 Tangerine 代替(中文「橘子」对应)
"""
import os
import sys
import urllib.error
import urllib.request

# (本地 slug, GitHub 资产目录名, 输出文件名)
FRUITS = [
    ("banana",      "Banana",      "banana_color.svg"),
    ("orange",      "Tangerine",   "tangerine_color.svg"),
    ("lemon",       "Lemon",       "lemon_color.svg"),
    ("grape",       "Grapes",      "grapes_color.svg"),
    ("watermelon",  "Watermelon",  "watermelon_color.svg"),
    ("pineapple",   "Pineapple",   "pineapple_color.svg"),
    ("apple",       "Red apple",   "red_apple_color.svg"),
    ("pear",        "Pear",        "pear_color.svg"),
    ("peach",       "Peach",       "peach_color.svg"),
    ("cherry",      "Cherries",    "cherries_color.svg"),
    ("strawberry",  "Strawberry",  "strawberry_color.svg"),
    ("cantaloupe",  "Melon",       "melon_color.svg"),
    ("mango",       "Mango",       "mango_color.svg"),
    ("coconut",     "Coconut",     "coconut_color.svg"),
    ("blueberry",   "Blueberries", "blueberries_color.svg"),
    ("avocado",     "Avocado",     "avocado_color.svg"),
]

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "imgs", "fruits")
BASE = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/"
UA = "Mozilla/5.0"


def log(m):
    print(m, flush=True)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log(f"输出: {OUT_DIR}")
    log(f"待下载: {len(FRUITS)} 张 Color SVG (Fluent Emoji, MIT)")
    ok, miss = [], []
    for slug, folder, fname in FRUITS:
        out = os.path.join(OUT_DIR, slug + ".svg")
        if os.path.exists(out) and os.path.getsize(out) > 200:
            log(f"  ✓ {slug}.svg  (已存在 {os.path.getsize(out)//1024} KB)")
            ok.append(slug)
            continue
        url = BASE + folder.replace(" ", "%20") + "/Color/" + fname
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                ct = r.headers.get("Content-Type", "")
                data = r.read()
            if len(data) < 200 or "svg" not in ct:
                log(f"  ✗ {slug}.svg  非 SVG ({len(data)}B, {ct})")
                miss.append(slug)
                continue
            with open(out, "wb") as f:
                f.write(data)
            log(f"  ✓ {slug}.svg  {len(data)//1024} KB  ({folder}/Color/{fname})")
            ok.append(slug)
        except urllib.error.HTTPError as e:
            log(f"  ✗ {slug}.svg  HTTP {e.code}  ({folder}/Color/{fname})")
            miss.append(slug)
        except Exception as e:
            log(f"  ✗ {slug}.svg  {e}  ({folder}/Color/{fname})")
            miss.append(slug)
    log("")
    log(f"汇总:{len(ok)}/{len(FRUITS)} 成功")
    if miss:
        log(f"失败: {miss}")
        sys.exit(1)


if __name__ == "__main__":
    main()
