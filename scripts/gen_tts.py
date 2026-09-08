#!/usr/bin/env python3
"""为 arrows.html 的 81 个小图用 edge-tts 生成中文 TTS 音频。

音色：zh-CN-XiaoxiaoNeural（微软云希，最自然的中文女声之一）。
输出：../tts/<codepoint>.mp3

依赖：edge-tts（首次需 pip install edge-tts，使用 venv 或 --user）
"""
import asyncio
import os
import sys

import edge_tts

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-10%"  # 稍慢，便于小孩听清
PITCH = "+0Hz"

# 与 arrows.html 中 PETS 数组完全对应(20 车辆 + 16 水果 + 40 动物 + 5 甜点 = 81)
PETS = [
    # ---- 20 个工程车/交通工具(最先进入) ----
    ("1f69c", "拖拉机"),
    ("1f69a", "大卡车"),
    ("1f69b", "大货车"),
    ("1f68c", "公交车"),
    ("1f690", "小巴"),
    ("1f691", "救护车"),
    ("1f692", "消防车"),
    ("1f693", "警车"),
    ("1f695", "出租车"),
    ("1f697", "小汽车"),
    ("1f699", "越野车"),
    ("1f682", "小火车"),
    ("1f684", "高铁"),
    ("1f681", "直升机"),
    ("2708",  "大飞机"),
    ("1f680", "小火箭"),
    ("1f6a2", "大轮船"),
    ("26f5",  "小帆船"),
    ("1f3ce", "赛车"),
    ("1f3cd", "摩托车"),
    # ---- 16 种水果 ----
    ("1f34c", "香蕉"),
    ("1f34a", "橘子"),
    ("1f34b", "柠檬"),
    ("1f347", "葡萄"),
    ("1f349", "西瓜"),
    ("1f34d", "菠萝"),
    ("1f34e", "红苹果"),
    ("1f350", "大鸭梨"),
    ("1f351", "桃子"),
    ("1f352", "樱桃"),
    ("1f353", "草莓"),
    ("1f348", "哈密瓜"),
    ("1f96d", "大芒果"),
    ("1f965", "椰子"),
    ("1fad0", "蓝莓"),
    ("1f951", "牛油果"),
    # ---- 40 只小动物 ----
    ("1f436", "小狗"),
    ("1f431", "小猫"),
    ("1f430", "小兔子"),
    ("1f439", "小仓鼠"),
    ("1f42d", "小老鼠"),
    ("1f43b", "小熊"),
    ("1f43c", "大熊猫"),
    ("1f428", "小考拉"),
    ("1f42f", "小老虎"),
    ("1f981", "小狮子"),
    ("1f42e", "小牛"),
    ("1f437", "小猪"),
    ("1f435", "小猴子"),
    ("1f98a", "小狐狸"),
    ("1f992", "长颈鹿"),
    ("1f418", "大象"),
    ("1f993", "斑马"),
    ("1f998", "袋鼠"),
    ("1f414", "小鸡"),
    ("1f424", "小鸡"),
    ("1f425", "小鸡"),
    ("1f426", "小鸟"),
    ("1f427", "企鹅"),
    ("1f986", "小鸭子"),
    ("1f99a", "天鹅"),
    ("1f99b", "孔雀"),
    ("1f99c", "小鹦鹉"),
    ("1f989", "猫头鹰"),
    ("1f985", "老鹰"),
    ("1f413", "大公鸡"),
    ("1f42c", "小海豚"),
    ("1f433", "大鲸鱼"),
    ("1f420", "小鱼"),
    ("1f419", "章鱼"),
    ("1f422", "小乌龟"),
    ("1f41d", "小蜜蜂"),
    ("1f98b", "小蝴蝶"),
    ("1f984", "独角兽"),
    ("1f434", "小马"),
    ("1f411", "小绵羊"),
    # ---- 5 个甜点/小食(最后) ----
    ("1f366", "冰淇淋"),
    ("1f369", "甜甜圈"),
    ("1f36a", "棒棒糖"),
    ("1f36b", "巧克力"),
    ("1f33d", "玉米"),
]


async def gen(out_dir: str, code: str, text: str) -> str:
    out = os.path.join(out_dir, f"{code}.mp3")
    if os.path.exists(out) and not os.environ.get("FORCE"):
        return out  # 跳过已存在
    comm = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    await comm.save(out)
    return out


async def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "tts")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    sem = asyncio.Semaphore(4)  # 并发控制，避免触发限流

    async def run(item):
        async with sem:
            try:
                path = await gen(out_dir, *item)
                size = os.path.getsize(path)
                print(f"  ✓ {item[0]}.mp3  {size//1024} KB  \"{item[1]}\"")
            except Exception as e:
                print(f"  ✗ {item[0]}.mp3  FAILED: {e}", file=sys.stderr)

    await asyncio.gather(*[run(p) for p in PETS])
    print(f"\nDone. {len(PETS)} files in {out_dir}")


if __name__ == "__main__":
    asyncio.run(main())
