package_paths = [r"C:\Users\benja\Documents\projects\goalscorers"]
import sys

for path in package_paths:
    sys.path.append(path)
# import goalscorer_package.constants as c
from goalscorer_package.constants import *
import goalscorer_package.data_cleaning as dc
import httpx
import bs4
from dataclasses import dataclass, asdict
import unicodedata
import datetime as dt
import pandas as pd
import numpy as np
import time

pd.set_option("display.max_columns", 1000)
pd.set_option("display.max_rows", 1000)
pd.set_option("max_colwidth", 100)

# seasons_leagues = [("2018-2019", 9, "Premier-League")]


@dataclass
class Fixture:
    url: str = None
    home_team: str = None
    away_team: str = None
    datetime: int = None
    home_team_manager: str = None
    away_team_manager: str = None
    stadium: str = None
    attendance: int = None


# def request_soup(url: str, max_tries=10) -> bs4.BeautifulSoup:
#     with httpx.Client() as client:
#         tries = 0
#         while tries < max_tries:
#             try:
#                 resp = client.get(url)
#                 tries = max_tries
#             except:
#                 tries += 1
#                 time.sleep(10)

#     soup = bs4.BeautifulSoup(resp, "html.parser")
#     return soup


def request_soup(
    url: str, func_validate_soup=lambda x: True, max_tries=10
) -> bs4.BeautifulSoup:
    with httpx.Client() as client:
        tries = 0
        while tries < max_tries:
            try:
                resp = client.get(url)
                soup = bs4.BeautifulSoup(resp, "html.parser")
                if func_validate_soup(soup):
                    tries = max_tries
                else:
                    tries += 1
                    time.sleep(10)
            except:
                tries += 1
                time.sleep(10)

    return soup


def create_fixtures(season: str, comp_id: int, comp_name: str) -> list[Fixture]:
    url = f"https://fbref.com/en/comps/{comp_id}/{season}/schedule/{season}-{comp_name}-Scores-and-Fixtures"
    soup = request_soup(url)

    # Get soup elements for score
    soup_table = soup.select("div.table_container")[0]
    soups_score = soup_table.find_all("td", attrs={"data-stat": "score"})
    soups_away_xg = soup_table.find_all("td", attrs={"data-stat": "away_xg"})

    # Add link to fixtures list
    fixtures = []
    for i, soup_score in enumerate(soups_score):
        soup_away_xg = soups_away_xg[i]
        if soup_score["class"] == ["center", "iz"]:  # is not fixture
            continue
        elif (
            soup_away_xg.text == ""
        ):  # fixture does not have stats (happens rarely, for example when a match is voided)
            continue
        else:
            fixtures.append(
                Fixture(url="https://fbref.com" + soup_score.find("a")["href"])
            )

    return fixtures


def validate_fixture_soup(soup: bs4.BeautifulSoup) -> bool:
    try:
        soup_scorebox = soup.find("div", {"class": "scorebox"})
        soup_home_scorebox = soup_scorebox.findChildren("div")[0]
        soup_scorebox_meta = soup_scorebox.find("div", {"class": "scorebox_meta"})
        datetime = soup_scorebox_meta.find("span")["data-venue-epoch"]
        return True
    except:
        return False


def add_fixture_info(fixture: Fixture, soup: bs4.BeautifulSoup) -> Fixture:
    # Get soup for scorebox
    soup_scorebox = soup.find("div", {"class": "scorebox"})
    soup_home_scorebox = soup_scorebox.findChildren("div")[0]
    soup_away_scorebox = soup_home_scorebox.find_next_sibling("div")

    # Add fixture info
    fixture.home_team = (
        soup_home_scorebox.select("div.media-item.logo")[0]
        .findNext("strong")
        .text.strip()
    )
    fixture.away_team = (
        soup_away_scorebox.select("div.media-item.logo")[0]
        .findNext("strong")
        .text.strip()
    )

    fixture.home_team_manager = unicodedata.normalize(
        "NFKD", soup_home_scorebox.find("div", {"class": "datapoint"}).text
    ).split("Manager: ")[-1]

    fixture.away_team_manager = unicodedata.normalize(
        "NFKD", soup_away_scorebox.find("div", {"class": "datapoint"}).text
    ).split("Manager: ")[-1]

    soup_scorebox_meta = soup_scorebox.find("div", {"class": "scorebox_meta"})
    fixture.datetime = int(soup_scorebox_meta.find("span")["data-venue-epoch"])

    try:
        fixture.attendance = int(
            soup_scorebox_meta.find_all("div")[4]
            .text.split("Attendance: ")[-1]
            .replace(",", "")
        )
        fixture.stadium = soup_scorebox_meta.find_all("div")[5].text.split("Venue: ")[
            -1
        ]
    except:  # covid - no attendance
        fixture.attendance = 0
        fixture.stadium = soup_scorebox_meta.find_all("div")[5].text.split("Venue: ")[
            -1
        ]

    return fixture


