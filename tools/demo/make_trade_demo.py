"""UK Importers and Exporters demo video (1920x1080, 30 fps, H.264) from a saved sample CSV.

Usage: python make_trade_demo.py --csv <sample.csv> --out <folder> [--preview <dir>] [--music <mp3>]
The name column is blurred in every frame. Nothing is read from Apify.
"""
import csv
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter

import make_contracts_demo as m
from make_contracts_demo import (ACCENT, BG, FG, FONT, FONT_B, H, LINE, MUTED, PANEL, W, FPS,
                                 arg, caption_bar, centred, code_card, ease, fit, font, title_card)

STORE_URL = "https://apify.com/yappman/uk-importers-exporters"
KAGGLE = "kaggle.com/datasets/russellyapp/uk-importers-and-exporters-hs-8419-aug-2026"
RUN_ID = "waHqOO59Um2WGBw75"


def text_card(heading, body, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((120, 110), heading, font=font(FONT_B, 54), fill=FG)
    f = font(FONT, 42)
    for i, line in enumerate(body):
        d.text((120, 250 + 80 * i), line, font=f, fill=FG)
    caption_bar(img, caption)
    return img


def end_card():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    centred(d, 340, "UK Importers and Exporters", font(FONT_B, 72), FG)
    centred(d, 460, STORE_URL, font(FONT, 52), ACCENT)
    centred(d, 580, "Free sample of this run on Kaggle (OGL credit):", font(FONT, 34), MUTED)
    centred(d, 630, KAGGLE, font(FONT, 36), FG)
    centred(d, 740, "Not affiliated with HMRC.", font(FONT, 34), MUTED)
    return img


def table_frame(rows, scroll, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cols = [("traderKey", 330), ("name", 560), ("postcodeDistrict", 260), ("flow", 150), ("month", 140),
            ("cn8Codes", 380)]
    x0, hy, rh = 60, 40, 56
    body_top, body_bot = hy + 64, H - 110
    hf, bf = font(FONT_B, 28), font(FONT, 28)
    layer = Image.new("RGB", (W, body_bot - body_top), BG)
    ld = ImageDraw.Draw(layer)
    blur = Image.new("RGB", (W, body_bot - body_top), BG)  # name column drawn here, then blurred
    bd = ImageDraw.Draw(blur)
    name_x = x0 + cols[0][1]
    for i, r in enumerate(rows):
        y = i * rh - scroll
        if y + rh < 0 or y > body_bot - body_top:
            continue
        if i % 2 == 0:
            ld.rectangle([x0 - 10, y, W - x0 + 10, y + rh], fill=(27, 29, 32))
            bd.rectangle([x0 - 10, y, W - x0 + 10, y + rh], fill=(27, 29, 32))
        x = x0
        for key, w in cols:
            v = r.get(key) or ""
            if key == "cn8Codes":
                v = ", ".join(v.split(";"))
            if key == "name":
                bd.text((x, y + 11), fit(bd, v, bf, w - 18), font=bf, fill=FG)
            else:
                ld.text((x, y + 11), fit(ld, v, bf, w - 18), font=bf, fill=FG)
            x += w
    name_w = cols[1][1]
    region = blur.crop((name_x - 10, 0, name_x + name_w - 8, body_bot - body_top)).filter(ImageFilter.GaussianBlur(11))
    layer.paste(region, (name_x - 10, 0))
    img.paste(layer, (0, body_top))
    d.rectangle([0, 0, W, body_top], fill=BG)
    x = x0
    for key, w in cols:
        d.text((x, hy + 10), key + (" (blurred)" if key == "name" else ""), font=hf, fill=ACCENT)
        x += w
    d.line([x0 - 10, body_top - 4, W - x0 + 10, body_top - 4], fill=LINE, width=2)
    caption_bar(img, caption)
    return img


def main():
    rows = list(csv.DictReader(open(arg("--csv"), encoding="utf-8", newline="")))
    assert len(rows) == 20, len(rows)
    imports = sum(r["flow"] == "imports" for r in rows)
    out = Path(arg("--out"))
    out.mkdir(parents=True, exist_ok=True)
    max_scroll = len(rows) * 56 - (H - 110 - 104)

    def table_scene(t):
        s = 0 if t < 0.3 else (max_scroll if t > 0.75 else max_scroll * ease((t - 0.3) / 0.45))
        return table_frame(rows, s, f"A 20-row search, both flows: {imports} imports, {len(rows) - imports} exports, HS 8419, 2026-08. "
                                    "Company names blurred in this video")

    scenes = [
        (4.0, lambda t, im=title_card("UK Importers and Exporters on the Apify Store",
                                      "Find UK traders by commodity code and month"): im),
        (5.0, lambda t, im=text_card("What the Store page says", [
            "Finds UK businesses that imported or exported goods,",
            "by HS code and month.",
            "Data: HMRC UK Trade Info, Open Government Licence v3.0.",
            "Not affiliated with HMRC."], "From the Store page, build 0.1.7"): im),
        (4.0, lambda t, im=code_card("Input", ['{', '  "hsCodes": ["8419"],', '  "maxItems": 20', '}'],
                                     "Search mode is the default. HS code 8419: heating and cooling machinery"): im),
        (4.0, lambda t, im=code_card("Run finished", [f"run     {RUN_ID}", "status  SUCCEEDED", "traders 20", "build   0.1.7"],
                                     "From the run record"): im),
        (12.0, table_scene),
        (5.0, lambda t, im=text_card("Names of organisations only", [
            "A name is returned only if it looks like an organisation.",
            "Sole traders' names are withheld.",
            "Only the outward postcode is returned, never a full postcode."],
            "From the Store page"): im),
        (4.0, lambda t, im=code_card("What it cost", ["run   $0.005", "rows  20 x $0.002", "total $0.045"],
                                     "Pay per event: $0.005 a run plus $0.002 per trader row"): im),
        (5.0, lambda t, im=end_card(): im),
    ]
    mp4 = out / "uk-importers-exporters-demo-silent.mp4"
    proc = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo",
                             "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                             "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart",
                             str(mp4)], stdin=subprocess.PIPE)
    total = 0
    for idx, (dur, fn) in enumerate(scenes):
        n = int(round(dur * FPS))
        cache = None
        for k in range(n):
            t = k / max(1, n - 1)
            frame = fn(t) if dur == 12.0 else (cache or fn(t))
            cache = frame
            if arg("--preview") and k == n // 2:
                Path(arg("--preview")).mkdir(parents=True, exist_ok=True)
                frame.save(Path(arg("--preview")) / f"trade-{idx}.png")
            proc.stdin.write(frame.tobytes())
        total += dur
    proc.stdin.close()
    proc.wait()
    print(mp4, f"{total:.1f} s")


if __name__ == "__main__":
    main()
