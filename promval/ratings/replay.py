"""Load played maps and replay a model chronologically without result leakage."""

import pandas as pd


def load_maps(conn) -> pd.DataFrame:
    return pd.read_sql(
        """SELECT g.game_id, m.match_id, m.start_utc, g."order", g.map,
                  m.team1_id, m.team2_id, (g.score1 > g.score2) AS won,
                  m.best_of, m.event_id, COALESCE(e.section, 'unknown') AS section,
                  COALESCE(e.international, 0) AS international,
                  (m.winner = 1) AS series_won
           FROM maps g JOIN matches m USING (match_id)
           LEFT JOIN events e USING (event_id)
           WHERE g.score1 != g.score2
           ORDER BY m.start_utc, m.match_id, g."order"
        """,
        conn,
    )


def replay(maps, model) -> pd.DataFrame:
    result = maps.sort_values(["start_utc", "match_id", "order"], kind="stable").copy()
    probabilities = []
    for row in result.itertuples(index=False):
        probabilities.append(model.predict(row))
        model.update(row)
    result["p"] = probabilities
    return result.reset_index(drop=True)