def parse_soup_table(fixture: Fixture, soup_table: bs4.BeautifulSoup) -> list[dict]:
    soup_table = soup_table.find("tbody")  # restrict table to tbody

    soup_table_rows = soup_table.find_all("tr")

    table_rows = []
    for soup_table_row in soup_table_rows:  # row in rows
        # filter out seperator rows
        if soup_table_row.has_attr("class"):
            if soup_table_row["class"] == ["spacer", "partial_table"]:
                continue

        soup_table_row_columns = soup_table_row.find_all("td")
        soup_table_row_columns.append(soup_table_row.find("th"))

        table_row = {
            "home_team": fixture.home_team,
            "away_team": fixture.away_team,
            "datetime": fixture.datetime,
        }
        for soup_table_row_column in soup_table_row_columns:  # columns in row
            data_stat = soup_table_row_column["data-stat"]

            # if player, take player-id
            if data_stat.endswith("player"):
                if soup_table_row_column.find("a"):
                    table_row[f"{data_stat}_id"] = soup_table_row_column.find("a")[
                        "href"
                    ].split("/")[-2]
                else:
                    table_row[f"{data_stat}_id"] = ""

            table_row[data_stat] = soup_table_row_column.text

        table_rows.append(table_row)

    return table_rows


def scrape(fixture: Fixture, soup: bs4.BeautifulSoup) -> tuple:
    print(fixture.url)

    # Get Fixture specific info
    fixture = add_fixture_info(fixture, soup)

    # Get all tables soups
    soup_tables = soup.select("table.stats_table.sortable")[: 17 - 2]  # all tables

    # Get player stats from table
    player_tables = []
    for i, soup_table in enumerate(soup_tables):
        player_tables.append(parse_soup_table(fixture, soup_table))

    return fixture, player_tables


def export_player_tables(all_player_tables: list, season: str, comp_id: int) -> None:
    table_name = {
        0: "summary",
        1: "passing",
        2: "pass-types",
        3: "defensive-actions",
        4: "possession",
        5: "miscellaneous-stats",
        6: "goalkeeper-stats",
        7: "summary",
        8: "passing",
        9: "pass-types",
        10: "defensive-actions",
        11: "possession",
        12: "miscellaneous-stats",
        13: "goalkeeper-stats",
        14: "shots",
    }

    player_tables = {
        "summary": [],
        "passing": [],
        "pass-types": [],
        "defensive-actions": [],
        "possession": [],
        "miscellaneous-stats": [],
        "goalkeeper-stats": [],
        "shots": [],
    }

    # Add players team to dataframe and combine same tables
    for i, all_player_table in enumerate(all_player_tables):
        df_all_player_table = pd.DataFrame(all_player_table)

        if i < 7:
            df_all_player_table["squad"] = df_all_player_table.home_team
        elif i < 13:
            df_all_player_table["squad"] = df_all_player_table.away_team

        player_tables[table_name[i]].append(df_all_player_table)

    # Add whether player started the match to dataframes
    # Add whether shot eas a pen in shots dataframe
    for k, v in player_tables.items():
        df = pd.concat(v)
        if k != "shots":
            df["start"] = np.where(
                df.player.str.startswith("\xa0\xa0\xa0"), False, True
            )
            df.player = df.player.str.strip()

        else:
            df["pen"] = np.where(df.player.str.endswith(" (pen)"), True, False)
            df["player"] = np.where(df.pen.values, df.player.str[:-6], df.player.values)

        df.to_csv(
            FilePath.FBREF_RAW + f"{season}-league-{comp_id}-{k}.csv", index=False
        )


def main(seasons_leagues: list) -> None:
    for season_league in seasons_leagues:
        season, comp_id, comp_name = (
            season_league.season.season_str,
            season_league.league.league_id,
            season_league.league.league_name,
        )

        # Get Url for all games
        fixtures = create_fixtures(season, comp_id, comp_name)

        all_fixture_info = []
        all_player_tables = [
            [] for _ in range(17 - 2)
        ]  # Only for season where each fixture has 17 tables

        for i, fixture in enumerate(fixtures):
            print(i + 1, "/", len(fixtures))

            # Sleep to avoid getting blocked (limit 30 requests per minute)
            time.sleep(3)

            # Request fixture soup
            soup = request_soup(fixture.url, validate_fixture_soup)

            # Scrape
            fixture, player_tables = scrape(fixture, soup)

            # Append
            all_fixture_info.append(fixture)
            for i in range(len(all_player_tables)):
                all_player_tables[i] += player_tables[i]

        # Export
        pd.DataFrame(all_fixture_info).to_csv(
            FilePath.FBREF_RAW + f"{season}-league-{comp_id}-fixture-info.csv",
            index=False,
        )
        export_player_tables(all_player_tables, season, comp_id)


if __name__ == "__main__":
    seasons_leagues = [
        # SeasonLeague(SEASON_17_18, EUROPEAN_EUROPA_LEAGUE, xg_league_bool=True),
        # SeasonLeague(SEASON_20, AMERICAN_MLS, xg_league_bool=True),
        SeasonLeague(SEASON_17_18, FRENCH_LIGUE_1, xg_league_bool=True),
    ]
    main(seasons_leagues)
