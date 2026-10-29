"""The `promval` command line."""

from pathlib import Path

import typer

from promval.kalshi.cli import app as kalshi_app
from promval.vlr.cli import app as vlr_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(kalshi_app, name="kalshi", help="Collect Kalshi Valorant markets.")
app.add_typer(vlr_app, name="vlr", help="Crawl and parse VLR.gg matches.")


@app.command()
def export(out: Path | None = None, no_fetch: bool = False, state: Path | None = None):
    """Write Valorant predictions for the Prometheus website."""
    from promval.feed import export as export_feed
    from promval.feed import load_state

    export_feed(out, no_fetch=no_fetch, state=load_state(state) if state else None)


@app.command()
def feed_state(out: Path | None = None):
    """Save replayed ratings for DB-free website exports."""
    import os
    import time

    from promval.feed import REPO, save_state, state_from_db

    started = time.perf_counter()
    out = (
        out or Path(os.environ.get("PROMVAL_DATA", REPO / "data")) / "feed/state.pkl.gz"
    )
    state = state_from_db()
    save_state(state, out)
    print(
        f"state={out} bytes={out.stat().st_size} elapsed={time.perf_counter() - started:.2f}s"
    )


if __name__ == "__main__":
    app()
