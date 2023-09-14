package_paths = [r"C:\Users\benja\Documents\projects\goalscorers"]
import sys

for path in package_paths:
    sys.path.append(path)
from goalscorer_package.constants import *
import goalscorer_package.data_cleaning as dc
import datetime as dt
import pandas as pd
import numpy as np
import scipy
import glob

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_colwidth", 100)
pd.options.display.float_format = "{: ,.3f}".format

# DATA


def add_datetime(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        # Convert "date" and "time" columns to datetime format
        # date=lambda x: pd.to_datetime(x.Date, format="%d/%m/%Y"),
        date=lambda x: pd.to_datetime(x.Date, format="mixed"),
        time=lambda x: pd.to_datetime(x.Time, format="%H:%M").dt.time
        if "Time" in x.columns
        else [dt.time(0, 0, 0, 0) for _ in range(len(x))],
        # Combine "date" and "time" columns to create "datetime" columns
        datetime=lambda x: pd.to_datetime(
            x.date.astype(str) + " " + x.time.astype(str)
        ),
    )


def add_fbref_team_names(df: pd.DataFrame) -> pd.DataFrame:
    df_home_team_name_map = pd.DataFrame(
        {
            "team_home": FOOTBALL_DATA_TO_FBREF_TEAM_NAME_MAP.keys(),
            "home_team": FOOTBALL_DATA_TO_FBREF_TEAM_NAME_MAP.values(),
        }
    )
    df_away_team_name_map = pd.DataFrame(
        {
            "team_away": FOOTBALL_DATA_TO_FBREF_TEAM_NAME_MAP.keys(),
            "away_team": FOOTBALL_DATA_TO_FBREF_TEAM_NAME_MAP.values(),
        }
    )
    return (
        df.merge(df_home_team_name_map, how="left", on=["team_home"], validate="m:1")
        .merge(df_away_team_name_map, how="left", on=["team_away"], validate="m:1")
        .assign(
            home_team=lambda x: x.home_team.fillna(x.team_home),
            away_team=lambda x: x.away_team.fillna(x.team_away),
        )
    )


def data(season_league: SeasonLeague) -> pd.DataFrame:
    season, comp_id = season_league.season.season_str, season_league.league.league_id

    file_path = (
        FilePath.FOOTBALL_DATA_RAW + f"{season}-league-{comp_id}-historic-odds.csv"
    )
    # file_path = FilePath.FOOTBALL_DATA_RAW + "2020-20201-league-9-historic-odds.csv"

    df = pd.read_csv(file_path)
    df = add_datetime(df)
    return df


# MATHS


def odds_to_probs(odds: np.array) -> np.array:
    probs = 1.0 / odds
    probs = probs / np.sum(probs)
    return probs


def calc_score_matrix(home_exp: float, away_exp: float, max_goals=10) -> np.array:
    home_team_goals = scipy.stats.poisson.pmf(np.arange(0, max_goals + 1), home_exp)
    away_team_goals = scipy.stats.poisson.pmf(np.arange(0, max_goals + 1), away_exp)
    score_matrix = np.outer(home_team_goals, away_team_goals)
    return score_matrix


def wdw_probabilities(
    score_matrix: np.array,
) -> np.array:  # [home_win_prob, draw_prob, away_win_prob]
    home_win_prob = np.tril(score_matrix, -1).sum()
    draw_prob = np.diag(score_matrix).sum()
    away_win_prob = np.triu(score_matrix, 1).sum()
    return np.array([home_win_prob, draw_prob, away_win_prob])


def ou_probabilities(
    score_matrix: np.array, line=2.5
) -> np.array:  # [over_prob, under_prob]
    under_prob = 0
    for home_goals in range(int(np.floor(line)) + 1):
        for away_goals in range(int(np.floor(line)) + 1 - home_goals):
            under_prob += score_matrix[home_goals][away_goals]
    over_prob = 1.0 - under_prob
    return np.array([over_prob, under_prob])


def params_to_vars(params: np.array) -> tuple:
    home_exp, away_exp = params[0], params[1]
    return home_exp, away_exp


