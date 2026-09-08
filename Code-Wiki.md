# kids-keyboard-game — Code Wiki

> 自动生成于 2026-09-07,基于仓库快照;运行命令均以项目根目录为 cwd。

## 1. 项目概览

- **定位**:面向 0~5 岁小朋友的极简网页小游戏集合;两个独立 HTML 游戏,纯键盘操作、全屏、零运行时依赖、所有资源本地。
- **主要功能**:
  - `index.html`:键盘反应游戏。26 个字母键调用 `SpeechSynthesisUtterance` 念出英文发音,方向键/空格播放 WebAudio 合成的随机音符(C 大调音阶 + 6 种音色);每次按键从屏幕中心炸开 6 波 emoji(共 ~24 个),背景切换柔和色。
  - `arrows.html`:图像切换游戏。首次空格/回车/→ 进入全屏(`requestFullscreen`,**不再调用 `keyboard.lock`**,以保证 Esc 能正常退出全屏),Esc 退出全屏;**↑/↓ 切类(工程车/水果/动物/甜点),←/→ 切图**(在当前类内循环),空/回车 = →。81 张图:车辆/动物/甜点用 Twemoji SVG;**水果 16 张改用 Microsoft Fluent Emoji Color SVG(MIT,viewBox 0 0 32 32,任意尺寸不糊)**,路径写死到 `PETS[i].img`,`showCurrent` 优先用 `img` 否则回退 `emojis/<id>.svg`。
- **技术栈**:HTML5 + 原生 JS(ES5 IIFE 风格) + CSS 关键帧 + WebAudio API + `SpeechSynthesis` API + `edge-tts`(Python,仅用于一次性预生成中文音频)。
- **仓库入口**:`index.html`(主)、`arrows.html`(副);离线资源目录 `emojis/`(371 个 SVG)、`imgs/fruits/`(16 个 SVG)、`tts/`(81 个 mp3)。

## 2. 整体架构

两个游戏各自独立,完全无共享 JS/CSS 模块,仅共享资源目录 `emojis/` 与 `tts/`。

```
[ 浏览器 ]
  ├── index.html  ── 内联 <style> + 内联 <script>(IIFE)
  │     ├── WebAudio(音符合成)
  │     ├── SpeechSynthesis(字母发音)
  │     └── emojis/*.svg(喷发动画)
  │
  └── arrows.html ── 内联 <style> + 内联 <script>(IIFE)
        ├── <audio>(预生成中文 mp3)
        ├── emojis/*.svg(动物 + 星星)
        └── tts/*.mp3(动物名发音)

[ 构建/资源生成 ]
  └── scripts/gen_tts.py  ── edge-tts → tts/<codepoint>.mp3
```

- **进程/线程模型**:无后台进程,纯单页浏览器;音频节点在 `AudioContext` 上临时创建/销毁;TTS 句柄随事件触发即用即弃。
- **数据流**:按键事件 → 校验白名单 → 触发音效/语音/视觉反馈 → 立即返回。无状态持久化(刷新即重置)。

## 3. 主要模块

### 3.1 `index.html` — 小小键盘乐园(键盘学习)

- **路径**:`/index.html`(单文件,~355 行,内联 CSS + 内联 JS)
- **职责**:捕获所有键盘事件并产生即时多模态反馈(语音 + 音符 + emoji 喷射 + 背景换色 + 中央大字符)。
- **关键函数**:
  - `ensureAudio()`:懒创建 `AudioContext`,处理 `suspended` 恢复。
  - `playNote()`:从 10 个 C 大调频率中随机抽一个,再从 6 种合成音色中随机一种(sine/triangle/square/sawtooth + 滑音/双音)。
  - `tone(type, freqStart, freqEnd, startTime, duration, volume)`:WebAudio 振荡器封装,支持指数滑音与衰减包络。
  - `pickVoice()`:从 `speechSynthesis.getVoices()` 按优先级匹配 macOS 高品质人声(Zoe/Ava/Evan/Nathan/Samantha)→ Google US English → Microsoft → 任意 `en-US`;`onvoiceschanged` 时重选。
  - `speakLetter(letter)`:用 `SpeechSynthesisUtterance` 念单字母,`cancel()` 防止连按堆积。
  - `spawnEmoji()` / `emitWave(count, maxDist)`:6 波递减喷射,`setTimeout` 调度波间间隔。
  - `emojiFile(emoji)`:codepoint → `emojis/<hex>.svg` 文件名,过滤 FE0F 变体选择符。
  - `changeBackground()` / `showChar(key)`:CSS 过渡切换背景;`#bigChar` 通过 `void el.offsetWidth` 重启动画。
  - `goFullscreen()`:全屏 API + `navigator.keyboard.lock()`(Chrome/Edge),用于连 Esc 也由页面接管。
