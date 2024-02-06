from extraction.carioca import *

inputs = get_carioca_inputs()
fname = ROOT_DIR + f"/data/{inputs['fname']}"
round = inputs["round"]
teams = inputs["teams"]
data = get_df_from_carioca_round(round, teams)
data.to_csv(fname)