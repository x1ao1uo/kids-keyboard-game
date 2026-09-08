# 小小键盘乐园（kids-keyboard-game）

面向 0~5 岁小朋友的极简网页小游戏集合：纯键盘操作、全屏、零依赖、所有资源本地。

## 游戏

### 1. `index.html` — 小小键盘乐园（2~5 岁）

- 有反应的按键只有：**26 个字母键、方向键（↑↓←→）、空格键**
  - 字母键：英语语音朗读该字母（自动选用系统最高品质语音）
  - 方向键、空格：播放随机音符（6 种音色轮换）
  - 三者都会让 emoji 从屏幕中心喷涌而出、停留片刻后慢慢消散，背景切换柔和颜色
  - 字母键同时在屏幕中央显示大号字符（认字启蒙）
- 其余所有按键一律被捕获并禁用，不会产生任何反应，也不会触发浏览器操作
- 首次按键自动进入全屏（Chrome/Edge 下通过 Keyboard Lock 连 Esc 也由页面接管）
- 游戏开始后误关标签页会被拦截确认；右键菜单已禁用
- 家长按 `Esc` 退出全屏结束游戏

### 2. `arrows.html` — 小动物乐园（0~3 岁）

- 屏幕中央固定显示一只超大的可爱小图（默认 🚜 拖拉机）
- 首次按 **空格** / **回车** / **→** 自动进入全屏；之后任意时刻按 **Esc** 退出全屏
- 之后每按一次切换小图（共 **81** 张，进入顺序 4 段，可按 **↑/↓** 切段、**←/→** 切图）：
  - **① 工程车/交通工具 20 个**（最先进入，默认起点）：Twemoji SVG
  - **② 水果 16 种**：[Microsoft Fluent Emoji Color](https://github.com/microsoft/fluentui-emoji) SVG（MIT 许可，矢量，viewBox 0 0 32 32，任意尺寸不糊，比 3D PNG 更清晰）：香蕉/橘子（Fluent Emoji 没有 Orange，用 Tangerine 代替）/柠檬/葡萄/西瓜/菠萝/红苹果/大鸭梨/桃子/樱桃/草莓/哈密瓜/大芒果/椰子/蓝莓/牛油果
  - **③ 小动物 40 只**：Twemoji SVG
  - **④ 甜点小食 5 个**（最后）：Twemoji SVG：冰淇淋/甜甜圈/棒棒糖/巧克力/玉米
  - 切换时同时播放对应的中文音频念出名字
- 按键映射：**空格/回车/→** 下一张 ｜ **←** 上一张 ｜ **↑/↓** 上一类/下一类 ｜ **Esc** 退出全屏
- 切换时：图像原地放大轻跳 + 从中心炸开一波彩色星星
- 所有图像都是仓库 `emojis/` 下原版 Twemoji 矢量 SVG，**超高清**且**离线**可用
- 中文音频为 `tts/` 目录下的 mp3（用 `edge-tts` + 微软云希 `zh-CN-XiaoxiaoNeural` 预生成），音色统一自然，浏览器原生 `<audio>` 播放，**离线**、不依赖系统 TTS 引擎
- 注：Unicode 暂无“挖掘机”/“榴莲”/“山竹”/“荔枝”/“火龙果”/“百香果”emoji。挖掘机用 🚜 拖拉机代替；榴莲等热带水果以 🥑 牛油果 / 🥭 芒果 / 🥥 椰子 / 🥝 猕猴桃 等覆盖

> 重新生成中文音频：
> ```bash
> python3 -m venv /tmp/tts-venv && /tmp/tts-venv/bin/pip install edge-tts
> /tmp/tts-venv/bin/python scripts/gen_tts.py
> ```
>
> 重新下载水果 3D 素材(从 microsoft/fluentui-emoji,需要联网):
> ```bash
> python3 scripts/download_fruits_3d.py
> ```
- 其余按键一律被拦截，右键菜单与误关标签页也被拦下

> 注意：`Cmd+Tab`、`Cmd+Q`、`Cmd+空格` 等 macOS 系统级快捷键任何网页都无法拦截，
> 如需彻底防切走，可在系统设置中临时关闭这些快捷键，或使用 Chrome 的 `--kiosk` 模式启动。

## 运行

直接用浏览器打开对应页面即可：

```bash
open index.html          # macOS  · 小小键盘乐园（2~5 岁）
open arrows.html         # macOS  · 小动物跑跑跑（0~3 岁）
```

或起一个本地服务：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

所有资源（含 `emojis/` 目录下 371 个 SVG、`imgs/fruits/` 目录下 16 张 SVG）均为本地文件，离线可玩。

## 资源与许可

- `emojis/` 目录中的图形来自 [Twemoji](https://github.com/jdecked/twemoji),版权归 X Corp（原 Twitter）所有,以 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可使用。
- `imgs/fruits/` 目录的水果 3D 图像来自 [microsoft/fluentui-emoji](https://github.com/microsoft/fluentui-emoji),以 [MIT License](https://github.com/microsoft/fluentui-emoji/blob/main/LICENSE) 许可使用。
