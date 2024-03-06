from extraction.team import *
from extraction.sofastats import *


class Tournament:
    """Class for fetching live data from a tournament in Sofascore.
    It must be provided two Id's, the unique and season id. Both can be
    found on the url link of the tournament on sofascore site."""

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
        """Get teams from a tournament"""
        teams_data = []
        for id in tqdm(self.team_ids, desc=f"Creating teams from {self.name}"):
            new_team = Team(id)
            teams_data.append(new_team)
        return teams_data
    
    def _get_players_from_team(self, team: Team) -> dict:
        """Return a dict with key - player id and value - player name from a specific team"""
        players_id_name = {}
        data = get_json_data(f"https://api.sofascore.com/api/v1/team/{team.id}/unique-tournament/{self.unique_id}/season/{self.season_id}/top-players/overall")
        players = data["topPlayers"]["rating"]
        for player in players:
            infos = player['player']
            id = infos['id']
            name = infos['name'] # shortName also avaiable
            players_id_name[id] = name
        
        return players_id_name
    
    def _find_team_by_id(self, team_id):
        """Given a team id, find on tournament teams that team"""
        for team in self.teams:
            if team.id == team_id:
                return team
            
    def fetch_live_tournament_player_heatmap(self, player_id):
        """Return a DataFrame with all tournament event coordinates from a player. Columns in the 
        DataFrame: player_id, x, y and count.

        The x and y coordinates varies between 0 and 1, so when plotting, it has to be multiplied by
        width and height of the pitch. The count column represent the number of time an event has 
        happened on that coordinate."""
        points_data = get_tournament_heatmap(player_id, self.unique_id, self.season_id)
        points = points_data.get('points', [])
        df = pd.DataFrame(columns=('player_id', 'x', 'y', 'count'))
        for index, point in enumerate(points):
            x = point['x'] / 100
            y = point['y'] / 100
            count = point['count']
            df.loc[index] = [player_id, x, y, count]
        
        return df

    def fetch_live_tournament_stats_from_teams(self):
        """Return a DataFrame containing the accumulate statistics from all teams from tournament"""
        df = pd.DataFrame(columns=('team_id', 'name', 'primary_color', 'secondary_color', 
                                   'badge_url', *SofaStats.Team_Stats_For_Tournament))
        df.set_index('team_id', inplace=True)
        for team in tqdm(self.teams, desc="Fetching stats from teams..."):
            data = get_team_data(team.id, self.unique_id, self.season_id)
            id = team.id
            name = team.name
            primary_color = team.primary_color
            secondary_color = team.secondary_color
            badge_url = team.badge
            df.loc[id] = [name, primary_color, secondary_color, badge_url, *[0.0 for _ in range(len(SofaStats.Team_Stats_For_Tournament))]]
            for attr in SofaStats.Team_Stats_For_Tournament:
                df.at[id, attr] = data.get(attr, 0)
        
        return df
    
    def fetch_live_tournament_stats_from_player(self, player_name, player_id):
        """Return a DataFrame containing the accumulate stats from a given player"""
        data = get_player_data(player_id, self.unique_id, self.season_id)
        if 'error' in data:
            print(f"Cannot find {self.name} data for {player_name}")
            return pd.DataFrame()
        
        statistics = data.get('statistics', {})
        team_id = data['team']['id']
        team = self._find_team_by_id(team_id)
        df = pd.DataFrame(columns=('player_id', 'player_name', 'team_name', 'primary_color', 'secondary_color', 
                                   'badge_url', 'avatar_url', *SofaStats.Player_Stats_For_Tournament))
        df.set_index('player_id', inplace=True)
        team_name = team.name
        primary_color = team.primary_color
        secondary_color = team.secondary_color
        badge_url = team.badge
        avatar_url = f"https://api.sofascore.com/api/v1/player/{player_id}/image"
        df.loc[player_id] = [player_name, team_name, primary_color, secondary_color, badge_url, avatar_url, 
                             *[0.0 for _ in range(len(SofaStats.Player_Stats_For_Tournament))]]
        for attr in SofaStats.Player_Stats_For_Tournament:
            df.at[player_id, attr] = statistics.get(attr, 0)
        
        return df
    
    def fetch_live_tournament_stats_from_all_players(self):
        """Return a DataFrame containing the accumulate stats from all players from tournament"""
        df = pd.DataFrame()
        for team in self.teams:
            team.players = self._get_players_from_team(team)
            for id, name in tqdm(team.players.items(), desc=f"Fetching players data from {team.name}..."):
                player_df = self.fetch_live_tournament_stats_from_player(name, id)
                df = pd.concat([df, player_df])
        return df
    
    # estatisticas do campeonato inteiro 
    # https://api.sofascore.com/api/v1/team/1961/unique-tournament/92/season/56974/statistics/overall
    # top player por competição do time
    # https://api.sofascore.com/api/v1/team/1961/unique-tournament/92/season/56974/top-players/overall
    # ultimas partidas
    # https://api.sofascore.com/api/v1/team/1961/events/last/0
    # estatisticas de jogador por torneio
    # https://api.sofascore.com/api/v1/player/33238/unique-tournament/92/season/56974/statistics/overall