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
        """Get matches instances for each match in that tournament round"""
        matches = []
        matches_data = get_round_matches(self.tournament.unique_id, self.tournament.season_id, self.round)
        for match in tqdm(matches_data, desc=f"Loading {self.round}th round matches..."):
            match_id = match['id']
            matches.append(Match(match_id))
    
        return matches
    
    def fetch_teams_stats(self):
        """Return a DataFrame with the team stats from all teams in a Round"""
        df = pd.DataFrame()
        for match in tqdm(self.matches, desc=f"Fetching teams stats from {self.round}th round matches..."):
            teams_df = match.fetch_teams_stats()
            df = pd.concat([df, teams_df])
        
        return df
    
    def fetch_players_stats(self):
        """Return a DataFrame with the players stats from all listed players in a Round"""
        df = pd.DataFrame()
        for match in tqdm(self.matches, desc=f"Fetching players stats from {self.round}th round matches..."):
            players_df = match.fetch_players_stats()
            df = pd.concat([df, players_df])

        return df
    
    def fetch_teams_stats_until(self):
        """Return a DataFrame with the accumulate team stats until, and including, the Round"""
        df = pd.DataFrame()
        text_attrs = pd.DataFrame()
        text_columns = ['team', 'primary_color', 'secondary_color', 'badge_url']

        for round_number in range(1, self.round + 1):
            round = Round(round_number, self.tournament)
            teams_stats = round.fetch_teams_stats()
            text_teams = teams_stats[text_columns]
            teams_stats.drop(['match_id', 'opponent', *text_columns], axis=1, inplace=True)

            if round_number == 1:
                df = teams_stats
            else: 
                df = df.add(teams_stats, fill_value=0)

            text_attrs = pd.concat([text_attrs, text_teams])
        
        text_attrs.drop_duplicates(inplace=True)
        df[text_columns] = text_attrs

        df['Ball possession'] = df['Ball possession'] / df['Matches']
        df.rename(columns={'Ball possession': 'Average ball possession'}, inplace=True)

        return df
    
    def fetch_players_stats_until(self):
        """Return a DataFrame with the accumulate team stats until, and including, the Round"""
        df = pd.DataFrame()
        text_attrs = pd.DataFrame()
        text_columns = ['player_name', 'team_name', 'primary_color', 
                     'secondary_color', 'badge_url', 'avatar_url']

        for round_number in range(1, self.round + 1):
            round = Round(round_number, self.tournament)
            players_stats = round.fetch_players_stats()
            text_players = players_stats[text_columns]
            players_stats.drop(text_columns, axis=1, inplace=True)

            if round_number == 1:
                df = players_stats
            else: 
                df = df.add(players_stats, fill_value=0)

            text_attrs = pd.concat([text_attrs, text_players])
        
        text_attrs.drop_duplicates(inplace=True)
        df[text_columns] = text_attrs

        return df
