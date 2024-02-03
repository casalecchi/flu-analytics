from utils.charts import *

inputs = get_bar_chart_inputs()
fname = inputs["fname"]
attr = inputs["attr"]
k = int(inputs["k"])
int_response = inputs["isInt"]
isInt = False if int_response.lower().find('n') != -1 else True
title = inputs["title"]

path = os.getcwd() + "/data/" + fname
data = pd.read_csv(path)
generate_bar_from_data(data, attr, title, isInt=isInt, k=k)
