import pandas as pd
from indicators.swing_points.swing_points_2 import SwingPointsIndicatorLogic
from indicators.order_block.order_block import OrderBlockIndicatorLogic
from indicators.bos_finder.bos_finder import BosFinderIndicatorLogic
from indicators.breaker_block.breaker_block import BreakerBlockIndicatorLogic
from indicators.choch.choch import ChochIndicatorLogic
import time

df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)
# getting one symbol for visualization
df = df.swaplevel(axis=1).sort_index(axis=1)["GO"]
df = df.iloc[:100]
# for reindexing the dataframe descending
#df = df.set_index(pd.Index(range(len(df)-1, -1, -1)))


data_calc = {"price": df}
meta_data = {}

swings = SwingPointsIndicatorLogic.logic(meta_data, data_calc, "1m")
data_calc["swings"] = swings

bos = BosFinderIndicatorLogic.logic(meta_data,data_calc,"1m")
data_calc["bos"] = bos

choch = ChochIndicatorLogic.logic(meta_data, data_calc, "1m")
data_calc["choch"] = choch

ob = OrderBlockIndicatorLogic.logic(meta_data,data_calc,"1m")
data_calc["order_block"] = ob

st = time.time()
bb = BreakerBlockIndicatorLogic.logic(meta_data,data_calc,"1m")
print(time.time()-st)
data_calc["breaker_block"] = bb

BreakerBlockIndicatorLogic.visualize(meta_data,data_calc)
print(bb)