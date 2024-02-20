from extraction import *
from extraction.fetchData import *
from extraction.team import Team
from extraction.sofastats import SofaStats


class Match:
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
        team_id = self.event_data[field]['id']
        return Team(team_id)
    
    def get_match_df_stats(self):
        if self.teams_stats == {}:
            return pd.DataFrame()
        
        stats = self.teams_stats['groups']
        total_attrs = ["Long balls", "Crosses", "Dribbles"]
        df = pd.DataFrame(columns=('match_id', 'team', *SofaStats.Match_Stats, *['Accurate ' + att for att in total_attrs]))
        for index, team in enumerate([self.home, self.away]):
            if index == 0:
                field = 'home'
            else:
                field = 'away'
            value = field + 'Value'
            total = field + 'Total'

            df.loc[index] = [self.id, team.name, *[0.0 for _ in range(len(SofaStats.Match_Stats) + len(total_attrs))]]
            for group in stats:
                for item in group['statisticsItems']:
                    attr = item['name']
                    if attr in total_attrs:
                        df.at[index, 'Accurate ' + attr] = item[value]
                        df.at[index, attr] = item[total]
                    else:     
                        df.at[index, attr] = item[value]
        
        return df
                



print(Match(11873086).get_match_df_stats())
    