import matplotlib.pyplot as plt
import pandas as pd
import requests
import shutil
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
from PIL import Image, ImageDraw

from Team import *


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

TEAMS = [Botafogo, Flamengo, Fluminense, Vasco]

def crop_img(path):
    img = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", img.size, (0,0,0,0))

    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,150,150), fill='green', outline=None)

    new_img = Image.composite(img, background, mask)
    new_img.save('image.png')

def fetch_img(url):
    response = requests.get(url, stream=True, headers=HEADERS)
    if response.status_code == 200:
        f = open('image.jpg', 'wb')
        shutil.copyfileobj(response.raw, f)
        f.close()
        crop_img('image.jpg')
        return 'image.png'
    else:
        crop_img('img/player.png')
        return 'img/player.png'

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
    df = pd.DataFrame(columns=('name', 'position', 'aerial_won', 'ground_won', 'clearences', 'interceptions', 'primary_color', 'secondary_color', 'badge', 'avatar_url'))
    team_players = data[field]
    players = team_players["players"]
    for index, player in enumerate(players):
        name = player["player"]["name"]
        avatar_url = f"https://api.sofascore.com/api/v1/player/{player["player"]["id"]}/image"
        position = player["position"]
        statistics = player.get("statistics", {})
        aerial_won = statistics.get("aerialWon", 0)
        ground_won = statistics.get("duelWon", 0) - aerial_won
        total_clearence = statistics.get("totalClearance", 0)
        interceptions = statistics.get("interceptionWon", 0)
        primary_color = team.primary_color
        secondary_color = team.secondary_color
        badge = team.badge
        df.loc[index] = [name, position, aerial_won, ground_won, total_clearence, interceptions, primary_color, secondary_color, badge, avatar_url]
    
    return df

def generate_bar_from_data(data, column, title, k=10):
    plt.figure(figsize=(24,6), facecolor="#EEE9E4") 
    ax = plt.axes()
    ax.set_facecolor("#EEE9E4")

    plt.bar(
        data["name"].head(10), data[column].head(k),
        color=data["primary_color"].head(k),
        edgecolor=data["secondary_color"].head(k),
        width=0.5,
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
        badge = plt.imread(data.iloc[i]['badge'])
        offset_badge = OffsetImage(badge, zoom=0.9)
        offset_badge.image.axes = ax
        ab = AnnotationBbox(offset_badge, (i, 0),  xybox=(i, valor - 4), frameon=False,
                            xycoords='data', pad=0)
        ax.add_artist(ab)

        img_path = fetch_img(data.iloc[i]['avatar_url'])
        avatar = plt.imread(img_path)
        offset_avatar = OffsetImage(avatar, zoom=0.4)
        offset_avatar.image.axes = ax
        ab = AnnotationBbox(offset_avatar, (i, 0),  xybox=(i, -3.5), frameon=True,
                        xycoords='data', pad=0, bboxprops={'boxstyle': 'circle', 
                                                           'ec': data.iloc[i]["primary_color"],
                                                           'linewidth': 3})
        ax.add_artist(ab)
        
    def format_names(x, _):
        name = data.iloc[x]['name'].split(' ')
        return " ".join(name[0:2])
    
    plt.xticks(fontsize=19)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_names))
    ax.set_yticks([])
    plt.title(title, fontsize=24)
    plt.savefig(f'{title}.png', bbox_inches = 'tight')