# 贾维斯全息核心（示例）

1920×1080、单文件、零外部依赖。径向构图：中央三层球壳共 5,600 粒子，叠球面经纬网格、白核与十字光芒、纵向能量柱；三段弧反向缓转、弧上带扫描头，一条 6.6 秒一轮的扫描切面。外围七块数据模块铺满四边，球体包围盒内零文字。

双语在运行时切换：`?lang=zh` / `?lang=en`，不带参数时按系统语言（`navigator.language`）自动选择，行为与 `scripts/detect-language.sh` 的口径一致。

窗口小于 1920×1080 时页面整体等比缩放（`zoom`），避免右上角时间与右侧面板被窗口边缘裁掉；在 1920×1080 下缩放系数为 1，出图不受影响。

## 文件

- `hero.html`：全部内容（布局、粒子、双语字典、动效）。
- `screenshots/jarvis-1920x1080-zh.png` / `-en.png`：两版成图。
- `screenshots/jarvis-25pct.png`：25% 缩略，用于多尺度验收。

## 出图

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1920,1080 --force-device-scale-factor=1 \
  --virtual-time-budget=1600 \
  --screenshot=screenshots/jarvis-1920x1080-zh.png "file://$PWD/hero.html?lang=zh"
sips -z 270 480 screenshots/jarvis-1920x1080-zh.png --out screenshots/jarvis-25pct.png
```

`--virtual-time-budget` 不能省：这是动画画面，不给虚拟时间预算，无头浏览器会拍到第一帧——粒子还没散开、弧还在起始角，出来的图是死的。

## 动效清单（并发 3，符合技能上限）

| 元素 | 类型 | 周期 / 参数 |
|---|---|---|
| 粒子球 | 常态呼吸 | 自转 0.28 rad/s，半径脉动 ±2.4%，经纬网格随球同步转 |
| 三段弧 | 常态呼吸 | 0.055 / −0.042 / 0.030 rad/s，互相反向；弧上扫描头 15 秒一轮 |
| 扫描切面 | 常态呼吸 | 6.6 秒往返一次，切到的粒子轻提亮（1.35×），不做频闪 |
| 强调 | 无 | 核心亮度恒定，画面内不放大动效，保持「活着但不吵」 |

## 信息模块（七块）

| 位置 | 模块 | 内容 |
|---|---|---|
| 左上 | 品牌区 | 标题、副标、状态、会话/模式/运行时长 |
| 左上 | 模块状态 | 6 行：语音模型、语义内核、内存总线、热管理、视觉、执行器（含 1 条琥珀告警） |
| 右上 | 顶栏读数 | 链路、时延、温度、负载、能源、线程 |
| 右上 | 语音频谱 | 24 根柱 + 带轴 + 信噪比/语音/字错率/语言 |
| 左下 | 四环表 | 算力、内存、语音、能源 + 总线/电流/风扇/主频 |
| 右下 | 系统日志 | 7 条带时间戳与模块标签，1 条告警 |
| 底栏 | 链路参数 | 输入、底噪、同步、位深、编码 |

告警只出现在「热管理回路」与「热余量」两处，颜色 + 文字双编码，不用红色填充。

## 改文案的边界

- 机器标识不翻译：`JARVIS`、`v4.2`、`°C`、`kHz` 之类保持一致。
- 单位跟语言走：中文用「转/分、帧/秒、千赫、分贝、毫秒」，英文用 `RPM`、`FPS`、`kHz`、`dB`、`MS`。
- 一屏只允许一种自然语言；混排只留机器标识。
- 不使用电影台词与角色视觉（头盔、厂牌标识）。这里是通用的 AI 核心界面，不是某部作品的复刻。

## 抖音成片（10 秒 / 竖屏）

| 文件 | 规格 | 用途 |
|---|---|---|
| `jarvis-douyin-1080x1920.mp4` | 1080×1920 / 60fps / 10.0s / AAC 立体声 / 4.8 MB | 直接投抖音、视频号 |
| `jarvis-master-1920x1080.mp4` | 1920×1080 / 60fps / 10.0s / 15 Mbps | 无字幕母版，二次剪辑用 |

版式：竖屏上部标题区，中部 16:9 画面（1080×608），下部四条字幕；背景为画面自身模糊放大铺底。四条字幕依次为「5600 个粒子 实时运算」「三层球壳 加经纬网格」「七块面板 一屏读完状态」「可复用的 HUD 设计规则」。

配乐为程序化合成（低频脉冲 + pad + 高频颗粒 + 结尾上扬），无第三方素材，可商用。`mean -19.9 dB / max -6.4 dB`。

### 重新生成

画面不是录屏，而是逐帧定格渲染（`?rec=1` 下由脚本调用 `window.__renderFrame(ms)`），因此不会掉帧、不会拍到浏览器 UI：

```bash
python3 rec_frames.py --fps 60 --dur 10 --lang zh     # 输出 /tmp/jarvis_frames/*.jpg
```

再用 ffmpeg 合成（`FF` 为 ffmpeg 可执行文件；中文字体用 `STHeiti Medium`）：

```bash
# 横屏母版
$FF -framerate 60 -i /tmp/jarvis_frames/f%05d.jpg \
  -vf "scale=in_range=full:out_range=tv,format=yuv420p" \
  -c:v libx264 -crf 17 -preset medium -r 60 -movflags +faststart -an \
  jarvis-master-1920x1080.mp4

# 竖屏成片（模糊背景 + 前景 + 标题 + 定时字幕 + 配乐）
$FF -framerate 60 -i /tmp/jarvis_frames/f%05d.jpg -i /tmp/jarvis_music.wav \
  -filter_complex "[0:v]scale=2048:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=64,eq=brightness=0.03:saturation=1.42:contrast=1.16[bg];\
[0:v]scale=1080:608:flags=lanczos[fg];[bg][fg]overlay=0:392[base];\
[base]drawtext=fontfile=/tmp/hud_font.ttc:text='JARVIS':fontsize=110:fontcolor=0xEAFDFF:x=(w-text_w)/2:y=40,\dots,format=yuv420p,setsar=1[v]" \
  -map "[v]" -map 1:a -c:v libx264 -crf 20 -preset medium -r 60 -color_range tv \
  -c:a aac -b:a 192k -shortest -movflags +faststart jarvis-douyin-1080x1920.mp4
```

字幕用 `enable='between(t,a,b)'` 定时显示；改文案时同步改 `drawtext` 的 `text`，并注意避免半角逗号与冒号（它们是 filter 分隔符）。
