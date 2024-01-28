from utils import *
from pprint import pprint
import pandas as pd
import requests


match_url = "https://www.sofascore.com/audax-rj-fluminense/lOsQgJ#id:11873046"#input('Digite a URL da partida que deseja pegar as estatísiticas de duelos: ')
match_id = get_match_id(match_url)
json_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
response = requests.get(json_url, headers=HEADERS)
data = response.json()

home_df = pd.DataFrame(columns=('name', 'position', 'aerial_won', 'ground_won', 'clearences', 'interceptions'))
home_team = data["home"]
home_players = home_team["players"]
for index, player in enumerate(home_players):
    name = player["player"]["name"]
    position = player["position"]
    statistics = player.get("statistics", {})
    aerial_won = statistics.get("aerialWon", 0)
    ground_won = statistics.get("duelWon", 0) - aerial_won
    total_clearence = statistics.get("totalClearance", 0)
    interceptions = statistics.get("interceptionWon", 0)
    home_df.loc[index] = [name, position, aerial_won, ground_won, total_clearence, interceptions]

home_df.to_csv('teste.csv')

