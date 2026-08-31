# 小小键盘乐园（kids-keyboard-game）

面向 2~5 岁小朋友的极简网页小游戏：纯键盘操作、全屏、零依赖。

## 玩法

- 按键盘上**任意键**：
  - 随机位置弹出可爱 emoji（本地 Twemoji SVG 矢量图，任意大小都清晰）
  - 背景切换柔和颜色
  - 播放一个清脆的音符（C 大调音阶随机，6 种音色轮换）
  - 按字母/数字键时屏幕中央显示大号字符（认字启蒙）
- 首次按键自动进入全屏
- 家长按 `Esc` 退出全屏结束游戏

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
