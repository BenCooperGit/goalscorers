class FilePath:
    FBREF_RAW = r"C:\Users\benja\Documents\projects\goalscorers\data\files\raw\fbref\\"
    FBREF_EDITED = (
        r"C:\Users\benja\Documents\projects\goalscorers\data\files\edited\fbref\\"
    )


class League:
    def __init__(self, league_id: int, league_name: str, season_duration: int):
        self.league_id = league_id
        self.league_name = league_name
        self.season_duration = (
            season_duration  # 2 if league is played over 2 years, else 1
        )


class Season:
    def __init__(self, season_str: str):
        self.season_str = season_str
        self.start_year = int(season_str.split("-")[0])
        if "-" in season_str:
            self.end_year = int(season_str.split("-")[1])
        else:
            self.end_year = int(season_str.split("-")[1])

    def num_years(self) -> int:
        if self.end_year == self.start_year:
            return 1
        else:
            return 2


class SeasonLeague:
    def __init__(self, season: Season, league: League, xg_league_bool: bool):
        self.season = season
        self.league = league
        self.xg_league_bool = xg_league_bool


XG_DATA_START_YEAR = {
    9: 2018,
    10: 2017,
    11: 2017,
    12: 2017,
    13: 2017,
    20: 2017,
}

SEASON_22_23 = Season("2022-2023")
SEASON_21_22 = Season("2021-2022")
SEASON_20_21 = Season("2020-2021")
SEASON_19_20 = Season("2019-2020")
SEASON_18_19 = Season("2018-2019")
SEASON_17_18 = Season("2017-2018")

ENGLISH_PREMIER_LEAGUE = League(
    league_id=9, league_name="Premier-League", season_duration=2
)
ENGLISH_CHAMPIONSHIP = League(
    league_id=10, league_name="Championship", season_duration=2
)
ITALIAN_SERIE_A = League(league_id=11, league_name="Serie-A", season_duration=2)
SPANISH_LA_LIGA = League(league_id=12, league_name="La-Liga", season_duration=2)
FRENCH_LIGUE_1 = League(league_id=13, league_name="Ligue-1", season_duration=2)
GERMAN_BUNDESLIGA = League(league_id=20, league_name="Bundesliga", season_duration=2)

SEASONS_LEAGUES = [
    SeasonLeague(SEASON_22_23, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, GERMAN_BUNDESLIGA, xg_league_bool=True),
]

# SEASONS = [
#     Season("2022-2023"),
#     Season("2021-2022"),
#     Season("2020-2021"),
#     Season("2019-2020"),
#     Season("2018-2019"),
#     Season("2017-2018"),
# ]

# LEAGUES = [
#     League(league_id=9, league_name="Premier-League", season_duration=2),
#     League(league_id=10, league_name="Championship", season_duration=2),
#     League(league_id=11, league_name="Serie-A", season_duration=2),
#     League(league_id=12, league_name="La-Liga", season_duration=2),
#     League(league_id=13, league_name="Ligue-1", season_duration=2),
#     League(league_id=20, league_name="Bundesliga", season_duration=2),
# ]

# # create seasons_leagues list constant that defines season leagues.
# seasons_leagues = []
# for season in SEASONS:
#     for league in LEAGUES:
#         if season.num_years() == league.season_duration:
#             if season.start_year >= XG_DATA_START_YEAR[league.league_id]:
#                 season_league = SeasonLeague(
#                     season=season, league=league, xg_league_bool=True
#                 )
#             else:
#                 season_league = SeasonLeague(
#                     season=season, league=league, xg_league_bool=False
#                 )

#             seasons_leagues.append(season_league)

FOOTBALL_DATA_TO_FBREF_TEAM_NAME_MAP = {
    "Brighton": "Brighton & Hove Albion",
    "Cardiff": "Cardiff City",
    "Huddersfield": "Huddersfield Town",
    "Leeds": "Leeds United",
    "Leicester": "Leicester United",
    "Man City": "Manchester City",
    "Man United": "Manchester United",
    "Newcastle": "Newcastle United",
    "Norwich": "Norwich City",
    "Nott'm Forest": "Nottingham Forest",
    "Stoke": "Stoke City",
    "Swansea": "Swansea City",
    "Tottenham": "Tottenham Hotspur",
    "West Brom": "West Bromwich Albion",
    "West Ham": "West Ham United",
    "Wolves": "Wolverhamption Wanderers",
}
