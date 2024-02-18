from typing import List
from extraction.fetchData import get_team_data
from extraction.team import *


class Tournament:
    def __init__(self, name, unique_id, season_id):
        self.name = name
        self.unique_id = unique_id
        self.season_id = season_id
        self.team_ids = self._get_teams_ids_from_tournament()
        self.teams = self._get_teams()

    def _get_teams_ids_from_tournament(self) -> List[int]:
        ids = []
        data = get_json_data(f"https://api.sofascore.com/api/v1/unique-tournament/{self.unique_id}/season/{self.season_id}/team-events")
        tournament_team_events = data['tournamentTeamEvents']
        for team_obj in tournament_team_events.values():
            for id in team_obj.keys():
                id = int(id)
                ids.append(id)
            break
        return ids
    
    def _get_teams(self) -> List[Team]:
        teams_data = []
        for id in self.team_ids:
            new_team = Team(id)
            teams_data.append(new_team)
        return teams_data
    
    def find_team_by_id(self, team_id):
        for team in self.teams:
            if team.id == team_id:
                return team
    
    def get_tournament_stats_from_teams(self):
        df = pd.DataFrame(columns=('id', 'name', 'primary_color', 'secondary_color', 
                                   'badge_url', *SofaStats.Team_Stats))
        for index, team in enumerate(self.teams):
            data = get_team_data(team.id, self.unique_id, self.season_id)
            id = team.id
            name = team.name
            primary_color = team.primary_color
            secondary_color = team.secondary_color
            badge_url = team.badge
            df.loc[index] = [id, name, primary_color, secondary_color, badge_url, *[0.0 for _ in range(SofaStats.Num_Team_Stats)]]
            for attr in SofaStats.Team_Stats:
                df.at[index, attr] = data.get(attr, 0)
        
        return df
    
    def get_tournament_stats_from_player(self, player_name, player_id):
        data = get_player_data(player_id, self.unique_id, self.season_id)
        statistics = data['statistics']
        team_id = data['team']['id']
        team = self.find_team_by_id(team_id)
        df = pd.DataFrame(columns=('id', 'player_name', 'team_name', 'primary_color', 'secondary_color', 
                                   'badge_url', *SofaStats.Player_Stats_For_Tournament))
        team_name = team.name
        primary_color = team.primary_color
        secondary_color = team.secondary_color
        badge_url = team.badge
        df.loc[0] = [player_id, player_name, team_name, primary_color, secondary_color, badge_url, *[0.0 for _ in range(len(SofaStats.Player_Stats_For_Tournament))]]
        for attr in SofaStats.Player_Stats_For_Tournament:
            df.at[0, attr] = statistics.get(attr, 0)
        
        return df

    
    # estatisticas do campeonato inteiro 
    # https://api.sofascore.com/api/v1/team/1961/unique-tournament/92/season/56974/statistics/overall
    # top player por competição do time
    # https://api.sofascore.com/api/v1/team/1961/unique-tournament/92/season/56974/top-players/overall
    # ultimas partidas
    # https://api.sofascore.com/api/v1/team/1961/events/last/0
    # estatisticas de jogador por torneio
    # https://api.sofascore.com/api/v1/player/33238/unique-tournament/92/season/56974/statistics/overall