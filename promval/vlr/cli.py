"""VLR cache collection commands."""

from datetime import date
from typing import Annotated

import typer

from promval.vlr.crawl import crawl as crawl_pages
from promval.vlr.http import Fetcher

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main():
    """Crawl VLR.gg into a permanent raw cache."""


def _date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise typer.BadParameter("expected YYYY-MM-DD") from exc


@app.command()
def crawl(
    since: Annotated[str, typer.Option(callback=_date)],
    economy_since: Annotated[str, typer.Option(callback=_date)] = "2023-01-01",
    max_matches: Annotated[int | None, typer.Option(min=0)] = None,
    min_interval: Annotated[float, typer.Option(min=0)] = 2.0,
    full: Annotated[
        bool, typer.Option(help="Walk back to --since even past cached pages.")
    ] = False,
):
    """Cache completed matches since a date (inclusive)."""
    typer.echo(f"Estimate: ~2 requests per new match at {min_interval:g} s")
    result = crawl_pages(
        Fetcher(min_interval=min_interval),
        since,
        economy_since,
        max_matches,
        stop_after_known_pages=10**9 if full else 3,
    )
    typer.echo(
        f"pages={result.pages_read} matches={result.matches_fetched} "
        f"economy={result.economy_fetched} skipped={result.skipped} errors={result.errors}"
    )
