# Demo video tools

Scripts that build the short demo videos for the Actors. They draw cards from a saved run record or sample file, so nothing is invented and no Actor is called.

Requirements: Python 3, `pillow` and `imageio-ffmpeg` (pinned in a scratch virtual environment, for example `imageio-ffmpeg==0.6.0`). The cards use Segoe UI and Consolas. Set `DEMO_FONT_DIR` to a folder holding `segoeui.ttf`, `segoeuib.ttf` and `consola.ttf` if they are not in `C:/Windows/Fonts`.

Run the scripts from this folder, because the LEI and Trade Info scripts import `make_contracts_demo`.

| Script | Input | Output |
|---|---|---|
| `make_contracts_demo.py --data run.json --out <folder>` | run record JSON with `rows`, `run_id`, `started`, `finished`, `usage`, `events` (the Contracts Lookup run) | `contracts-lookup-demo.mp4`, silent |
| `make_lei_demo.py --data run.json --out <folder>` | the same JSON shape for an LEI Lookup run | `lei-lookup-demo.mp4`, silent |
| `make_trade_demo.py --csv sample.csv --out <folder>` | a saved 20-row sample CSV with the company-name column | `uk-importers-exporters-demo-silent.mp4`, names blurred |
| `add_music.py <video> <track.mp3> <out.mp4>` | a finished video and a track | the video with the music bed |

All videos are 1920x1080, 30 fps, H.264 (`libx264`, CRF 20, `yuv420p`, `+faststart`). Add `--preview <folder>` to save one still per scene.

## Music

`add_music.py` copies the video stream and mixes the track at -18 dB, with a 0.5 s fade in and a 1.5 s fade out, trimmed to the video length, as AAC at 192 kbit/s and 48 kHz.

The track used so far is "Pulsar" by The Grey Room / Density & Time, from the YouTube Audio Library (attribution not required). Keep a one-line credit next to the videos, for example:

`Music: "Pulsar" by The Grey Room / Density & Time (YouTube Audio Library, attribution not required)`

Check a track's licence terms yourself before you use it.

## What to keep out of the repository

Run records and sample files hold real data (notice titles, company names), and the videos are large. Keep them outside the repository. Names of trading companies are always blurred in the Trade Info video.

The scripts do not read tokens. The run record is saved by the caller from a finished run.
