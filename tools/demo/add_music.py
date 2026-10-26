"""Mux a music bed under a finished demo video.

Usage: python add_music.py <video.mp4> <track.mp3> <out.mp4>

The video stream is copied unchanged. The track is trimmed to the video's length,
set to -18 dB, faded in over 0.5 s and faded out over the last 1.5 s, and encoded
as AAC 192 kbit/s at 48 kHz.
"""
import re
import subprocess
import sys

import imageio_ffmpeg

MUSIC_DB = -18
FADE_IN_S = 0.5
FADE_OUT_S = 1.5


def video_seconds(ffmpeg: str, video: str) -> float:
    err = subprocess.run([ffmpeg, "-i", video], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def main(video: str, track: str, out: str) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    total = round(video_seconds(ffmpeg, video), 2)
    af = (f"atrim=0:{total},asetpts=PTS-STARTPTS,volume={MUSIC_DB}dB,"
          f"afade=t=in:st=0:d={FADE_IN_S},afade=t=out:st={total - FADE_OUT_S}:d={FADE_OUT_S}")
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", video, "-i", track,
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-af", af,
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", str(total),
                    "-movflags", "+faststart", out], check=True)
    print(f"{out}: music at {MUSIC_DB} dB, {total} s")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
