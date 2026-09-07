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

- 屏幕中央固定显示一只超大的小动物（默认小鸡 🐥）
- 按 **空格** 或 **回车** 切换动物（共 40 只超高清 Twemoji 矢量图：小狗/小猫/小兔子/小熊/大熊猫/小考拉/小老虎/小狮子/小牛/小猪/小猴子/小狐狸/长颈鹿/大象/斑马/袋鼠/小鸡/小鸟/企鹅/小鸭子/天鹅/孔雀/小鹦鹉/猫头鹰/老鹰/大公鸡/小海豚/大鲸鱼/小鱼/章鱼/小乌龟/小蜜蜂/小蝴蝶/独角兽/小马/小绵羊…… 循环切换）；同时播放对应的中文音频念出动物名
- 切换时：动物原地放大轻跳 + 从中心炸开一波彩色星星
- 所有动物 emoji 都是仓库 `emojis/` 下原版 Twemoji 矢量 SVG，**超高清**且**离线**可用
- 中文音频为 `tts/` 目录下的 mp3（用 `edge-tts` + 微软云希 `zh-CN-XiaoxiaoNeural` 预生成），音色统一自然，浏览器原生 `<audio>` 播放，**离线**、不依赖系统 TTS 引擎

> 重新生成中文音频：
> ```bash
> python3 -m venv /tmp/tts-venv && /tmp/tts-venv/bin/pip install edge-tts
> /tmp/tts-venv/bin/python scripts/gen_tts.py
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

所有资源（含 `emojis/` 目录下 371 个 SVG）均为本地文件，离线可玩。

## 资源与许可

`emojis/` 目录中的图形来自 [Twemoji](https://github.com/jdecked/twemoji)，
版权归 X Corp（原 Twitter）所有，以 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可使用。
