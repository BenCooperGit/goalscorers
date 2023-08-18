class FilePath:
    pass


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

SEASONS = [
    Season("2022-2023"),
    Season("2021-2022"),
    Season("2020-2021"),
    Season("2019-2020"),
    Season("2018-2019"),
    Season("2017-2018"),
]

LEAGUES = [
    League(league_id=9, league_name="Premier-League", season_duration=2),
    League(league_id=10, league_name="Championship", season_duration=2),
    League(league_id=11, league_name="Serie-A", season_duration=2),
    League(league_id=12, league_name="La-Liga", season_duration=2),
    League(league_id=13, league_name="Ligue-1", season_duration=2),
    League(league_id=20, league_name="Bundesliga", season_duration=2),
]


# create seasons_leagues list constant that defines season leagues.
seasons_leagues = []
for season in SEASONS:
    for league in LEAGUES:
        if season.num_years() == league.season_duration:
            if season.start_year >= XG_DATA_START_YEAR[league.league_id]:
                season_league = SeasonLeague(
                    season=season, league=league, xg_league_bool=True
                )
            else:
                season_league = SeasonLeague(
                    season=season, league=league, xg_league_bool=False
                )

            seasons_leagues.append(season_league)

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
