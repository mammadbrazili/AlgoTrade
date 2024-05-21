from indicators.bos_finder.bos_finder import BosFinderIndicatorLogic
from indicators.swing_points.swing_points_2 import SwingPointsIndicatorLogic
from indicators.choch.choch import ChochIndicatorLogic
import time
import pandas as pd

df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)
# getting one symbol for visualization
df = df.swaplevel(axis=1).sort_index(axis=1)["AAPL"]
df = df.iloc[:200]
# for reindexing the dataframe descending
#df = df.set_index(pd.Index(range(len(df)-1, -1, -1)))

data_calc = {"price": df}
meta_data = {}

st = time.time()

swings = SwingPointsIndicatorLogic.logic(meta_data, data_calc, "1m")
data_calc["swings"] = swings
print(time.time()-st)

bos = BosFinderIndicatorLogic.logic(meta_data,data_calc,"1m")
data_calc["bos"] = bos
print(time.time()-st)

choch = ChochIndicatorLogic.logic(meta_data, data_calc, "1m")
data_calc["choch"] = choch
print(time.time()-st)

ChochIndicatorLogic.visualize(meta_data, data_calc)