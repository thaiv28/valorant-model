"""Permanent gzip raw cache; paths follow PROMVAL_DATA at call time."""

import gzip
import os
import pickle
import tempfile
from pathlib import Path

from promval.vlr import parse


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


def events_path(tier: int, page: int) -> Path:
    return root() / "events" / f"tier{tier}_p{page}.html.gz"


def parsed_path(match_id: int) -> Path:
    return root().parent / "parsed" / f"v{parse.PARSER_VERSION}" / f"{match_id}.pkl.gz"


def has_parsed(match_id: int) -> bool:
    path = parsed_path(match_id)
    if not path.is_file():
        return False
    modified = path.stat().st_mtime_ns
    return all(
        modified > raw.stat().st_mtime_ns
        for raw in (match_path(match_id), economy_path(match_id))
        if raw.is_file()
    )


def load_parsed(match_id: int):
    # Only load locally generated cache files, never untrusted pickles.
    with gzip.open(parsed_path(match_id), "rb") as source:
        return pickle.load(source)


def save_parsed(match_id: int, result) -> None:
    path = parsed_path(match_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as out:
            with gzip.GzipFile(fileobj=out, mode="wb") as compressed:
                pickle.dump(result, compressed, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
