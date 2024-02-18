from extraction.tournament import *

Carioca = Tournament("Carioca Série A – Taça Guanabara", 92, 56974)
players = Carioca.get_tournament_stats_from_all_players()
players.to_csv('data/players_carioca.csv')
teams = Carioca.get_tournament_stats_from_teams()
teams.to_csv('data/teams_carioca.csv')

