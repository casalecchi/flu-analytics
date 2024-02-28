from extraction.tournament import *
from extraction.round import *


Carioca = Tournament("Carioca Série A – Taça Guanabara", 92, 56974)
round_number = int(input("Which round you want to fetch data?\n"))
round = Round(round_number, Carioca)

players = round.fetch_players_stats()
players.to_csv(f'data/carioca-2024/players/new_carioca_players_round_{round_number}.csv')

teams = round.fetch_teams_stats()
teams.to_csv(f'data/carioca-2024/matches/new_carioca_teams_round_{round_number}.csv')

players_combined = round.fetch_players_stats_combined()
players_combined.to_csv(f'data/carioca-2024/players/new_carioca_players_until_{round_number}th_round.csv')

teams_combined = round.fetch_teams_stats_combined()
teams_combined.to_csv(f'data/carioca-2024/matches/new_carioca_teams_until_{round_number}th_round.csv')
