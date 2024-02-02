from utils.charts import *

path = os.getcwd() + '/data/data.csv'
data = pd.read_csv(path)
generate_bar_from_data(data, "accuratePass", "Ranking de passes certos na rodada 4 - Carioca")