- **依赖**:浏览器原生 API(`AudioContext`/`speechSynthesis`/`requestFullscreen`/`keyboard.lock`),`emojis/`。

### 3.2 `arrows.html` — 小动物乐园(图像切换)

- **路径**:`/arrows.html`(单文件,内联 CSS + 内联 JS)
- **职责**:维护 `catIdx` + `itemIdx`,首次按键进入全屏,之后按 **↑/↓** 切类(工程车/水果/动物/甜点)、**←/→** 在类内切图,空/回车 = →;Esc 退出全屏。
- **关键数据结构**:
  - `PETS`:81 项 `[{id, name}]` 数组,`id` 为 emoji codepoint hex,`name` 为中文显示名;**进入顺序**:20 车辆/工程车(挖掘机用 🚜 1f69c 拖拉机代替)→ 16 水果(无榴莲/山竹/荔枝/火龙果/百香果,补 🥑 1f951 牛油果)→ 40 动物 → 5 甜点小食;默认起点为 `1f69c 拖拉机`。
  - `CATS`:`[{label, start, len}]` 描述 4 段边界(0/20, 20/16, 36/40, 76/5),与 `PETS` 顺序必须保持同步。
  - `SPARKS`:7 个固定 codepoint(`2b50` ⭐、`1f31f` 🌟、`2728` ✨、`1f496` 💖、`1f308` 🌈、`1f388` 🎈、`1f36a` 🍭)。
- **关键函数**:
  - `goFullscreen()`:`requestFullscreen`(只调一次,**不调 `navigator.keyboard.lock`**,因为它会让 Esc 失灵)。
  - `exitFullscreen()`:若 `document.fullscreenElement` 存在则 `exitFullscreen()`,供 Esc 显式调用。
  - `start()`:`started = true` + 移除 `#hint` 提示 + `goFullscreen()`;幂等。
  - `speakName(idx)`:单 `<audio>` 元素复用,`pause() + currentTime=0 + src=` 防重叠。
  - `spawnSparks()`:在屏幕中心 ±266 px 范围随机位置撒 4 颗 426 px 星星,1 秒后 `remove()`。
  - `showCurrent()`:用 `CATS[catIdx].start + itemIdx` 索引 `PETS`,刷图 + bounce + sparks + TTS。
  - `goNext()` / `goPrev()`:在当前 `CATS[catIdx].len` 内 `itemIdx` 循环。
  - `changeCategory(delta)`:`catIdx` 循环(包头包尾),`itemIdx` 归 0。
  - keydown:**Space/Enter/→** → `goNext()`;**←** → `goPrev()`;**↓/↑** → `changeCategory(±1)`;**Esc** → `exitFullscreen()`;首次按方向键也走 `start()`。其余按键丢弃。
  - `beforeunload`:`started=true` 时拦截误关。
- **依赖**:浏览器原生 `<audio>`;`emojis/`、`tts/`。

### 3.3 `scripts/gen_tts.py` — 中文 TTS 预生成器

- **路径**:`/scripts/gen_tts.py`(Python 3)
- **职责**:用 `edge-tts` 调用微软云希 `zh-CN-XiaoxiaoNeural`,为 `arrows.html` 的 81 项生成 mp3(20 车辆 + 16 水果 + 40 动物 + 5 甜点);输出到 `../tts/<codepoint>.mp3`。
- **关键函数**:
  - `gen(out_dir, code, text)`:幂等生成(已存在且未设 `FORCE` 环境变量则跳过)。
  - `main()`:`asyncio.gather` + `Semaphore(4)` 控制并发(避免触发限流);每只动物打印 `KB` 大小或失败原因。
