from utils import *


def get_data_from_matches(round_number, teams_selected):
    data = pd.DataFrame()
    round_data = get_round_data(round_number)
    teams_info = get_fetch_info(round_data, teams_selected)
    for info in teams_info:
        team = TEAMS_OBJ[info["name"]]
        id = info["id"]
        field = info["field"]
        try:
            team_data = get_data_from_event_lineups(id)
            team_df = get_df_from_team(team_data, field, team)
            data = pd.concat([data, team_df])
        except:
            print(f"Cannot find data for {team.name} match")

    return data

def get_data_from_event_lineups(match_id):
    json_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
    return get_data(json_url)

def get_df_from_team(data, field, team: Team):
    df = pd.DataFrame(columns=('name', 'position', 'primary_color', 'secondary_color', 'badge', 'avatar_url', *Statistics.Attributes, 'groundWon'))
    team_players = data[field]
    players = team_players["players"]
    for index, player in enumerate(players):
        name = player["player"]["name"]
        avatar_url = f"https://api.sofascore.com/api/v1/player/{player["player"]["id"]}/image"
        position = player["position"]
        primary_color = team.primary_color
        secondary_color = team.secondary_color
        badge = team.badge
        df.loc[index]= [name, position, primary_color, secondary_color, badge, avatar_url, *[0.0 for _ in range(Statistics.Num_attributes + 1)]]
        statistics = player.get("statistics", {})
        for attr in Statistics.Attributes:
            df.at[index, attr] = statistics.get(attr, 0)
        
        ground_won = statistics.get("duelWon", 0) - df.iloc[index]['aerialWon']
        df.at[index, 'groundWon'] = ground_won
        
    return df

def get_data(url):
    response = requests.get(url, stream=True, headers=HEADERS)
    return response.json()

def get_data_inputs():
    choices = []
    for team in TEAMS:
        choices.append(team.name.capitalize())

    questions = [
        inquirer.Text('round', message="Type the round of Carioca"),
        inquirer.Checkbox('teams', message="What teams you want to fetch data?",
                        choices=choices,
                        ),
        inquirer.Text('fname', message="Name the csv file"),
        #inquirer.List('attr', message="Select the statistics for the chart")
    ]

    answers = inquirer.prompt(questions)
    return answers

def get_round_data(round_number):
    url = f"https://api.sofascore.com/api/v1/unique-tournament/92/season/56974/events/round/{round_number}"
    data = get_data(url)
    try:
        # return list of matches
        return data["events"]
    except:
        print(f"Cannot find data from round {round_number}")

def get_team_props(name, id, field) -> object:
    return {
        "name"  : name.upper(),
        "id"    : id,
        "field" : field,
    }

def get_fetch_info(round_data: object, teams):
    info = []
    for match in round_data:
        for team in teams:
            field = ""
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]
            if home == team:
                field = "home"
                team_obj = get_team_props(team, match["id"], field)
                info.append(team_obj)
                break
            elif away == team:
                field = "away"
                team_obj = get_team_props(team, match["id"], field)
                info.append(team_obj)
                break

    return info