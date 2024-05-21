import pandas as pd
from indicators.candlestick.candlestick import CandleStickIndicatorLogic
import time

df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)
# getting one symbol for visualization
df = df.swaplevel(axis=1).sort_index(axis=1)["AAPL"]
df = df.iloc[:100]
st=time.time()

data_calc = {"price": df}
meta_data = {}

patterns = CandleStickIndicatorLogic.logic(meta_data, data_calc,"1m")
data_calc["patterns"] = patterns

CandleStickIndicatorLogic.visualize(meta_data,data_calc)

