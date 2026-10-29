PRAGMA foreign_keys = ON;
CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    event TEXT NOT NULL, event_id INTEGER NOT NULL, stage TEXT,
    start_utc TEXT NOT NULL, best_of INTEGER, patch TEXT,
    team1_name TEXT NOT NULL, team1_id INTEGER NOT NULL,
    team2_name TEXT NOT NULL, team2_id INTEGER NOT NULL,
    score1 INTEGER NOT NULL, score2 INTEGER NOT NULL,
    winner INTEGER CHECK (winner IN (1, 2))
);
CREATE TABLE vetoes (
    match_id INTEGER REFERENCES matches(match_id), step INTEGER,
    team_tag TEXT, action TEXT CHECK (action IN ('ban', 'pick', 'decider')), map TEXT,
    PRIMARY KEY (match_id, step)
);
CREATE TABLE maps (
    game_id INTEGER PRIMARY KEY, match_id INTEGER NOT NULL REFERENCES matches(match_id),
    "order" INTEGER NOT NULL, map TEXT NOT NULL, picked INTEGER NOT NULL, picked_by INTEGER CHECK (picked_by IN (1, 2)),
    score1 INTEGER NOT NULL, score2 INTEGER NOT NULL,
    team1_atk INTEGER, team1_def INTEGER, team2_atk INTEGER, team2_def INTEGER,
    overtime INTEGER NOT NULL, duration TEXT,
    UNIQUE (match_id, "order")
);
CREATE TABLE rounds (
    game_id INTEGER REFERENCES maps(game_id), round INTEGER,
    winner INTEGER CHECK (winner IN (1, 2)),
    winner_side TEXT CHECK (winner_side IN ('atk', 'def')),
    win_type TEXT CHECK (win_type IN ('elim', 'boom', 'defuse', 'time')),
    PRIMARY KEY (game_id, round)
);
CREATE TABLE player_maps (
    game_id INTEGER REFERENCES maps(game_id), player_id INTEGER,
    name TEXT, team INTEGER CHECK (team IN (1, 2)), agents TEXT,
    rating REAL, acs REAL, kills INTEGER, deaths INTEGER, assists INTEGER,
    kast REAL, adr REAL, hs_pct REAL, fk INTEGER, fd INTEGER,
    PRIMARY KEY (game_id, player_id)
);
CREATE TABLE economy (
    game_id INTEGER REFERENCES maps(game_id), team INTEGER CHECK (team IN (1, 2)),
    pistols_won INTEGER, pistols_played INTEGER,
    conversions_won INTEGER, conversions_played INTEGER,
    bonus_won INTEGER, bonus_played INTEGER,
    eco_played INTEGER, eco_won INTEGER,
    semi_eco_played INTEGER, semi_eco_won INTEGER,
    semi_buy_played INTEGER, semi_buy_won INTEGER,
    half_buy_played INTEGER, half_buy_won INTEGER,
    full_buy_played INTEGER, full_buy_won INTEGER,
    rounds TEXT,
    PRIMARY KEY (game_id, team)
);
