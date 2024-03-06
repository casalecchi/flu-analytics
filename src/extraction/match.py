from extraction import *
from extraction.fetchData import *
from extraction.team import Team
from extraction.sofastats import SofaStats


class Match:
    """Class for fetching data from Sofascore matches.
    It must be provided the id of the match."""

    def __init__(self, id):
        self.id = id
        self.event_data = get_match_data(self.id)
        self.away = self._get_team('awayTeam')
        self.awayScore = self._get_score('awayScore')
        self.home = self._get_team('homeTeam')
        self.homeScore = self._get_score('homeScore')
        self.round = self._get_round()
        self.teams_stats = self._get_teams_stats()

    def _get_teams_stats(self) -> dict:
        """Get JSON data from teams in the match"""
        try:
            return get_teams_stats_by_match(self.id)[0]
        except:
            print(f"Cannot fetch team statistics from {self.home.name} x {self.away.name}")
            return {}

    def _get_round(self) -> int:
        return self.event_data['roundInfo']['round']
    
    def _get_score(self, field) -> int:
        return self.event_data[field]['display']

    def _get_team(self, field: str) -> Team:
        """Return the Team class instance"""
        team_id = self.event_data[field]['id']
        return Team(team_id)
    
    def _get_home_away_player_ids(self):
        """Return two arrrays with the players ids from each team in the match"""
        data = get_players_stats_by_match(self.id)
        home_ids = []
        away_ids = []
        
        for player in data['home']['players']:
            player_id = player['player']['id']
            home_ids.append(player_id)
        for player in data['away']['players']:
            player_id = player['player']['id']
            away_ids.append(player_id)
        
        return home_ids, away_ids
    
    def fetch_teams_stats(self):
        """Return a DataFrame containing stats from both teams, one in a row of the df"""
        if self.teams_stats == {}:
            return pd.DataFrame()
        
        stats = self.teams_stats['groups']
        total_attrs = ["Long balls", "Crosses", "Dribbles"]
        df = pd.DataFrame(columns=('team_id', 'match_id', 'team', 'opponent', 'primary_color', 'secondary_color', 'badge_url', 
                                   'Goals Scored', 'Goals Suffered', 'Matches', *SofaStats.Match_Stats, *['Accurate ' + att for att in total_attrs]))
        df.set_index('team_id', inplace=True)
        for index, team in enumerate([self.home, self.away]):
            if index == 0:
                field = 'home'
                goals_scored = self.homeScore
                goals_suffered = self.awayScore
                opponent = self.away
            else:
                field = 'away'
                goals_scored = self.awayScore
                goals_suffered = self.homeScore
                opponent = self.home
            value = field + 'Value'
            total = field + 'Total'

            primary_color = team.primary_color
            secondary_color = team.secondary_color
            badge_url = team.badge

            df.loc[team.id] = [self.id, team.name, opponent.name, primary_color, secondary_color, badge_url,
                               goals_scored, goals_suffered, 1, *[0.0 for _ in range(len(SofaStats.Match_Stats) + len(total_attrs))]]
            for group in stats:
                for item in group['statisticsItems']:
                    attr = item['name']
                    if attr in total_attrs:
                        df.at[team.id, 'Accurate ' + attr] = item[value]
                        df.at[team.id, attr] = item[total]
                    else:     
                        df.at[team.id, attr] = item[value]
        
        return df
                
    def fetch_players_stats(self):
        """Return a DataFrame containing the stats from all players listed for the match"""
        data = get_players_stats_by_match(self.id)
        df = pd.DataFrame(columns=('player_id', 'player_name', 'team_name', 'primary_color', 'secondary_color', 
                                   'badge_url', 'avatar_url', *SofaStats.Individual_Stats))
        df.set_index('player_id', inplace=True)
        for field, team in zip(['home', 'away'], [self.home, self.away]):
            team_stats = data[field]
            players: List[dict] = team_stats['players']
            for player in players:
                player_id = player['player']['id']
                player_name = player['player']['name']
                team_name = team.name
                primary_color = team.primary_color
                secondary_color = team.secondary_color
                badge_url = team.badge
                avatar_url = f"https://api.sofascore.com/api/v1/player/{player_id}/image"
                df.loc[player_id] = [player_name, team_name, primary_color, secondary_color,
                                 badge_url, avatar_url, *[0.0 for _ in range(len(SofaStats.Individual_Stats))]]
                statistics: dict = player.get('statistics', {})
                for attr in SofaStats.Individual_Stats:
                    df.at[player_id, attr] = statistics.get(attr, 0)
        
        return df

    def fetch_shots(self):
        """Return a DataFrame with the match shots. Columns in the DataFrame: player_id, player_name,
        team, opponent, x, y, xG, xGOT, shot_result, body_part.

        The x and y coordinates varies between 0 and 1, so when plotting, it has to be multiplied by
        width and height of the pitch."""
        shotmap_data = get_shotmap(self.id)
        shotmap_data = shotmap_data.get('shotmap', [])
        df = pd.DataFrame(columns=('shot_id', 'player_id', 'player_name', 'team', 'opponent',
                                   'x', 'y', 'xG', 'xGOT', 'shot_result', 'body_part'))
        # pode adicionar aqui: cor do time, escudo, foto jogador...
        df.set_index('shot_id', inplace=True)

        for shot in shotmap_data:
            shot_id = shot['id']
            player = shot['player']
            player_id = player['id']
            player_name = player['name']
            
            if shot['isHome']:
                team = self.home.name
                opponent = self.away.name
            else:
                team = self.away.name
                opponent = self.home.name
        
            shot_result = shot['shotType']
            body_part = shot['bodyPart']

            shot_coord = shot['playerCoordinates']
            x = shot_coord['x'] / 100
            y = shot_coord['y'] / 100
            xG = shot['xg']
            xGOT = shot.get('xgot', np.nan)

            df.loc[shot_id] = [player_id, player_name, team, opponent, x, y, xG, xGOT, shot_result, body_part]

        return df
    
    def fetch_heatmap_player(self, player_id):
        """Return a DataFrame with the events coordinates from a player. Columns in the DataFrame: player_id,
        x, y.

        The x and y coordinates varies between 0 and 1, so when plotting, it has to be multiplied by
        width and height of the pitch."""
        heatmap_data = get_match_heatmap(self.id, player_id)
        heatmap = heatmap_data.get('heatmap', [])
        df = pd.DataFrame(columns=('player_id', 'x', 'y'))
        for index, point in enumerate(heatmap):
            x = point['x'] / 100
            y = point['y'] / 100
            df.loc[index] = [player_id, x, y]
        
        return df
    
    def fetch_heatmap_teams(self):
        """Return a DataFrame with the events coordinates from a team. It concatenates all the heatmap from the 
        players listed on the match. Columns in the DataFrame: player_id, x, y and team.

        The x and y coordinates varies between 0 and 1, so when plotting, it has to be multiplied by
        width and height of the pitch."""
        home_ids, away_ids = self._get_home_away_player_ids()
        df = pd.DataFrame(columns=('player_id', 'x', 'y', 'team'))
        
        for field in ['home', 'away']:
            if field == 'home':
                team = self.home
                ids = home_ids
            else:
                team = self.away
                ids = away_ids
            
            for id in ids:
                heatmap = self.fetch_heatmap_player(id)
                heatmap['team'] = team.name
                df = pd.concat([df, heatmap])
            
        return df
