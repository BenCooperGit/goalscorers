class FilePath:
    FBREF_RAW = r"C:\Users\benja\Documents\projects\goalscorers\data\files\raw\fbref\\"
    FBREF_EDITED = (
        r"C:\Users\benja\Documents\projects\goalscorers\data\files\edited\fbref\\"
    )
    FOOTBALL_DATA_RAW = (
        r"C:\Users\benja\Documents\projects\goalscorers\data\files\raw\football-data\\"
    )
    FOOTBALL_DATA_EDITED = r"C:\Users\benja\Documents\projects\goalscorers\data\files\edited\football-data\\"


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
        self.end_year = int(season_str.split("-")[-1])

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

    def __str__(self):
        return f"{self.league.league_name} {self.season.season_str}"


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

SEASON_22 = Season("2022")
SEASON_21 = Season("2021")
SEASON_20 = Season("2020")
SEASON_19 = Season("2019")
SEASON_18 = Season("2018")

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

PORTUGUESE_PREMIERA_LIGA = League(
    league_id=32, league_name="Primeira-Liga", season_duration=2
)
DUTCH_ERIDIVISIE_LIGA = League(
    league_id=23, league_name="Eridivisie", season_duration=2
)
MEXICAN_LIGA_MX = League(league_id=31, league_name="Liga-MX", season_duration=2)

EUROPEAN_CHAMPIONS_LEAGUE = League(
    league_id=8, league_name="Champions-League", season_duration=2
)
EUROPEAN_EUROPA_LEAGUE = League(
    league_id=19, league_name="Europa-League", season_duration=2
)
EUROPEAN_EUROPA_CONFERENCE_LEAGUE = League(
    league_id=882, league_name="Europa-Conference-League", season_duration=2
)

AMERICAN_MLS = League(
    league_id=22, league_name="Major-League-Soccer", season_duration=1
)
BRAZILIAN_SERIE_A = League(league_id=24, league_name="Serie-A", season_duration=1)


