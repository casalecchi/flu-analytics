from extraction.tournament import *

Brasileirao = Tournament("Brasileirão Série A", 325, 48982)
data = Brasileirao.get_tournament_stats_from_teams()
data.to_csv('data/brasileirao.csv')
