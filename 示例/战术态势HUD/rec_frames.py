#!/usr/bin/env python3
"""把战术态势 HUD 的动画逐帧定格导出为 JPEG 序列（不录屏，避免掉帧、不拍到窗口边框）。

用法：
    python3 rec_frames.py                       # 10 秒 / 60fps / 中文版
    python3 rec_frames.py --lang en             # 英文版
    python3 rec_frames.py --fps 60 --dur 10 --out /tmp/tactical_frames

前提：页面支持 ?rec=1（不跑 rAF，由外部调用 window.__renderFrame(ms)）。
"""
import argparse
import pathlib
import shutil
import time

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="zh", choices=["zh", "en"])
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--dur", type=float, default=10.0)
    ap.add_argument("--out", default="/tmp/tactical_frames")
    ap.add_argument("--quality", type=int, default=92)
    args = ap.parse_args()

    html = "hero.html" if args.lang == "en" else "hero-zh.html"
    out = pathlib.Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)

    url = (HERE / html).as_uri() + "?rec=1"
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
                animations="allow",
            )
        browser.close()

    size = sum(f.stat().st_size for f in out.glob("*.jpg")) / 1e6
    print(f"{total} frames -> {out}  ({size:.1f} MB, {time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
