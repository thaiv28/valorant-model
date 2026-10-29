"""Permanent gzip raw cache; paths follow PROMVAL_DATA at call time."""

import gzip
import os
import tempfile
from pathlib import Path


def root() -> Path:
    default = Path(__file__).resolve().parents[2] / "data"
    return Path(os.environ.get("PROMVAL_DATA", default)) / "vlr" / "raw"


def match_path(match_id: int) -> Path:
    return root() / "matches" / f"{match_id}.html.gz"


def economy_path(match_id: int) -> Path:
    return root() / "matches" / f"{match_id}_economy.html.gz"


def has(path: Path) -> bool:
    return path.is_file()


def save(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(gzip.compress(text.encode("utf-8")))
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load(path: Path) -> str:
    return gzip.decompress(path.read_bytes()).decode("utf-8")
