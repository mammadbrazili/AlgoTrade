import pandas as pd
from indicators.ao_divergence.ao_divergence import AoDivergenceIndicatorLogic
from indicators.swing_points.swing_points_2 import SwingPointsIndicatorLogic
from indicators.ao.ao import AOIndicatorLogic
import time
df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)
# getting one symbol for visualization
df = df.swaplevel(axis=1).sort_index(axis=1)["AAPL"]
# df = df.iloc[150:300]

data_calc = {"price" : df}
meta_data = {}
swings = SwingPointsIndicatorLogic.logic(meta_data, data_calc, "1m")
data_calc["swings"] = swings

meta_data={"short_period" :9 , "long_period":36}
ao = AOIndicatorLogic.logic(meta_data,data_calc,"1m")
data_calc["ao"] = ao


divergence = AoDivergenceIndicatorLogic.logic(meta_data,data_calc,"1m")
data_calc["divergence"] = divergence

AoDivergenceIndicatorLogic.visualize(meta_data, data_calc)
