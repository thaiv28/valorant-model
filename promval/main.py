"""The `promval` command line."""

import typer

from promval.kalshi.cli import app as kalshi_app
from promval.vlr.cli import app as vlr_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(kalshi_app, name="kalshi", help="Collect Kalshi Valorant markets.")
app.add_typer(vlr_app, name="vlr", help="Crawl and parse VLR.gg matches.")

if __name__ == "__main__":
    app()
