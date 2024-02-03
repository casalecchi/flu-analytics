from utils.charts import *

inputs = get_bar_chart_inputs()
fname = inputs["fname"]
attr = inputs["attr"]
k = int(inputs["k"])
title = inputs["title"]

path = os.getcwd() + "/data/" + fname
data = pd.read_csv(path)
generate_bar_from_data(data, attr, title, k=k)
