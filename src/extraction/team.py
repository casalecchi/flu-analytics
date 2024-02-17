from extraction import *
from extraction.sofastats import *
from extraction.fetchData import *


class Team:
    def __init__(self, id, third_color=""):
        self.id = id
        self.team_details = self._get_team_details()
        self.name = self.team_details['name']
        self.primary_color = self.team_details['teamColors']['primary']
        self.secondary_color = self.team_details['teamColors']['secondary']
        self.badge = f"https://api.sofascore.com/api/v1/team/{self.id}/image"
        self.third_color = third_color
    
    def _get_team_details(self) -> object:
        # data = requests.get(f"https://api.sofascore.com/api/v1/team/{self.id}", headers=HEADERS).json()
        data = get_json_data(f"https://api.sofascore.com/api/v1/team/{self.id}")
        details = data['team']
        return details

    def get_df_from_team(self, data, field):
        """Return a DataFrame with the stats from a specific team"""
        df = pd.DataFrame(columns=('name', 'team', 'position', 'primary_color', 'secondary_color', 'badge_url', 'avatar_url', *SofaStats.Individual_Stats, 'groundWon'))
        team_players = data[field]
        players = team_players["players"]
        for index, player in enumerate(players):
            name = player["player"]["name"]
            team = self.name
            avatar_url = f"https://api.sofascore.com/api/v1/player/{player['player']['id']}/image"
            position = player.get("position", "")
            primary_color = self.primary_color
            secondary_color = self.secondary_color
            badge_url = self.badge
            df.loc[index]= [name, team, position, primary_color, secondary_color, badge_url, avatar_url, *[0.0 for _ in range(SofaStats.Num_Individual_Stats + 1)]]
            statistics = player.get("statistics", {})
            for attr in SofaStats.Individual_Stats:
                df.at[index, attr] = statistics.get(attr, 0)
            
            ground_won = statistics.get("duelWon", 0) - df.iloc[index]['aerialWon']
            df.at[index, 'groundWon'] = ground_won
            
        return df
    