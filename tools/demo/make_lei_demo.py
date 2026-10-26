"""LEI Lookup demo video (1920x1080, 30 fps, H.264) from a saved run record.

Usage: python make_lei_demo.py --data lei_demo/run.json --out <folder>
Same look as make_contracts_demo.py; scenes are drawn from the real run record only.
"""
import json
import subprocess
from datetime import datetime
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

import make_contracts_demo as m
from make_contracts_demo import BG, FG, MUTED, ACCENT, PANEL, LINE, W, H, FPS, font, centred, caption_bar, arg, FONT, FONT_B, MONO

STORE_URL = "https://apify.com/yappman/lei-lookup"


def end_card():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    centred(d, 380, "LEI Lookup", font(FONT_B, 72), FG)
    centred(d, 500, STORE_URL, font(FONT, 52), ACCENT)
    centred(d, 620, "GLEIF Golden Copy data. Pay per entity.", font(FONT, 36), MUTED)
    return img


def record_card(rec, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((120, 70), rec["legalName"], font=font(FONT_B, 54), fill=FG)
    city = lambda a: (a or {}).get("city", "")
    rows = [("lei", rec["lei"]), ("legalName", rec["legalName"]), ("jurisdiction", rec["jurisdiction"]),
            ("entityStatus", rec["entityStatus"]), ("registrationStatus", rec["registrationStatus"]),
            ("legalForm", rec["legalForm"]), ("legalAddress.city", city(rec["legalAddress"])),
            ("initialRegistrationDate", rec["initialRegistrationDate"][:10]),
            ("lastUpdateDate", rec["lastUpdateDate"][:10]), ("nextRenewalDate", rec["nextRenewalDate"][:10]),
            ("registeredAs", rec["registeredAs"]), ("bic", ", ".join(rec.get("bic") or []))]
    mf = font(MONO, 36)
    d.rounded_rectangle([120, 170, 1500, 170 + 30 + 64 * len(rows)], radius=18, fill=PANEL, outline=LINE, width=2)
    for i, (k, v) in enumerate(rows):
        d.text((160, 190 + 64 * i), k, font=mf, fill=ACCENT)
        d.text((760, 190 + 64 * i), str(v), font=mf, fill=FG)
    caption_bar(img, caption)
    return img


def main():
    data = json.load(open(arg("--data"), encoding="utf-8"))
    rec = data["rows"][0]
    out = Path(arg("--out"))
    out.mkdir(parents=True, exist_ok=True)
    t0, t1 = (datetime.fromisoformat(data[k]) for k in ("started", "finished"))
    secs = (t1 - t0).total_seconds()
    ev = data["events"]["entity"]
    scenes = [
        (4.0, m.title_card("LEI Lookup on the Apify Store", "Look up legal entities by LEI, in one fixed row schema")),
        (4.0, m.code_card("Default input", ['{', '  "mode": "lei",', '  "leis": ["2138002P5RNKC5W2JZ46"]', '}'],
                          "One LEI: TESCO PLC")),
        (4.0, m.code_card("Run finished", [f"run     {data['run_id']}", "status  SUCCEEDED", f"time    {secs:.0f} seconds",
                                           "entities 1"], "From the run record of the default input")),
        (10.0, record_card(rec, "The entity record: identity, status, registration dates, address, BIC codes")),
        (5.0, m.schema_card(list(rec.keys()), "The same fields for every entity", "One fixed row per entity")),
        (4.0, m.code_card("What it cost", [f"entity  {ev} x $0.004", f"total   ${data['usage']:.3f}"],
                          "Pay per event: $0.004 an entity, no start fee, charged on this run's record")),
        (4.0, end_card()),
    ]
    mp4 = out / "lei-lookup-demo.mp4"
    proc = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo",
                             "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                             "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart",
                             str(mp4)], stdin=subprocess.PIPE)
    total = 0
    for dur, img in scenes:
        raw = img.tobytes()
        for _ in range(int(round(dur * FPS))):
            proc.stdin.write(raw)
        total += dur
        if arg("--preview"):
            Path(arg("--preview")).mkdir(parents=True, exist_ok=True)
            img.save(Path(arg("--preview")) / f"lei-{int(total)}.png")
    proc.stdin.close()
    proc.wait()
    print(mp4, f"{total:.1f} s")


if __name__ == "__main__":
    main()
