# Tech

## Stack

Python ≥ 3.12 with uv; SQLite rebuilt from raw caches; raw SQL; Typer CLI (`promval`); BeautifulSoup + lxml for HTML; ruff; pytest (offline, fixtures in `tests/fixtures/`).

## Layout

| Path | Purpose |
|---|---|
| `promval/main.py` | CLI entry; mounts the `kalshi` and `vlr` command groups |
| `promval/kalshi/api.py` | Public HTTP client, pacing, retries and pagination |
| `promval/kalshi/collect.py` | Raw catalog, trade, candle and book files |
| `promval/kalshi/cli.py` | Collector and book-loop commands |
| `tests/test_kalshi_collect.py` | Offline fixture-based collector and CLI tests |
| `promval/vlr/` | VLR.gg crawler, raw cache and parsers |
| `scripts/work_log.py`, `.githooks/` | Work-log tooling |
| `tests/test_steering.py` | Doc guard |
| `tests/fixtures/` | Saved Kalshi JSON and gzipped VLR pages |

## Kalshi collector

`promval kalshi collect [--no-books] [--limit N]` refreshes both Valorant series (`KXVALORANTGAME`, `KXVALORANTMAP`), saves final-market histories and snapshots active books. `--limit` caps new trade/candle fetches combined (each file attempt counts separately). `promval kalshi books --every 60 --minutes 60` refreshes active tickers each pass; pass summaries include failures. No schedule installed.

Public base: `https://api.elections.kalshi.com/trade-api/v2`. Paginate `/markets` and `/historical/markets` by series; merge by ticker, preferring `/markets`. Historical-catalog markets use `/historical/trades?ticker=T` and `/historical/markets/T/candlesticks`; recent markets use `/markets/trades?ticker=T` and `/series/S/markets/T/candlesticks`. Trades paginate with `limit=1000`; hourly candles use market open/close unix timestamps and `period_interval=60`. Preserve raw fields. Books use `/markets/T/orderbook`; the books loop discovers tickers through `/markets?series_ticker=S&status=open`.

Under `data/kalshi/` (or `$PROMVAL_DATA/kalshi/`):

- `markets/<SERIES>.json`: raw market list sorted by ticker, refreshed each run.
- `trades/<TICKER>.jsonl.gz`: raw full tape sorted by (`created_time`, `trade_id`).
- `candles/<TICKER>.json.gz`: raw candlesticks list.
- `books/<TICKER>.jsonl`: append-only lines with `at` (UTC ISO Z, second precision) and raw `orderbook_fp`.

New files and refreshed catalogs use temporary files plus atomic rename. Only finalized/settled markets get histories; existing trade/candle files are never rewritten. Empty tapes with positive `volume_fp` (or `volume`) and empty candle lists report errors without writing files, allowing retries. Zero-volume empty tapes are saved as complete. Other markets continue after failures; failed catalogs skip that series. Initial book creation is atomic; later snapshots append.

The standard-library client uses a repository User-Agent, 30-second timeout and at least 0.06 seconds between requests. HTTP 429/5xx, URL errors and timeouts retry up to five attempts with 1/2/4/8-second backoff. First-run estimate: about 10k final markets × two requests at ~0.06-second spacing plus latency, roughly an hour; pagination and retries can add time.

## VLR scraper

Not built yet.