- **依赖**:`edge-tts`(运行时安装,非项目内依赖,见 README venv 步骤);与 `arrows.html` 的 `PETS` 列表需保持完全一致(注释里明确标注)。

### 3.4 `emojis/` — Twemoji 矢量资源

- **路径**:`/emojis/`(371 个 `.svg` 文件,单文件通常 < 10 KB)
- **职责**:被 `index.html`(emoji 喷射)与 `arrows.html`(动物图 + 星星)共同引用;文件名格式 `<codepoint>.svg`,支持 `1f436-1f431.svg` 多 codepoint 组合(emojiFile 已过滤 FE0F)。
- **来源/许可**:Twemoji (X Corp),CC-BY 4.0(README 注明)。
- **依赖**:无(纯静态资产)。

### 3.5 `imgs/fruits/` — Fluent Emoji Color SVG 水果素材

- **路径**:`/imgs/fruits/`(16 个 `.svg`,viewBox 0 0 32 32,合计 ~140 KB)
- **职责**:`arrows.html` 的水果段用 `PETS[i].img` 引用本地 SVG,矢量缩放不糊(比 3D PNG 在 1066px 全屏下更清晰);其余段继续用 Twemoji SVG。
- **依赖**:由 `scripts/download_fruits_3d.py` 从 [microsoft/fluentui-emoji](https://github.com/microsoft/fluentui-emoji)(MIT) 一次性下载。注:Fluent Emoji 没有 Orange 水果条目,用 Tangerine 代替显示为「橘子」。
- **许可**:MIT(微软),允许商用,需保留版权。

### 3.6 `tts/` — 预生成中文音频

- **路径**:`/tts/`(81 个 `.mp3`,与 `PETS` 一一对应)
- **职责**:`arrows.html` 通过 `<audio src="tts/<id>.mp3">` 直接播放;离线可用,不依赖系统 TTS 引擎。
- **依赖**:由 `scripts/gen_tts.py` 产出。

## 4. 关键类与函数

跨模块入口/协议/状态机:

- **全局键盘捕获协议**(`index.html`):所有按键一律 `e.preventDefault()`,按白名单(`/^[a-zA-Z]$/`、`ArrowUp|Down|Left|Right`、`Space`)决定是否触发反馈;Esc 仅用于退出全屏;`e.repeat` 与 50 ms 去抖过滤。
- **生命周期状态机**(`index.html`):`started = false`(初始) → 首次白名单按键 → `started = true` + `goFullscreen()` + 移除 `#welcome` 提示;`beforeunload` 在 `started=true` 时拦截误关。
- **资源命名协议**:`emoji` codepoint → `emojis/<hex>.svg`(过滤 FE0F);`PETS` 项 id → `tts/<id>.mp3` + `emojis/<id>.svg`,两套资源同 codepoint 命名,通过 `PETS` 数组绑定;`gen_tts.py` 的 `PETS` 列表与 `arrows.html` 严格同步,任何新增需同时改两处。
- **常量/枚举**:
  - `EMOJIS`(`index.html`):~250 个 emoji 字符的喷发池(动物/食物/自然/交通/音乐/表情)。
  - `COLORS`(`index.html`):10 个柔和背景色 hex。
  - `NOTES`(`index.html`):C4 大调 10 个频率 `[262, 294, 330, 349, 392, 440, 494, 523, 587, 659]` Hz。
  - `VOICE / RATE / PITCH`(`gen_tts.py`):`zh-CN-XiaoxiaoNeural`、`-10%` 语速、`+0Hz` 音调。

## 5. 依赖关系

### 5.1 浏览器运行时

- 零 npm 依赖;仅依赖浏览器原生 API:
  - `AudioContext` / `webkitAudioContext`
  - `SpeechSynthesis` / `SpeechSynthesisUtterance`
  - `Element.requestFullscreen`
  - `Navigator.keyboard.lock`(Chrome/Edge 专属,失败静默 catch)
- 跨浏览器/平台差异:
  - macOS 自带 Samantha/Zoe/Ava 等高品质英语人声;Windows/ChromeOS 退化为 Google/Microsoft 网络语音;移动端可能没有 `keyboard.lock`。

### 5.2 Python 依赖(仅用于一次性预生成 TTS)

- `edge-tts`:运行时通过 `pip install edge-tts` 安装,推荐 `python3 -m venv /tmp/tts-venv`(README 写法)。
- Python 标准库:`asyncio`、`os`、`sys`。

### 5.3 静态资源依赖

- `emojis/`:Twemoji CC-BY 4.0,371 个 SVG。
- `tts/`:由 `gen_tts.py` 产出,81 个 mp3。

### 5.4 构建/工具链

- 无 `package.json`、`build.gradle`、`Cargo.toml`;不需要 npm/Gradle/Cargo。
- 运行:浏览器直接打开 HTML,或起静态服务(`python3 -m http.server 8000`,README 推荐)。

## 6. 项目运行方式

> 仅引用 `README.md` 中已声明的命令,不编造。

### 6.1 直接打开(最简)

```bash
open index.html          # macOS · 小小键盘乐园(2~5 岁)
open arrows.html         # macOS · 小动物乐园(0~3 岁)
```

### 6.2 启动本地静态服务

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

### 6.3 重新生成中文 TTS(可选)

```bash
python3 -m venv /tmp/tts-venv && /tmp/tts-venv/bin/pip install edge-tts
/tmp/tts-venv/bin/python scripts/gen_tts.py
```

### 6.4 关键配置/约束

- `tts/` 内 mp3 已预生成且覆盖 `arrows.html` 全部 81 项(动物/车辆/水果/甜点);`gen_tts.py` 默认跳过已存在文件(除非设置环境变量 `FORCE`)。
- 全屏体验建议使用 Chrome / Edge(支持 `keyboard.lock`);`Esc` 在游戏内仅退出全屏,不退出页面;`Cmd+Tab`/`Cmd+Q` 等 macOS 系统快捷键**无法被网页拦截**(README 已标注)。

## 7. 约定与备注

### 7.1 命名规范

- 文件:全小写,带连字符或点(如 `index.html`、`gen_tts.py`)。
- emoji 资源:`<codepoint-hex>.svg`,多 codepoint 用 `-` 连接,过滤 FE0F(`emojiFile` 内置)。
- 动物 id 与 `tts/` mp3 名严格一致,均由 `gen_tts.py` 的 `PETS` 元组决定。
- JS 内联:全部 IIFE、`"use strict"`、ES5 风格(`var`/`function`,无 ES6 class),保持单文件零构建。

### 7.2 重要约束

- 全键盘捕获:`e.preventDefault()` 在 keydown 入口无条件调用,任何按键都不会触发浏览器默认行为(返回/前进/搜索/F5 等)。
- 平台差异:`keyboard.lock` 仅 Chrome/Edge 支持,失败被静默吞掉;`speechSynthesis.getVoices()` 在部分平台异步返回,代码已通过 `onvoiceschanged` 重选。
- 安全边界:右键菜单 `contextmenu` 被 `preventDefault`;`beforeunload` 在游戏开始后才拦截,首次进入页面的刷新不会被拦截。
- 零运行时依赖意味着:任何依赖升级(比如换浏览器引擎)都需要手动验证 `keyboard.lock` / TTS 声音可用性,无构建系统兜底。

### 7.3 已知风险或遗留事项

- macOS 系统级快捷键(`Cmd+Tab`/`Cmd+Q`/`Cmd+空格`)无法拦截,README 建议必要时改用 Chrome `--kiosk` 模式。
- `arrows.html` 的 `tts/` 与 `gen_tts.py` 的 `PETS` 是手工同步的两份列表,新增项时需同时改两处(README/`gen_tts.py` 顶部注释已注明)。
- 预生成 mp3 命名与 `arrows.html` 的 `PETS[].id` 一一对应;若改名需同时删除/重建 `tts/<old>.mp3`。
- 无单元测试、无 CI、无 lint 配置;改动需人工跑 `python3 -m http.server` 验证两个页面在主流浏览器(尤其 Chrome/Edge)的全屏 + 键盘锁定体验。
- `emojis/` 体积未追踪,新增 SVG 时需关注首屏加载(尤其 `index.html` 一次性喷射 24 个 SVG)。
