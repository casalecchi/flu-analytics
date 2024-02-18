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
        self.players = []

    
    def _get_team_details(self) -> dict:
        data = get_json_data(f"https://api.sofascore.com/api/v1/team/{self.id}")
        details = data['team']
        return details


    # todos os jogadores de um time com nome e id
    # https://api.sofascore.com/api/v1/team/1961/players
    