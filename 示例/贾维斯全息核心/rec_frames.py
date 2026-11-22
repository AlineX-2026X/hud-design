#!/usr/bin/env python3
"""把 hero.html 的动画逐帧定格导出为 JPEG 序列（不录屏，避免掉帧）。

用法：
    python3 rec_frames.py                 # 默认 10 秒 / 60fps / 中文
    python3 rec_frames.py --lang en --fps 60 --dur 10

输出：/tmp/jarvis_frames/f0000.jpg …
页面需要支持 ?rec=1（由外部调用 window.__renderFrame(ms) 渲染固定时刻）。
"""
import argparse
import os
import pathlib
import shutil
import time

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path("/tmp/jarvis_frames")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="zh", choices=["zh", "en"])
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--dur", type=float, default=10.0)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--quality", type=int, default=92)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)

    url = (HERE / "hero.html").as_uri() + f"?lang={args.lang}&rec=1"
    total = int(round(args.fps * args.dur))

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1"],
        )
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.goto(url)
        page.wait_for_function("window.__ready === true", timeout=15000)

        t0 = time.time()
        for i in range(total):
            page.evaluate("ms => window.__renderFrame(ms)", i * 1000.0 / args.fps)
            page.screenshot(
                path=str(out / f"f{i:05d}.jpg"),
                type="jpeg",
                quality=args.quality,
                animations="disabled",
            )
        browser.close()

    size = sum(f.stat().st_size for f in out.glob("*.jpg")) / 1e6
    print(f"frames={total} dir={out} size={size:.1f}MB elapsed={time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
