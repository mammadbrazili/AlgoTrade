from indicators.bos_finder.bos_finder import BosFinderIndicatorLogic
from indicators.swing_points.swing_points_2 import SwingPointsIndicatorLogic
from indicators.order_block.order_block import OrderBlockIndicatorLogic
from indicators.order_block_single_timeframe.order_block_single_timeframe import ObSingleTimeFrameIndicatorLogic
import time
import pandas as pd

df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)
# getting one symbol for visualization
df = df.swaplevel(axis=1).sort_index(axis=1)["AMZN"]
#df = df.iloc[450:468]
# for reindexing the dataframe descending
#df = df.set_index(pd.Index(range(len(df)-1, -1, -1)))


data_calc = {"price": df}
meta_data = {}
swings = SwingPointsIndicatorLogic.logic(meta_data, data_calc, "1m")
data_calc["swings"] = swings

ob = OrderBlockIndicatorLogic.logic(meta_data,data_calc,"1m")
data_calc["order_block"] = ob

st =time.time()

single_tf_ob = ObSingleTimeFrameIndicatorLogic.logic(meta_data, data_calc,"1m")
print(time.time()-st)
print(single_tf_ob)
