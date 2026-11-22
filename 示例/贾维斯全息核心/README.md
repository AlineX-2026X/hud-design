# 贾维斯全息核心（示例）

1920×1080、单文件、零外部依赖。径向构图：中央 3,600 粒子的球核，三段反向缓转的弧，一条 6 秒一轮的扫描切面；四角只放短面板，球体包围盒内零文字。

双语在运行时切换：`?lang=zh` / `?lang=en`，不带参数时按系统语言（`navigator.language`）自动选择，行为与 `scripts/detect-language.sh` 的口径一致。

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
| 粒子球 | 常态呼吸 | 自转 0.16 rad/s，半径脉动 ±2.8%，8 秒一周期 |
| 三段弧 | 常态呼吸 | 0.055 / −0.042 / 0.030 rad/s，互相反向 |
| 扫描切面 | 常态呼吸 | 6.6 秒往返一次，切到的粒子提亮，不做频闪 |
| 强调 | 无 | 画面内不放大动效，保持「活着但不吵」 |

## 改文案的边界

- 机器标识不翻译：`JARVIS`、`v4.2`、`°C`、`kHz` 之类保持一致。
- 单位跟语言走：中文用「转/分、帧/秒、千赫、分贝、毫秒」，英文用 `RPM`、`FPS`、`kHz`、`dB`、`MS`。
- 一屏只允许一种自然语言；混排只留机器标识。
- 不使用电影台词与角色视觉（头盔、厂牌标识）。这里是通用的 AI 核心界面，不是某部作品的复刻。
