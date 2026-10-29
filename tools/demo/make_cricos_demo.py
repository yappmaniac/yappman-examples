"""CRICOS Register Lookup demo video (1920x1080, 30 fps, H.264) from a saved run record.

Usage: python make_cricos_demo.py --data cricos/run.json --out <folder> [--preview <dir>]
The JSON holds a "search" and a "lookup" record, each with run_id, status, started, finished, usage, events, rows
and summary. Same look as make_contracts_demo.py; scenes are drawn from the real run records only.
Provider names, postcodes and cities are never drawn: only the provider code and the register's own counts and types.
"""
import json
import subprocess
from datetime import datetime
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

import make_contracts_demo as m
from make_contracts_demo import (ACCENT, BG, FG, FONT, FONT_B, FPS, H, LINE, MONO, MUTED, PANEL, W,
                                 arg, caption_bar, centred, font)

STORE_URL = "https://apify.com/yappman/cricos-register"
TITLE = "CRICOS Register Lookup (Australia)"


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def text_card(heading, body, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((120, 110), heading, font=font(FONT_B, 54), fill=FG)
    f = font(FONT, 42)
    for i, line in enumerate(body):
        d.text((120, 250 + 80 * i), line, font=f, fill=FG)
    caption_bar(img, caption)
    return img


def attribution_card(attribution, non_affiliation):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((120, 110), "Data and licence", font=font(FONT_B, 54), fill=FG)
    f = font(FONT, 40)
    y = 250
    for line in wrap(d, attribution, f, W - 240):
        d.text((120, y), line, font=f, fill=FG)
        y += 62
    d.text((120, y + 40), non_affiliation, font=f, fill=MUTED)
    caption_bar(img, "From the run's RUN_SUMMARY record")
    return img


def table_card(rows, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cols = [("providerCode", 300), ("institutionType", 330), ("state", 180), ("institutionCapacity", 360),
            ("courseCount", 250), ("activeCourseCount", 300)]
    x0, hy, rh = 60, 50, 62
    hf, bf = font(FONT_B, 30), font(FONT, 32)
    x = x0
    for key, w in cols:
        d.text((x, hy), key, font=hf, fill=ACCENT)
        x += w
    d.line([x0 - 10, hy + 54, W - x0 + 10, hy + 54], fill=LINE, width=2)
    for i, r in enumerate(rows):
        y = hy + 70 + i * rh
        if i % 2 == 0:
            d.rectangle([x0 - 10, y, W - x0 + 10, y + rh], fill=(27, 29, 32))
        x = x0
        for key, w in cols:
            v = r.get(key)
            d.text((x, y + 13), "" if v is None else str(v), font=bf, fill=FG)
            x += w
    caption_bar(img, caption)
    return img


def end_card():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    centred(d, 340, TITLE, font(FONT_B, 72), FG)
    centred(d, 460, STORE_URL, font(FONT, 52), ACCENT)
    centred(d, 580, "CRICOS data, CC BY 2.5 AU. Pay per record.", font(FONT, 36), MUTED)
    centred(d, 640, "Not affiliated with or endorsed by the Department of Education.", font(FONT, 34), MUTED)
    return img


def main():
    data = json.load(open(arg("--data"), encoding="utf-8"))
    s, lk = data["search"], data["lookup"]
    out = Path(arg("--out"))
    out.mkdir(parents=True, exist_ok=True)
    secs = lambda r: (datetime.fromisoformat(r["finished"].replace("Z", "+00:00"))
                      - datetime.fromisoformat(r["started"].replace("Z", "+00:00"))).total_seconds()
    sm = s["summary"]
    codes = [r["providerCode"] for r in s["rows"][:2]]
    total = s["usage"] + lk["usage"]
    scenes = [
        (4.0, m.title_card(TITLE + " on the Apify Store", "Search Australian education providers for overseas students")),
        (6.0, attribution_card(sm["attribution"], sm["nonAffiliation"])),
        (4.0, m.code_card("Search input", ['{', '  "mode": "search",', '  "states": ["NSW"],', '  "maxItems": 10', '}'],
                          "One state, at most 10 rows")),
        (4.0, m.code_card("Run finished", [f"run     {s['run_id']}", "status  SUCCEEDED", f"time    {secs(s):.0f} seconds",
                                           f"rows    {sm['returned']} of {sm['matched']} matched"],
                          f"From the run record. Register copy dated {sm['snapshotDate']}")),
        (9.0, table_card(s["rows"], "Provider code and the register's own fields. Names, postcodes and cities are not shown in this video")),
        (4.0, m.code_card("Look up by code", ['{', '  "mode": "lookup",', f'  "providerCodes": ["{codes[0]}", "{codes[1]}"]', '}'],
                          f"Run {lk['run_id']}: SUCCEEDED, {len(lk['rows'])} rows")),
        (4.0, m.code_card("What it cost", [f"search  {s['events']['record']} x $0.002", f"lookup  {lk['events']['record']} x $0.002",
                                           f"total   ${total:.3f}"],
                          "Pay per record: $0.002 a row, no start fee")),
        (4.0, end_card()),
    ]
    mp4 = out / "cricos-register-demo-silent.mp4"
    proc = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo",
                             "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                             "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart",
                             str(mp4)], stdin=subprocess.PIPE)
    length = 0
    for idx, (dur, img) in enumerate(scenes):
        raw = img.tobytes()
        for _ in range(int(round(dur * FPS))):
            proc.stdin.write(raw)
        length += dur
        if arg("--preview"):
            Path(arg("--preview")).mkdir(parents=True, exist_ok=True)
            img.save(Path(arg("--preview")) / f"cricos-{idx}.png")
    proc.stdin.close()
    proc.wait()
    print(mp4, f"{length:.1f} s")


if __name__ == "__main__":
    main()
