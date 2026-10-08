"""Fail if the repo contains notebook outputs, token-like strings, data files or images.

Checks: notebook outputs, execution counts, cell attachments and stored widget
state; strings shaped like current Apify tokens (apify_api_...) or a token in a
URL query; and data, image or saved-map files. It cannot spot every secret, so
keep GitHub secret scanning on as well.

Run before every commit: python scripts/check_repo.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN_RES = [
    re.compile(r"apify_api_[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)[?&]token=[A-Za-z0-9_]{20,}"),
]
BANNED_SUFFIXES = {
    ".csv", ".parquet", ".jsonl", ".json", ".xlsx", ".xls", ".pdf", ".pkl", ".feather",
    ".db", ".sqlite", ".zip", ".html",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
}
SKIP_DIRS = {".git", ".venv", "venv", "output", ".ipynb_checkpoints", "__pycache__"}


def repo_files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return [ROOT / line for line in out.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob("*")
                if p.is_file() and not SKIP_DIRS.intersection(p.relative_to(ROOT).parts)]


problems = []
for path in repo_files():
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix.lower() in BANNED_SUFFIXES:
        problems.append(f"{rel}: data, image or map files do not belong in this repo")
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if any(rx.search(text) for rx in TOKEN_RES):
        problems.append(f"{rel}: contains something that looks like a token")
    if path.suffix == ".ipynb":
        nb = json.loads(text)
        if nb.get("metadata", {}).get("widgets"):
            problems.append(f"{rel}: stored widget state; clear it before committing")
        for i, cell in enumerate(nb["cells"]):
            if cell.get("outputs") or cell.get("execution_count") or cell.get("attachments"):
                problems.append(f"{rel}: cell {i} has outputs or attachments; clear them before committing")
                break

print("\n".join(problems) if problems else "OK: no outputs, tokens, data files or images")
sys.exit(1 if problems else 0)
