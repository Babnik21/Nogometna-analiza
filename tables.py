import pandas
from glob import glob


# Doda ekipo (vrstico) v lestvico sezone
def add_row(games, df, team_name):
    home_games = games[games["team"] == team_name]
    away_games = games[games["opponent"] == team_name]
    goals = sum(home_games["goals"]) + sum(away_games["opponent goals"])
    opp_goals = sum(home_games["opponent goals"]) + sum(away_games["goals"])
    goal_diff = goals - opp_goals
    wins = len(home_games[home_games["goals"] > home_games["opponent goals"]].index) + \
        len(away_games[away_games["goals"] < away_games["opponent goals"]].index)
    draws = len(home_games[home_games["goals"] == home_games["opponent goals"]].index) + \
        len(away_games[away_games["goals"] == away_games["opponent goals"]].index)
    losses = len(home_games.index) + len(away_games.index) - wins - draws
    points = 3 * wins + draws
    row = pandas.DataFrame([[points, goal_diff, goals, opp_goals, wins, draws, losses]], \
        columns = ["PTS", "Goal Difference", "Goals", "Goals against", "Wins", "Draws", "Losses"], \
        index = [team_name])
    return pandas.concat([df, row])

# Vrne lestvico sezone
def get_table(games):
    teams = set(games["team"].tolist())
    table = pandas.DataFrame()
    for team in teams:
        table = add_row(games, table, team)
    return table.sort_values(by = "PTS", ascending=False)

#Seznam poti za vsako sezono
season_paths = glob("data/input/*.csv")

# Lestvica za vsako sezono
def make_tables(paths):
    for path in paths:
        matches = pandas.read_csv(path)
        path_2 = "data/tables" + path[4:]
        table = get_table(matches)
        table.to_csv(path_2, index=True)


# Ustvari vse lestvice (iz vseh sezon, za katere so na voljo podatki)
make_tables(season_paths)


