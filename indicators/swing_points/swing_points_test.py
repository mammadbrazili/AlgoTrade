import time
from indicators.swing_points.swing_points_2 import SwingPointsIndicatorLogic
import pandas as pd

df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)
# getting one symbol for visualization
df = df.swaplevel(axis=1).sort_index(axis=1)["AAPL"]
#df= df.iloc[100:150]


# data
st = time.time()
data_calc = {"price": df}
meta_data = {}
swings = SwingPointsIndicatorLogic.logic(meta_data,data_calc,"1m")
print(time.time()-st)
print(swings[swings["ltl"]])

# adding swing points to calculated data
# data_calc["indicator"] = swing_points
# SwingPointsIndicatorLogic.visualize(meta_data, data_calc)
