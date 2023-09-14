import goalscorer_package.constants as c
import pandas as pd
import numpy as np
import glob
from statistics import mode

### Files ###


def league_from_file_path(file_path: str) -> int:
    return int(file_path.split("-")[-2])


def season_from_file_path(file_path: str) -> str:
    return file_path.split("\\")[-1].split("-league")[0]


def seasons_leagues_not_seen() -> list[c.SeasonLeague]:
    seasons_leagues_seen = []
    for file_path in glob.glob(c.FilePath.FBREF_RAW + "*summary.csv"):
        season = season_from_file_path(file_path)
        league = league_from_file_path(file_path)
        seasons_leagues_seen.append((season, league))

    seasons_leagues = c.seasons_leagues
    for season_league in seasons_leagues:
        for season_seen, league_seen in seasons_leagues_seen:
            if (season_league.season.season_str == season_seen) and (
                season_league.league.league_id == league_seen
            ):
                seasons_leagues.remove(season_league)

    return seasons_leagues


def get_seasons_leagues_from_str(
    seasons: list[str], comp_ids: list[int]
) -> list[c.SeasonLeague]:
    return [
        season_league
        for season_league in c.SEASONS_LEAGUES
        if (season_league.season.season_str in seasons)
        and (season_league.league.league_id in comp_ids)
    ]


def get_fbref_file_path(
    file_type: str, raw_file_bool: bool, season_league: c.SeasonLeague
) -> str:
    file_name = f"{season_league.season.season_str}-league-{season_league.league.league_id}-{file_type}.csv"
    if raw_file_bool:
        file_path = c.FilePath.FBREF_RAW + file_name
    else:
        file_path = c.FilePath.FBREF_EDITED + file_name

    return file_path


def load_seasons_leagues_files(
    file_type: str, raw_file_bool: bool, seasons_leagues: list[c.SeasonLeague]
) -> pd.DataFrame:
    list_file_path_and_season_league = [
        (get_fbref_file_path(file_type, raw_file_bool, season_league), season_league)
        for season_league in seasons_leagues
    ]
    dfs = []
    for file_path, season_league in list_file_path_and_season_league:
        df = pd.read_csv(file_path)
        df["season_league"] = season_league
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)

    return df


#### Expectancies ####


def load_match_expectancies_df(seasons_leagues: list[c.SeasonLeague]) -> pd.DataFrame:
    df_exp = pd.concat(
        [
            pd.read_csv(
                c.FilePath.FOOTBALL_DATA_EDITED
                + f"{season_league.season.season_str}-league-{season_league.league.league_id}-historic-odds.csv"
            )
            for season_league in seasons_leagues
        ],
        ignore_index=True,
    )
    df_exp = df_exp.assign(
        datetime=lambda x: pd.to_datetime(x.datetime),
        date=lambda x: x.datetime.dt.date,
        time=lambda x: x.datetime.dt.time,
    ).drop(columns=["datetime"])
    return df_exp


def add_expectancies(df: pd.DataFrame, df_exp: pd.DataFrame) -> pd.DataFrame:
    return df.merge(
        df_exp, how="left", on=["date", "home_team", "away_team"], validate="m:1"
    ).assign(
        team_exp=lambda x: np.where(x.home == 0, x.away_exp, x.home_exp),
        opp_team_exp=lambda x: np.where(x.home == 0, x.home_exp, x.away_exp),
    )


### Clean DataFrame ###


def split_positions(df: pd.DataFrame) -> pd.DataFrame:
    df_positions = df.position.str.split(",", expand=True)
    df_positions.columns = [f"position_{num}" for num in df_positions.columns]
    df = df.join(df_positions)
    return df


def position_to_generic_position(
    df: pd.DataFrame, position_column_name="position_0"
) -> pd.DataFrame:
    conditions = [
        (
            (df[position_column_name] == "LB")
            | (df[position_column_name] == "RB")
            | (df[position_column_name] == "DF")
        ),
        ((df[position_column_name] == "LM") | (df[position_column_name] == "RM")),
        ((df[position_column_name] == "RW") | (df[position_column_name] == "LW")),
    ]
    outcomes = [
        "FB",  # Full-back
        "WM",  # Wide-mid
        "W",  # Winger
    ]
    df["complex_position"] = df.position.values
    df["position"] = np.select(conditions, outcomes, df[position_column_name].values)
    return df


def add_frac_90(df: pd.DataFrame) -> pd.DataFrame:
    df["frac_90"] = df.minutes / 90.0
    return df


def add_home(df: pd.DataFrame) -> pd.DataFrame:
    df["home"] = np.where((df.squad == df.home_team), 1, 0)
    return df


def add_opp_team(df: pd.DataFrame) -> pd.DataFrame:
    df["opposition_team"] = np.where(
        (df.squad == df.home_team), df.away_team, df.home_team
    )
    return df


def drop_gk(df: pd.DataFrame) -> pd.DataFrame:
    return df.query("not position_0.str.startswith('GK')").reset_index(drop=True)


def drop_na_npxg(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["npxg"], ignore_index=True)


def drop_na_frac_90(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["frac_90"], ignore_index=True)


def add_league(df: pd.DataFrame) -> pd.DataFrame:
    df["league"] = np.vectorize(lambda x: x.league.league_id)(df.season_league)
    return df


def add_season(df: pd.DataFrame) -> pd.DataFrame:
    df["season"] = np.vectorize(lambda x: x.season.season_str)(df.season_league)
    return df


def add_npg(df: pd.DataFrame) -> pd.DataFrame:
    df["npg"] = df.goals - df.pens_made
    df.npxg = np.where(
        (df.npg != 0) & (df.npxg == 0), 0.03, df.npxg
    )  # npxg gets rounded to 0, but a non-penalty goal is scored
    return df


### Functions ###


def calc_main_position(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("player_id", as_index=False).agg(position=("position", mode))


def calc_main_squad(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("player_id", as_index=False).agg(squad=("squad", mode))
