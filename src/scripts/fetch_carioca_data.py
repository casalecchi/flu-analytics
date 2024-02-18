from extraction.tournament import *

Carioca = Tournament("Carioca Série A – Taça Guanabara", 92, 56974)
data = Carioca.get_tournament_stats_from_player('Gérman Cano', 33238)
data.to_csv('data/cano.csv')

