from static_support_resistance import StaticSupportResistanceIndicatorLogic
import pandas as pd

df = pd.read_csv("C:/signal/signal_khosro/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.iloc[:50]
# getting one symbol for visualization
candle = df.reset_index(drop=True)
symbol = "AAPL"
candle = candle.swaplevel(axis=1).sort_index(axis=1)[symbol]

# data
data_calc = {"price_candle": candle, "price": df}
meta_data = {"length": 5}

# calculating levels
levels = StaticSupportResistanceIndicatorLogic.logic(meta_data, data_calc, "1m")
# adding levels to calculated data
data_calc["indicator"] = levels[symbol]
# plotting levels
StaticSupportResistanceIndicatorLogic.visualize(data_calc)