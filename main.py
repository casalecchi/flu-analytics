from utils import *

data = get_data_from_matches()

ground_filter = data.sort_values('ground_won', ascending=False)
aerial_filter = data.sort_values('aerial_won', ascending=False)
clearence_filter = data.sort_values('clearences', ascending=False)
interceptions_filter = data.sort_values('interceptions', ascending=False)

generate_bar_from_data(ground_filter, 'ground_won', 'Ranking of ground duels won - 3th round - Carioca')