def _mse(params: np.array, wdw_obs: np.array, ou_obs: np.array) -> float:
    exp_params = np.exp(params)

    home_exp, away_exp = params_to_vars(exp_params)

    score_matrix = calc_score_matrix(home_exp, away_exp)

    wdw_probs = wdw_probabilities(score_matrix)
    ou_probs = ou_probabilities(score_matrix)

    pred = np.concatenate([wdw_probs, ou_probs])
    obs = np.concatenate([wdw_obs, ou_obs])

    mse = np.sum((pred - obs) ** 2)

    return mse


def goal_expectation(
    home_odds: float,
    draw_odds: float,
    away_odds: float,
    over_odds: float,
    under_odds: float,
) -> dict:
    wdw_odds = np.array([home_odds, draw_odds, away_odds])
    ou_odds = np.array([over_odds, under_odds])

    wdw_obs = odds_to_probs(wdw_odds)
    ou_obs = odds_to_probs(ou_odds)

    options = {
        "maxiter": 1000,
        "disp": False,
    }

    res = scipy.optimize.minimize(
        fun=_mse, x0=[1.5, 0.75], args=(wdw_obs, ou_obs), options=options
    )

    output = {
        "home_exp": res["x"][0],
        "away_exp": res["x"][1],
        "error": res["fun"],
        "success": res["success"],
    }

    return output


def get_ou_book(row: dict) -> str:
    if "P<2.5" in row:
        if np.isnan(row["P<2.5"]) == False:
            return "P"
    if "PC<2.5" in row:
        if np.isnan(row["PC<2.5"]) == False:
            return "PC"
    if "BbMx<2.5" in row:
        if np.isnan(row["BbMx<2.5"]) == False:
            return "BbMx"
    if "Max<2.5" in row:
        if np.isnan(row["Max<2.5"]) == False:
            return "Max"


def get_wdw_book(row: dict) -> str:
    if "PSH" in row:
        if np.isnan(row["PSH"]) == False:
            return "PS"
    if "MaxH" in row:
        if np.isnan(row["MaxH"]) == False:
            return "Max"
    if "BbMxH" in row:
        if np.isnan(row["BbMxH"]) == False:
            return "BbMx"
    if "PSCH" in row:
        if np.isnan(row["PSCH"]) == False:
            return "PSC"
    if "MaxCH" in row:
        if np.isnan(row["MaxCH"]) == False:
            return "MaxC"


def odds_to_xg(df: pd.DataFrame) -> pd.DataFrame:
    output = list()
    for _, row in df.iterrows():
        ou_book = get_ou_book(row)
        wdw_book = get_wdw_book(row)

        res = goal_expectation(
            row[f"{wdw_book}H"],
            row[f"{wdw_book}D"],
            row[f"{wdw_book}A"],
            row[f"{ou_book}>2.5"],
            row[f"{ou_book}<2.5"],
        )

        tmp = {
            "datetime": row["datetime"],
            "team_home": row["HomeTeam"],
            "team_away": row["AwayTeam"],
            "home_exp": np.exp(res["home_exp"]),
            "away_exp": np.exp(res["away_exp"]),
            "success": res["success"],
            "error": res["error"],
        }

        output.append(tmp)

    df_output = pd.DataFrame(output)
    return df_output


def print_failed_rows(df_exp: pd.DataFrame) -> None:
    df_failed = df_exp.query("success == False")
    if len(df_failed) > 0:
        print(
            "Failed rows:",
            "\n",
        )


def main(seasons_leagues: list[SeasonLeague]) -> None:
    for season_league in seasons_leagues:
        print(season_league)

        df = data(season_league)

        df_exp = odds_to_xg(df)

        df_exp = add_fbref_team_names(df_exp)

        season, comp_id = (
            season_league.season.season_str,
            season_league.league.league_id,
        )
        df_exp.to_csv(
            FilePath.FOOTBALL_DATA_EDITED
            + f"{season}-league-{comp_id}-historic-odds.csv",
            index=False,
        )

        print_failed_rows(df_exp)

    print("Complete", "\n")


if __name__ == "__main__":
    seasons_leagues = [
        SeasonLeague(SEASON_21_22, GERMAN_BUNDESLIGA, xg_league_bool=True),
    ]
    main(seasons_leagues)
