import pandas as pd
import numpy as np


def create_league_masks(
    df_model: pd.DataFrame, teams: list[str], leagues: list[int]
) -> list[list]:
    df_team_league = (
        df_model[["opposition_team", "league"]]
        .drop_duplicates(ignore_index=True)
        .rename(columns={"opposition_team": "team"})
    )
    df_team_league.index = df_team_league.team
    df_team_league = df_team_league.loc[teams]

    league_masks = []
    for league in leagues:
        league_mask = []
        for l in df_team_league.league.values:
            if l == league:
                league_mask.append(1)
            else:
                league_mask.append(0)
        league_masks.append(league_mask)

    return league_masks
