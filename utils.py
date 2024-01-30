import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.offsetbox import OffsetImage,AnnotationBbox

from Team import *


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

TEAMS = [Botafogo, Flamengo, Fluminense, Vasco]

def get_data_from_matches():
    data = pd.DataFrame()
    for team in TEAMS:
        url = input(f"Type the URL from this round {team.name} game: ")
        field = input(f"{team.name} is [home] or [away]? ")
        match_id = get_match_id(url)
        try:
            team_data = get_data_from_event_lineups(match_id)
            team_df = get_df_from_team(team_data, field, team)
            data = pd.concat([data, team_df])
        except:
            print("erro na url")
    
    return data

def get_data_from_event_lineups(match_id):
    json_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    response = requests.get(json_url, headers=HEADERS)
    return response.json()

def get_match_id(match_url):
    id_index = match_url.find('id') + 3
    return match_url[id_index:] 

def get_df_from_team(data, field, team: Team):
    df = pd.DataFrame(columns=('name', 'position', 'aerial_won', 'ground_won', 'clearences', 'interceptions', 'primary_color', 'secondary_color', 'badge'))
    team_players = data[field]
    players = team_players["players"]
    for index, player in enumerate(players):
        name = player["player"]["name"]
        position = player["position"]
        statistics = player.get("statistics", {})
        aerial_won = statistics.get("aerialWon", 0)
        ground_won = statistics.get("duelWon", 0) - aerial_won
        total_clearence = statistics.get("totalClearance", 0)
        interceptions = statistics.get("interceptionWon", 0)
        primary_color = team.primary_color
        secondary_color = team.secondary_color
        badge = team.badge
        df.loc[index] = [name, position, aerial_won, ground_won, total_clearence, interceptions, primary_color, secondary_color, badge]
    
    return df

def generate_bar_from_data(data, column, title, k=10):
    plt.figure(figsize=(24,6), facecolor="#EEE9E4") 
    ax = plt.axes()
    ax.set_facecolor("#EEE9E4")

    plt.bar(
        data["name"].head(10), data[column].head(k),
        color=data["primary_color"].head(k),
        edgecolor=data["secondary_color"].head(k),
        width=0.7,
        linewidth=5,
    )

    for i in range(k):
        valor = data.iloc[i][column]
        plt.text(x=i,
                y=valor - 2,
                s = str(valor),
                backgroundcolor='#EEE9E4',
                ha='center',
                fontsize=22,
                )
        img = plt.imread(data.iloc[i]['badge'])
        im = OffsetImage(img, zoom=0.9)
        im.image.axes = ax
        ab = AnnotationBbox(im, (i, 0),  xybox=(i, valor - 4), frameon=False,
                            xycoords='data', pad=0)
        ax.add_artist(ab)
        
        
    plt.title(title, fontsize=24)
    plt.savefig(f'{title}.png')