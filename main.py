from utils import *
from pprint import pprint
import pandas as pd
import requests


match_url = "https://www.sofascore.com/audax-rj-fluminense/lOsQgJ#id:11873046"#input('Digite a URL da partida que deseja pegar as estatísiticas de duelos: ')
match_id = get_match_id(match_url)
json_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
response = requests.get(json_url, headers=HEADERS)
data = response.json()

home_team = data["home"]
home_players = home_team["players"]
for player in home_players:
    name = player["player"]["name"]
    position = player["position"]
    statistics = player["statistics"]
    aerial_won = statistics["aerialWon"]
    ground_won = statistics["duelWon"] - aerial_won
    total_clearence = statistics["totalClearance"]
    interceptions = statistics["interceptionWon"]
    break

