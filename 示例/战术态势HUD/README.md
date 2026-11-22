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
