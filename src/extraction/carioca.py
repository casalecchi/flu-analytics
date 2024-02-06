from extraction import *
from extraction.fetchData import get_individual_stats_from_match, get_round_data_from_tournament, get_fetch_info

# --------- Esses métodos podem ser adaptados para outros campeonatos -----------

def get_df_from_carioca_round(round_number, teams_selected):
    """Return the data for a specific round from all teams selected in a DataFrame"""
    data = pd.DataFrame()
    carioca_round_data = get_round_data_from_tournament(Carioca, round_number)
    teams_info = get_fetch_info(carioca_round_data, CARIOCA_TEAMS_OBJ, teams_selected)
    for info in teams_info:
        team = CARIOCA_TEAMS_OBJ[info["name"]]
        id = info["id"]
        field = info["field"]
        try:
            team_data = get_individual_stats_from_match(id)
            team_df = get_df_from_team(team_data, field, team)
            data = pd.concat([data, team_df])
        except Exception as ex:
            print(f"Cannot find data for {team.name} match -> {ex}")

    return data

def get_df_from_team(data, field, team: Team):
    """Return a DataFrame with the stats from a specific team"""
    df = pd.DataFrame(columns=('name', 'position', 'primary_color', 'secondary_color', 'badge_url', 'avatar_url', *SofaStats.Individual_Stats, 'groundWon'))
    team_players = data[field]
    players = team_players["players"]
    for index, player in enumerate(players):
        name = player["player"]["name"]
        avatar_url = f"https://api.sofascore.com/api/v1/player/{player['player']['id']}/image"
        position = player.get("position", "")
        primary_color = team.primary_color
        secondary_color = team.secondary_color
        badge_url = team.badge
        df.loc[index]= [name, position, primary_color, secondary_color, badge_url, avatar_url, *[0.0 for _ in range(SofaStats.Num_Individual_Stats + 1)]]
        statistics = player.get("statistics", {})
        for attr in SofaStats.Individual_Stats:
            df.at[index, attr] = statistics.get(attr, 0)
        
        ground_won = statistics.get("duelWon", 0) - df.iloc[index]['aerialWon']
        df.at[index, 'groundWon'] = ground_won
        
    return df

def get_carioca_inputs():
    """Get Carioca inputs from user by the terminal."""
    choices = []
    for team in CARIOCA_TEAMS:
        choices.append(team.name.capitalize())

    questions = [
        inquirer.Text('round', message="Type the round of Carioca"),
        inquirer.Checkbox('teams', message="What teams you want to fetch data?",
                        choices=choices,
                        ),
        inquirer.Text('fname', message="Name the csv file (with .csv)"),
    ]

    answers = inquirer.prompt(questions)
    return answers