SEASONS_LEAGUES = [
    # xG season leagues
    ## Top 5 and championship
    SeasonLeague(SEASON_22_23, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, FRENCH_LIGUE_1, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, FRENCH_LIGUE_1, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, FRENCH_LIGUE_1, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, FRENCH_LIGUE_1, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, ENGLISH_CHAMPIONSHIP, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, FRENCH_LIGUE_1, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, GERMAN_BUNDESLIGA, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, ENGLISH_PREMIER_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, ITALIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, SPANISH_LA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, FRENCH_LIGUE_1, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, GERMAN_BUNDESLIGA, xg_league_bool=True),
    ## Lesser leagues
    SeasonLeague(SEASON_22_23, PORTUGUESE_PREMIERA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, DUTCH_ERIDIVISIE_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, MEXICAN_LIGA_MX, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, PORTUGUESE_PREMIERA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, DUTCH_ERIDIVISIE_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, MEXICAN_LIGA_MX, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, PORTUGUESE_PREMIERA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, DUTCH_ERIDIVISIE_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, MEXICAN_LIGA_MX, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, PORTUGUESE_PREMIERA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, DUTCH_ERIDIVISIE_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, MEXICAN_LIGA_MX, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, PORTUGUESE_PREMIERA_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, DUTCH_ERIDIVISIE_LIGA, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, MEXICAN_LIGA_MX, xg_league_bool=True),
    ## European competitions
    SeasonLeague(SEASON_22_23, EUROPEAN_CHAMPIONS_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, EUROPEAN_EUROPA_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_22_23, EUROPEAN_EUROPA_CONFERENCE_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, EUROPEAN_CHAMPIONS_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, EUROPEAN_EUROPA_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_21_22, EUROPEAN_EUROPA_CONFERENCE_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, EUROPEAN_CHAMPIONS_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_20_21, EUROPEAN_EUROPA_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, EUROPEAN_CHAMPIONS_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_19_20, EUROPEAN_EUROPA_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, EUROPEAN_CHAMPIONS_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_18_19, EUROPEAN_EUROPA_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, EUROPEAN_CHAMPIONS_LEAGUE, xg_league_bool=True),
    SeasonLeague(SEASON_17_18, EUROPEAN_EUROPA_LEAGUE, xg_league_bool=True),
    ## 1 year leagues
    SeasonLeague(SEASON_22, AMERICAN_MLS, xg_league_bool=True),
    SeasonLeague(SEASON_22, BRAZILIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_21, AMERICAN_MLS, xg_league_bool=True),
    SeasonLeague(SEASON_21, BRAZILIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_20, AMERICAN_MLS, xg_league_bool=True),
    SeasonLeague(SEASON_20, BRAZILIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_19, AMERICAN_MLS, xg_league_bool=True),
    SeasonLeague(SEASON_19, BRAZILIAN_SERIE_A, xg_league_bool=True),
    SeasonLeague(SEASON_18, AMERICAN_MLS, xg_league_bool=True),
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
    # Prem
    "Brighton": "Brighton & Hove Albion",
    "Cardiff": "Cardiff City",
    "Huddersfield": "Huddersfield Town",
    "Leeds": "Leeds United",
    "Leicester": "Leicester City",
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
    "Wolves": "Wolverhampton Wanderers",
    # Serie A
    "Verona": "Hellas Verona",
    "Inter": "Internazionale",
    "spal": "SPAL",
    # La Liga
    "Alaves": "Alavés",
    "Almeria": "Almería",
    "Ath Bilbao": "Athletic Club",
    "Ath Madrid": "Atlético Madrid",
    "Betis": "Real Betis",
    "Cadiz": "Cádiz",
    "Celta": "Celta Vigo",
    "Espanol": "Espanyol",
    "La Coruna": "Deportivo La Coruña",
    "Leganes": "Leganés",
    "Malaga": "Málaga",
    "Sociedad": "Real Sociedad",
    "Vallecano": "Rayo Vallecano",
    # Ligue 1
    "Clermont": "Clermont Foot",
    "Nimes": "Nîmes",
    "Paris SG": "Paris Saint-Germain",
    "St Etienne": "Saint-Étienne",
    # Bundesliga
    "Bielefeld": "Arminia",
    "Ein Frankfurt": "Eintracht Frankfurt",
    "FC Koln": "Köln",
    "Fortuna Dusseldorf": "Düsseldorf",
    "Greuther Furth": "Greuther Fürth",
    "Hamburg": "Hamburger SV",
    "Hannover": "Hannover 96",
    "Hertha": "Hertha BSC",
    "Leverkusen": "Bayer Leverkusen",
    "M'gladbach": "Mönchengladbach",
    "Mainz": "Mainz 05",
    "Nurnberg": "Nürnberg",
    "Paderborn": "Paderborn 07",
    # Championship
    "Birmingham": "Birmingham City",
    "Blackburn": "Blackburn Rovers",
    "Bolton": "Bolton Wanderers",
    "Cardiff": "Cardiff City",
    "Charlton": "Charlton Athletic",
    "Coventry": "Coventry City",
    "Derby": "Derby County",
    "Huddersfield": "Huddersfield Town",
    "Hull": "Hull City",
    "Ipswich": "Ipswich Town",
    "Leeds": "Leeds United",
    "Luton": "Luton Town",
    "Norwich": "Norwich City",
    "Nott'm Forest": "Nottingham Forest",
    "Peterboro": "Peterborough United",
    "Preston": "Preston North End",
    "QPR": "Queens Park Rangers",
    "Rotherham": "Rotherham United",
    "Sheffield Weds": "Sheffield Wednesday",
    "Stoke": "Stoke City",
    "Swansea": "Swansea City",
    "West Brom": "West Bromwich Albion",
    "Wigan": "Wigan Athletic",
    "Wycombe": "Wycombe Wanderers",
}
