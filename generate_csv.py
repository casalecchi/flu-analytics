from utils.fetch_data import *

inputs = get_data_inputs()
fname = os.getcwd() + f"/data/{inputs["fname"]}.csv"
round = inputs["round"]
teams = inputs["teams"]
data = get_data_from_matches(round, teams)
data.to_csv(fname)