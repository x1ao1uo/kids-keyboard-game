# 小小键盘乐园（kids-keyboard-game）

面向 2~5 岁小朋友的极简网页小游戏：纯键盘操作、全屏、零依赖。

## 玩法

- 有反应的按键只有：**26 个字母键、方向键（↑↓←→）、空格键**
  - 字母键：英语语音朗读该字母（自动选用系统最高品质语音）
  - 方向键、空格：播放随机音符（6 种音色轮换）
  - 三者都会让 emoji 从屏幕中心喷涌而出、停留片刻后慢慢消散，背景切换柔和颜色
  - 字母键同时在屏幕中央显示大号字符（认字启蒙）
- 其余所有按键一律被捕获并禁用，不会产生任何反应，也不会触发浏览器操作
- 首次按键自动进入全屏（Chrome/Edge 下通过 Keyboard Lock 连 Esc 也由页面接管）
- 游戏开始后误关标签页会被拦截确认；右键菜单已禁用
- 家长按 `Esc` 退出全屏结束游戏

> 注意：`Cmd+Tab`、`Cmd+Q`、`Cmd+空格` 等 macOS 系统级快捷键任何网页都无法拦截，
> 如需彻底防切走，可在系统设置中临时关闭这些快捷键，或使用 Chrome 的 `--kiosk` 模式启动。

## 运行

直接用浏览器打开 `index.html` 即可：

```bash
open index.html          # macOS
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
