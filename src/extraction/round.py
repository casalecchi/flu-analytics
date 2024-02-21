from extraction import *
from extraction.fetchData import *
from extraction.tournament import Tournament
from extraction.match import Match


class Round:
    def __init__(self, round_number: int, tournament: Tournament):
        self.round = round_number
        self.tournament = tournament
        self.matches = self._get_matches_by_round()

    def _get_matches_by_round(self) -> List[Match]:
        matches = []
        matches_data = get_round_matches(self.tournament.unique_id, self.tournament.season_id, self.round)
        for match in matches_data:
            match_id = match['id']
            matches.append(Match(match_id))
    
        return matches
    
    def fetch_teams_stats(self):
        df = pd.DataFrame()
        for match in self.matches:
            teams_df = match.get_teams_df_stats()
            df = pd.concat([df, teams_df])
        
        return df
    
    def fetch_players_stats(self):
        df = pd.DataFrame()
        for match in self.matches:
            players_df = match.get_players_df_stats()
            df = pd.concat([df, players_df])

        return df
    
    def fetch_teams_stats_combined(self):
        df = Round(1, self.tournament).fetch_teams_stats()
        df.set_index('team', inplace=True)
        for round_number in tqdm(range(2, self.round + 1), desc=f"Fetching data from rounds..."):
            round = Round(round_number, self.tournament)
            teams_stats = round.fetch_teams_stats()
            teams_stats.set_index('team', inplace=True)
            df = df.add(teams_stats, fill_value=0)
            df.drop(['match_id'], axis=1, inplace=True)
        
        return df
    
    def fetch_players_stats_combined(self):
        print("Fetching data from round 1...")
        df = Round(1, self.tournament).fetch_players_stats()
        df.set_index('player_id', inplace=True)
        text_columns = ['player_name', 'team_name', 'primary_color', 
                     'secondary_color', 'badge_url', 'avatar_url']
        text_attrs = df[text_columns]
        df.drop(text_columns, axis=1, inplace=True)
        for round_number in tqdm(range(2, self.round + 1), desc=f"Fetching data from remaining rounds..."):
            round = Round(round_number, self.tournament)
            players_stats = round.fetch_players_stats()
            players_stats.set_index('player_id', inplace=True)
            text_players = players_stats[text_columns]
            players_stats.drop(text_columns, axis=1, inplace=True)

            df = df.add(players_stats, fill_value=0)
            text_attrs = pd.concat([text_attrs, text_players])
        
        text_attrs.drop_duplicates(inplace=True)
        df[text_columns] = text_attrs

        return df



Carioca = Tournament("Carioca Série A – Taça Guanabara", 92, 56974)
print(Round(8, Carioca).fetch_teams_stats())