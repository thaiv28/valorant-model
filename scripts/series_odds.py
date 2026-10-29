"""Compare frozen independent, temperature and momentum series odds offline."""

import argparse
import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from promval.evaluation import (
    HOLDOUT_START,
    fit_momentum,
    game_losses,
    paired_bootstrap,
    slot_probabilities,
)
from promval.ratings.models import MODELS
from promval.ratings.replay import load_lineups, load_maps, replay
from scripts.evaluate_elo import (
    REPO,
    fit_series_temperature,
    scored_rows,
    series_rows,
    with_series_temperature,
)


def loss(frame):
    return game_losses(frame.p, frame.won).log_loss.to_numpy()


def delta(a, b, clusters):
    if not len(a):
        return "—"
    mean, low, high = paired_bootstrap(
        a, b, clusters=clusters, n_resamples=2000, seed=0
    )
    return f"{mean:+.6f} [{low:+.6f}, {high:+.6f}]"


def table(columns, rows):
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *("| " + " | ".join(map(str, row)) + " |" for row in rows),
        ]
    )


def calibration(frame):
    bins = np.minimum((frame.p * 10).astype(int), 9)
    return [
        (
            f"{b / 10:.1f}–{(b + 1) / 10:.1f}",
            len(part),
            f"{part.p.mean():.6f}",
            f"{part.won.mean():.6f}",
        )
        for b in range(10)
        for part in [frame[bins == b]]
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("db/valorant.db"))
    parser.add_argument("--model", choices=MODELS, default="player_round_glicko_rookie")
    parser.add_argument("--seed-from", default="2021-01-01")
    parser.add_argument("--tune-from", default="2023-01-01")
    parser.add_argument("--tune-to", default="2025-09-01")
    parser.add_argument("--validate-to", default=HOLDOUT_START)
    parser.add_argument("--out", type=Path, default=Path("series_odds_report.md"))
    args = parser.parse_args(argv)
    try:
        for value in (args.seed_from, args.tune_from, args.tune_to, args.validate_to):
            if date.fromisoformat(value).isoformat() != value:
                raise ValueError
        if (
            not args.seed_from
            <= args.tune_from
            < args.tune_to
            < args.validate_to
            <= HOLDOUT_START
        ):
            raise ValueError
    except ValueError:
        parser.error(
            "require ISO dates: seed-from <= tune-from < tune-to < validate-to <= 2026-07-01"
        )
    if not args.db.is_file():
        parser.error(f"database does not exist: {args.db}")
    weights = json.loads((REPO / "promval/ratings/elo_weights.json").read_text())
    if args.model not in weights:
        parser.error(f"no frozen parameters in elo_weights.json for {args.model}")
    params = {
        key: value for key, value in weights[args.model].items() if key != "fit_through"
    }
    with sqlite3.connect(f"file:{args.db.resolve()}?mode=ro", uri=True) as conn:
        maps = scored_rows(load_maps(conn), args.seed_from, args.validate_to)
        predictions = replay(
            maps, MODELS[args.model](lineups=load_lineups(conn), **params)
        )
    stage1 = scored_rows(predictions, args.tune_from, args.tune_to)
    m = fit_momentum(stage1)
    temperatures = fit_series_temperature(stage1)
    momentum_temperatures = fit_series_temperature(stage1.assign(series_m=m))
    fit_line = (
        f"{args.model}: m={m:.6f}; T={temperatures}; m+T T={momentum_temperatures}"
    )
    summary = [fit_line]
    report = [
        "# Series momentum odds",
        fit_line,
        f"Frozen model parameters: `{json.dumps(params, sort_keys=True)}`. "
        f"Replay [{args.seed_from}, {args.validate_to}); stage 1 [{args.tune_from}, {args.tune_to}); "
        f"stage 2 [{args.tune_to}, {args.validate_to}). All fits use stage 1 only. "
        "Δ is candidate minus T (negative favors candidate); 95% percentile intervals "
        "use 2,000 paired match-clustered resamples, seed 0. Stage-1 comparisons are fitting diagnostics.",
    ]
    for stage, start, end in (
        (1, args.tune_from, args.tune_to),
        (2, args.tune_to, args.validate_to),
    ):
        frame = scored_rows(predictions, start, end)
        variants = {
            "independent": series_rows(frame),
            "T": series_rows(with_series_temperature(frame, temperatures)),
            "m": series_rows(frame.assign(series_m=m)),
            "m+T": series_rows(
                with_series_temperature(frame.assign(series_m=m), momentum_temperatures)
            ),
        }
        base = variants["T"]
        losses = {name: loss(rows) for name, rows in variants.items()}
        means = [
            (name, len(base), f"{values.mean():.6f}") for name, values in losses.items()
        ]
        report += [
            f"## Stage {stage} series log loss",
            table(["Odds", "Rows", "Log loss"], means),
        ]
        summary.append(
            f"Stage {stage} ({len(base)} series): "
            + "; ".join(
                f"{name} {values.mean():.6f}" for name, values in losses.items()
            )
        )
        slices = {
            "all": np.ones(len(base), dtype=bool),
            "Bo3": (base.best_of == 3).to_numpy(),
            "Bo5": (base.best_of == 5).to_numpy(),
            **{
                section: (base.section == section).to_numpy()
                for section in ("vct", "vcl", "gc")
            },
            "international=1": (base.international == 1).to_numpy(),
        }
        comparisons = []
        for name, mask in slices.items():
            comparisons.append(
                (
                    name,
                    int(mask.sum()),
                    *(
                        delta(
                            losses[v][mask],
                            losses["T"][mask],
                            base.match_id.to_numpy()[mask],
                        )
                        for v in ("m", "m+T")
                    ),
                )
            )
        report += [
            f"### Stage {stage} paired Δ vs T",
            table(["Slice", "Rows", "m − T [95% CI]", "m+T − T [95% CI]"], comparisons),
        ]
        summary.append(
            f"Stage {stage} Δ vs T: m {comparisons[0][2]}; m+T {comparisons[0][3]}"
        )
        if stage == 2:
            for name in ("T", "m+T"):
                report += [
                    f"## Stage 2 Bo3 calibration: {name}",
                    table(
                        ["Bin", "Rows", "Predicted", "Actual"],
                        calibration(variants[name][base.best_of == 3]),
                    ),
                ]
            # Only observed slots with a valid first-map baseline and odd best-of.
            first = frame[frame["order"] == 1].set_index("match_id").p
            later = frame[
                (frame["order"] >= 2)
                & frame.best_of.notna()
                & (frame.best_of > 0)
                & (frame.best_of % 2 == 1)
            ].copy()
            later["p0"] = later.match_id.map(first)
            later = later[later.p0.notna() & (later["order"] <= later.best_of)]
            later["slot_p"] = [
                slot_probabilities(r.p0, int(r.best_of), m)[int(r.order) - 1]
                for r in later.itertuples()
            ]
            map_rows = []
            for name, part in [
                ("all", later),
                *((f"Bo{int(n)}", group) for n, group in later.groupby("best_of")),
            ]:
                baseline = game_losses(part.p0, part.won).log_loss.to_numpy()
                candidate = game_losses(part.slot_p, part.won).log_loss.to_numpy()
                change = delta(candidate, baseline, part.match_id.to_numpy())
                map_rows.append(
                    (
                        name,
                        len(part),
                        f"{baseline.mean():.6f}",
                        f"{candidate.mean():.6f}",
                        change,
                    )
                )
                summary.append(f"Stage 2 map slots {name} (n={len(part)}): Δ {change}")
            report += [
                "## Stage 2 map slots (order ≥ 2)",
                "Kalshi pre-match setting: P(win slot | slot played) versus first-map p0; no realized previous winner is used.",
                table(
                    [
                        "Slice",
                        "Rows",
                        "p0 log loss",
                        "Slot log loss",
                        "Δ slot − p0 [95% CI]",
                    ],
                    map_rows,
                ),
            ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n\n".join(report) + "\n")
    print("\n".join(summary[:19]))
    print(f"Report: {args.out}")


if __name__ == "__main__":
    main()
