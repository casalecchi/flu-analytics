from extraction.tournament import *

Brasileirao = Tournament("Brasileirão Série A", 325, 48982)
inputs = Brasileirao.get_tournament_inputs()
fname = ROOT_DIR + f"/data/{inputs['fname']}"
round = inputs["round"]
teams = inputs["teams"]
data = Brasileirao.get_df_from_tournament_round(round, teams)
data.to_csv(fname)
