"""Contracts Lookup demo video (1920x1080, 30 fps, H.264, no audio).

Usage:
  python make_contracts_demo.py --data contracts_demo/run.json --out <folder>
                                [--stills <folder with store-*.png>] [--preview <dir>]

Scenes are drawn from the real run record (rows, run id, charged events) saved by the
caller in --data; nothing is invented. Optional Store-page captures named store-*.png
in --stills are shown full-frame with a caption, between the title card and the input.
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
BG, PANEL, LINE = (22, 23, 24), (32, 34, 37), (58, 61, 66)
FG, MUTED, ACCENT = (236, 238, 240), (150, 156, 164), (86, 156, 255)
FONT_DIR = os.environ.get("DEMO_FONT_DIR", "C:/Windows/Fonts")  # needs segoeui, segoeuib and consola
FONT = FONT_DIR + "/segoeui.ttf"
FONT_B = FONT_DIR + "/segoeuib.ttf"
MONO = FONT_DIR + "/consola.ttf"
STORE_URL = "https://apify.com/yappman/contracts-lookup"


def font(path, px):
    return ImageFont.truetype(path, px)


def arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def fit(draw, text, f, width):
    text = " ".join(str(text).split())
    if draw.textlength(text, font=f) <= width:
        return text
    while text and draw.textlength(text + "…", font=f) > width:
        text = text[:-1]
    return text.rstrip() + "…"


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def centred(d, y, text, f, fill):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


def caption_bar(img, text):
    d = ImageDraw.Draw(img)
    f = font(FONT, 34)
    d.rectangle([0, H - 110, W, H], fill=(14, 15, 16))
    d.text((60, H - 110 + (110 - 34) / 2 - 6), fit(d, text, f, W - 120), font=f, fill=FG)


def title_card(title, sub):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    centred(d, 400, title, font(FONT_B, 76), FG)
    centred(d, 520, sub, font(FONT, 38), MUTED)
    d.rectangle([W / 2 - 80, 600, W / 2 + 80, 606], fill=ACCENT)
    return img


def code_card(heading, lines, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((120, 120), heading, font=font(FONT_B, 54), fill=FG)
    box = [120, 240, 1100, 240 + 70 + 60 * len(lines)]
    d.rounded_rectangle(box, radius=18, fill=PANEL, outline=LINE, width=2)
    m = font(MONO, 40)
    for i, ln in enumerate(lines):
        d.text((160, 270 + 60 * i), ln, font=m, fill=FG)
    caption_bar(img, caption)
    return img


def fmt_value(v):
    return "" if v is None or v != v else f"{v:,.0f}"


def date_short(s):
    return s[:16].replace("T", " ") if s else ""


def table_frame(rows, scroll, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cols = [("publishedAt", 290, date_short), ("source", 110, str), ("title", 430, str),
            ("buyer", 350, str), ("value", 150, fmt_value), ("currency", 130, lambda v: v or ""),
            ("stage", 130, lambda v: v or ""), ("deadline", 200, lambda v: (v or "")[:10])]
    x0, hy, rh = 60, 40, 56
    body_top, body_bot = hy + 64, H - 110
    hf, bf = font(FONT_B, 28), font(FONT, 28)
    # rows, clipped to the body area
    layer = Image.new("RGB", (W, body_bot - body_top), BG)
    ld = ImageDraw.Draw(layer)
    for i, r in enumerate(rows):
        y = i * rh - scroll
        if y + rh < 0 or y > body_bot - body_top:
            continue
        if i % 2 == 0:
            ld.rectangle([x0 - 10, y, W - x0 + 10, y + rh], fill=(27, 29, 32))
        x = x0
        for key, w, fn in cols:
            v = r.get(key)
            txt = fn(v) if key != "source" else (v or "")
            tx = fit(ld, txt, bf, w - 18)
            if key == "value":
                tx_w = ld.textlength(tx, font=bf)
                ld.text((x + w - 24 - tx_w, y + 11), tx, font=bf, fill=FG)
            else:
                ld.text((x, y + 11), tx, font=bf, fill=FG)
            x += w
    img.paste(layer, (0, body_top))
    d.rectangle([0, 0, W, body_top], fill=BG)
    x = x0
    for key, w, _ in cols:
        if key == "value":
            d.text((x + w - 24 - d.textlength(key, font=hf), hy + 10), key, font=hf, fill=ACCENT)
        else:
            d.text((x, hy + 10), key, font=hf, fill=ACCENT)
        x += w
    d.line([x0 - 10, body_top - 4, W - x0 + 10, body_top - 4], fill=LINE, width=2)
    caption_bar(img, caption)
    return img


def schema_card(keys, caption, heading="One fixed row per notice"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((120, 100), heading, font=font(FONT_B, 54), fill=FG)
    m = font(MONO, 38)
    cols, per = 3, (len(keys) + 2) // 3
    for i, k in enumerate(keys):
        c, r = divmod(i, per)
        d.text((120 + c * 580, 230 + r * 80), k, font=m, fill=ACCENT if k in ("buyer", "value", "stage") else FG)
    caption_bar(img, caption)
    return img


def end_card():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    centred(d, 380, "UK Public Contracts Lookup", font(FONT_B, 72), FG)
    centred(d, 500, STORE_URL, font(FONT, 52), ACCENT)
    centred(d, 620, "Official data under the OGL. Pay per event.", font(FONT, 36), MUTED)
    return img


def still_scene(path, caption):
    src = Image.open(path).convert("RGB")
    box_w, box_h = W, H - 110
    s = min(box_w / src.width, box_h / src.height)
    src = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    img = Image.new("RGB", (W, H), BG)
    img.paste(src, ((W - src.width) // 2, (box_h - src.height) // 2))
    caption_bar(img, caption)
    return img


def main():
    data = json.load(open(arg("--data"), encoding="utf-8"))
    rows = data["rows"]
    out = Path(arg("--out"))
    out.mkdir(parents=True, exist_ok=True)
    stills = sorted(Path(arg("--stills")).glob("store-*.png")) if arg("--stills") else []
    preview = Path(arg("--preview")) if arg("--preview") else None
    t0, t1 = (datetime.fromisoformat(data[k].replace("Z", "+00:00")) for k in ("started", "finished"))
    secs = round((t1 - t0).total_seconds())
    cost = data["usage"]

    # (duration seconds, frame factory(t in 0..1) -> Image)
    scenes = []
    scenes.append((4.0, lambda t, im=title_card("UK Public Contracts Lookup on the Apify Store",
                                               "Find a Tender and Contracts Finder notices in one fixed row schema"): im, "title"))
    store_caps = ["The Actor's page on the Apify Store: official UK procurement notices, built to hold no personal data",
                  "Inputs: search, look up or monitor, with Public Contracts Scotland opt-in"]
    for i, p in enumerate(stills):
        im = still_scene(p, store_caps[min(i, len(store_caps) - 1)])
        scenes.append((4.5, lambda t, im=im: im, f"store{i}"))
    scenes.append((4.0, lambda t, im=code_card(
        "Default input", ['{', '  "mode": "search",', '  "sources": ["fts", "cf"],', '  "maxItems": 20', '}'],
        "Search mode, Find a Tender and Contracts Finder, 20 notices"): im, "input"))
    scenes.append((5.0, lambda t, im=code_card(
        "Run finished", [f"run {data['run_id']}", "status  SUCCEEDED", f"time    {secs} seconds",
                         f"notices {len(rows)}"],
        "From the run record of the default input"): im, "run"))
    # table: hold, scroll, hold
    def table_scene(t):
        max_scroll = max(0, len(rows) * 56 - (H - 110 - 104))
        s = 0 if t < 0.3 else (max_scroll if t > 0.75 else max_scroll * ease((t - 0.3) / 0.45))
        cap = ("20 notices: published, source, title, buyer, value, currency, stage, deadline"
               if t < 0.6 else "Every notice links back to its official page")
        return table_frame(rows, s, cap)
    scenes.append((14.0, table_scene, "table"))
    keys = [k for k in rows[0].keys()]
    scenes.append((5.0, lambda t, im=schema_card(keys, "The same fields for every source and every stage of a notice"): im, "schema"))
    scenes.append((5.0, lambda t, im=code_card(
        "What it cost", ["run     1 x $0.005", f"notice  {data['events']['notice']} x $0.005",
                         f"total   ${cost:.3f}"],
        "Pay per event: $0.005 a notice plus $0.005 a run, charged on this run's record"): im, "cost"))
    scenes.append((4.0, lambda t, im=end_card(): im, "end"))

    mp4 = out / "contracts-lookup-demo.mp4"
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                             "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                             "-movflags", "+faststart", str(mp4)], stdin=subprocess.PIPE)
    total = 0
    for dur, fn, name in scenes:
        n = int(round(dur * FPS))
        cache = None
        for k in range(n):
            t = k / max(1, n - 1)
            frame = cache if (name != "table" and cache is not None) else fn(t)
            cache = frame
            if preview and k == n // 2:
                preview.mkdir(parents=True, exist_ok=True)
                frame.save(preview / f"{name}.png")
            proc.stdin.write(frame.tobytes())
        total += dur
    proc.stdin.close()
    proc.wait()
    print(mp4, f"{total:.1f} s")


if __name__ == "__main__":
    main()
