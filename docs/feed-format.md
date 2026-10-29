# Game feed format, version 1

One JSON file per game, written by that game's model repo (`<cli> export`) and
read by the Prometheus site build, which renders it with no knowledge of the game.
UTF-8, `ensure_ascii=False`, indent none. Times are UTC strings `YYYY-MM-DDTHH:MMZ`
(minute precision, exactly this shape: Prometheus parses with `%Y-%m-%dT%H:%MZ`).

```json
{
  "version": 1,
  "game": "valorant",                 // slug: [a-z0-9-]+; page is games/<game>.html
  "name": "Valorant",                 // display name (menu, page heading)
  "model": "Player round Elo",        // short name of the method behind the calls
  "generated": "2026-10-29T18:00Z",   // when the export ran
  "data_through": "2026-10-29",       // UTC date of the newest finished match in the DB
  "source": {"name": "VLR.gg", "url": "https://www.vlr.gg", "license": null},
  "sections": [                       // filter options, in display order
    {"key": "VCT", "label": "VCT", "major": true}
  ],
  "matches": [ <match>, ... ]         // any order; Prometheus sorts
}
```

`sections[].key` is a short code shown in the table's tier column and used as a
filter value (no commas or `|`). `major: true` sections form the default filter.

Match object:

```json
{
  "match_id": "777962",               // string, stable across exports for the same match
  "start": "2026-10-30T09:00Z",
  "status": "upcoming",               // "upcoming" | "live" | "final"
  "section": "VCT",                   // a sections[].key
  "event": "VCT 2026: China Threshold",
  "best_of": 3,                       // 1, 3 or 5 (int); null if unknown
  "name1": "Nova Esports", "name2": "A Team",
  "p_game": 0.5512,                   // team 1's chance to win one map (first map)
  "p_series": 0.5803,                 // team 1's chance to win the series (equals p_game for Bo1)
  "reconstructed": false,             // true: rebuilt after the match by replay, not saved before it
  "score1": null, "score2": null,     // map wins; current score when live, final score when final
  "winner": null,                     // 1 | 2 when final; null otherwise
  "url": "https://www.vlr.gg/777962", // source page for the match, or null
  "market": null                      // or {"p": 0.62, "at": "2026-10-29T18:00Z", "url": "https://kalshi.com/..."}
}
```

`market.p` is Kalshi's chance for team 1 (mid of yes bid/ask on team 1's
contract, or 1 − mid of team 2's). Upcoming/live: the price at export time.
Final: the closing line (last hourly candle mid at or before start), or null.

Which matches: every match from 2026-01-01 on with both teams rated, plus every
upcoming match within the next 7 days whose two teams are known (TBD sides are
left out), plus live ones. A final match's call is its frozen call when one was
saved before the start (`reconstructed: false`), otherwise the replay's
pre-match call (`reconstructed: true`).
