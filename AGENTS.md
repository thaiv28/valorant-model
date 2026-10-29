# AGENTS.md

Guidance for AI coding agents (and humans) working in this repo.

## Read before work

Read only what your change touches. If your task came with a spec naming files and docs, read those and skip this list.

- **Always:** the newest work-log entries, `python3 scripts/work_log.py recent 5` (not the whole file).
- **Data sources, tables, file layout, tests:** [Tech](docs/steering/tech.md).
- **Feature status, known limits, future work:** [Current state](docs/steering/current_state.md).
- **Goals and the model plan:** [Product](docs/steering/product.md) and the design plan, `docs/design_plan.pdf`.
- **Schedules, storage, AWS:** [Deployment](docs/steering/deployment.md).

Read large docs by section (`grep -n '^## '`), not whole. Code and the built data are the source of truth; if a doc disagrees, verify and fix the doc in the same change. The user's latest instructions override these docs.

## Required document updates

- **Every substantive code or behavior change:** a dated entry at the top of `docs/steering/work_log.md`: what changed, the checks actually run, any remaining limit. At most 150 words.
- **Feature status, known limit or future work changes:** `docs/steering/current_state.md` (suggestions go in its **Future work** section).
- **Sources, tables, algorithms, file or test layout:** `docs/steering/tech.md`.
- **Schedules, storage, secrets, AWS:** `docs/steering/deployment.md`.

`uv run pytest -q` includes `tests/test_steering.py`, which fails when code changed (uncommitted) without a `work_log.md` change or a steering doc passes its word budget.

The pre-commit hook rotates the work log (past 15 entries, all but the newest 10 move to `work_log_archive.md`). Enable once per clone: `git config core.hooksPath .githooks`.

## What this is

A pre-map trading model for Valorant esports: player-based round Elo, a map layer and a veto model, priced against Kalshi's Valorant series (`KXVALORANTGAME`) and map-winner (`KXVALORANTMAP`) markets. It follows the conventions of the sister project Prometheus (LoL, `../Prometheus`), whose Elo, benchmark and Kalshi execution code it reuses. A website comes later.

## Quick commands

```bash
uv sync                                   # install (Python >= 3.12, managed by uv)
uv run pytest -q                          # tests (offline; fixtures in tests/fixtures/)
uv run ruff format && uv run ruff check   # format and lint (CI checks both)
uv run promval --help                     # CLI: kalshi and vlr command groups
```

`data/` and `db/` are gitignored build artifacts. Never commit them.

### Worktrees

Work in a separate worktree (`git worktree add ../valorant-model-<branch> -b <branch> <base>`), then `uv sync`. Share the read-only raw caches by symlink (`mkdir -p data && ln -s "$MAIN/data/vlr" "$MAIN/data/kalshi" data/`); never share `db/`.

## Conventions

- **Network is polite and cached.** VLR.gg: one request per 2 s by default, a User-Agent naming this repo, never re-fetch a cached final match page. Kalshi: public endpoints, small sleeps. Every fetcher takes an injectable `get` so tests never touch the network.
- **Raw first, parse later.** Raw responses are saved unchanged (gzip) and the DB is always rebuilt from them; parsers never fetch.
- **Data access is raw SQL** on SQLite (`sqlite3` or `pd.read_sql`); no ORM. Schema changes go in a new numbered `scripts/NNN_*.sql`; the DB is rebuilt from scratch, so there are no migrations.
- **Times are stored in UTC** (ISO 8601 with `Z`). VLR's `data-utc-ts` is US Eastern, not UTC: convert it.
- **Model changes need a significant benchmark gain** (paired bootstrap by series, 95% interval excluding 0), with a holdout of games from 2026-07-01 on that is never tuned on. Rules follow Prometheus's `docs/steering/tech.md`, Metric change rules.
- **Trading** reuses Prometheus's executor rules: League's limits from a $50 seed; no new orders once capital (seed + settled profit − open stakes) is $0 or less.
- **CI time is a budget.** Measure anything that adds CI work and record before/after in the work log.
- **Token use is a budget.** Keep docs short; scripts print summaries, not per-row logs.
- Formatting and linting: `ruff` (configured in `pyproject.toml`).

## Before you finish a change

1. `uv run pytest -q` and `uv run ruff format --check && uv run ruff check` pass.
2. Inspect the diff and make the doc updates above match the code. State anything you did not verify.
