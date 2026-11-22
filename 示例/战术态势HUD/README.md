# 战术态势 HUD（示例）

1920×1080、单文件、零外部依赖，用来验证 `hud-design` 的分区、分层、语言与验收规则。

- `hero.html`：英文版，唯一源文件，所有布局与样式都在这里。
- `hero-zh.html`：中文版，由 `build-zh.py` 从英文版生成，别手改（改完会被覆盖）。
- `build-zh.py`：文案映射表。要改措辞，改英文版 + 映射表，再跑一次。
- `screenshots/`：`hero-1920x1080.png`、`hero-zh-1920x1080.png` 与对应 25% 缩略图。

## 重出图

```bash
python3 build-zh.py
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for f in hero hero-zh; do
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run \
    --force-device-scale-factor=1 --window-size=1920,1080 \
    --screenshot="screenshots/$f-1920x1080.png" "file://$PWD/$f.html"
done
sips -z 270 480 screenshots/hero-1920x1080.png    --out screenshots/hero-25pct.png
sips -z 270 480 screenshots/hero-zh-1920x1080.png --out screenshots/hero-zh-25pct.png
```

Windows 上把 `sips` 换成任意缩图工具即可；渲染用 Edge / Chrome 的 `--headless=new` 同样成立。

## 改文案的边界

- 机器标识（`UAV-02`、`ROE-2`、`TGT-01`、`AES-256`）不翻译，中英两版一致。
- 单位跟语言走：中文用「公里 / 毫秒」，英文用 `KM` / `MS`。
- 一屏只允许一种自然语言；新增文字先想清楚属于哪一版。

## 动效层

页面本身是静态构图，动效由末尾一段脚本注入。`?rec=1` 时不跑 rAF，改由外部调用 `window.__renderFrame(ms)` 逐帧渲染，所以可以精确定格导出，不会掉帧、不会拍到窗口边框。

| 动效 | 周期 / 触发 | 作用 |
|---|---|---|
| 入场推近 | 0–1.35s | 黑场淡入 + 3.5% 推近，交代「系统上线」 |
| 雷达扫掠 | 4 秒 / 圈 | 扇形余晖 + 前缘细线；目标被扫过时点亮再衰减 |
| 锁框漂移 | 全程，各自相位 | 目标在动、锁框跟动，画面不「贴死」 |
| 主目标双环 | 62°/s 与 −96°/s | 反向旋转，视线始终落回主目标 |
| 目标升级 | 6.2s | TGT-04 转红 + 三层脉冲环 + 告警条呼吸 |
| 频谱抖动 | 全程 | 20 根柱独立相位，读数不是死的 |
| 帧计数器 | 全程 | 时钟末位换成跳动帧号 |

## 抖音成片（10 秒 / 竖屏）

| 文件 | 规格 | 用途 |
|---|---|---|
| `tactical-douyin-1080x1920.mp4` | 1080×1920 / 60fps / 10.0s / AAC 立体声 / 2.3 MB | 直接投抖音、视频号 |
| `tactical-master-1920x1080.mp4` | 1920×1080 / 60fps / 10.0s / 5.4 Mbps | 无字幕母版，二次剪辑用 |

四条字幕依次为「一屏之内 读完整个战场」「等高线地形 四目标自动锁定」「告警升一级 只留一个主目标」「可复用的 HUD 设计规则」。配乐为程序化合成（48Hz 底噪 + 每 1.2 秒金属 ping + 每 4 秒雷达扫频 + 6.2 秒告警双音 + 结尾上扬），无第三方素材。

### 重新生成

```bash
python3 rec_frames.py --fps 60 --dur 10 --lang zh     # 输出 /tmp/tactical_frames/*.jpg
```

```bash
# 横屏母版
$FF -framerate 60 -i /tmp/tactical_frames/f%05d.jpg \
  -vf "scale=in_range=full:out_range=tv,format=yuv420p" \
  -c:v libx264 -crf 17 -preset medium -r 60 -movflags +faststart -an \
  tactical-master-1920x1080.mp4

# 竖屏成片：先把 -filter_complex 写进 fc.txt（imageio-ffmpeg 的构建不支持 -filter_complex_script）
$FF -framerate 60 -i /tmp/tactical_frames/f%05d.jpg -i /tmp/tactical_music.wav \
  -filter_complex "$(cat fc.txt)" -map "[v]" -map 1:a \
  -c:v libx264 -crf 20 -preset medium -r 60 -color_range tv \
  -af "volume=-6dB" -c:a aac -b:a 192k -shortest -movflags +faststart \
  tactical-douyin-1080x1920.mp4
```

背景取画面中段（`crop=1920:780:0:270`）再放大模糊、压暗加暗角——直接整帧模糊会把顶栏文字糊成一片脏底。
