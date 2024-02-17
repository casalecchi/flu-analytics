from extraction.tournament import *

Carioca = Tournament("Carioca Série A – Taça Guanabara", 92, 56974)
inputs = Carioca.get_tournament_inputs()
fname = ROOT_DIR + f"/data/{inputs['fname']}"
round = inputs["round"]
teams = inputs["teams"]
data = Carioca.get_df_from_tournament_round(round, teams)
data.to_csv(fname)
