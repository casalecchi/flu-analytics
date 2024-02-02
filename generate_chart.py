from utils.charts import *

path = os.getcwd() + '/data/data.csv'
data = pd.read_csv(path)
generate_bar_from_data(data, "totalPass", "Ranking de passes certos na rodada 4 - Carioca")
generate_bar_from_data(data, "duelWon", "Ranking de duelos ganhos na rodada 4 - Carioca")
generate_bar_from_data(data, "interceptionWon", "Ranking de interceptações na rodada 4 - Carioca")

