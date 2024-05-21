import pandas as pd
import time
from visualization.plotter import Plotter

df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/Telegram Desktop/data.csv")
df = df.iloc[9567:9597].reset_index()
# candlestick plot
plotter = Plotter()
plotter.plot_candlestick(df)

df = df.set_index(pd.Index(range(len(df) - 1, -1, -1)))


st = time.time()
# calculating pivots
data_previous = df.shift(1)
data_next = df.shift(-1)

# stl
mask1 = data_previous["low"] > df["low"]
mask2 = data_next["low"] > df["low"]
df["stl"] = mask1 & mask2

# sth
mask1 = data_previous["high"] < df["high"]
mask2 = data_next["high"] < df["high"]
df["sth"] = mask1 & mask2

# finding last stl timestamp & value
last_low_candle = df[df["stl"]].index.min()
last_low_value = df.loc[last_low_candle, "low"]

# finding last sth timestamp & value
last_high_candle = df[df["sth"]].index.min()
last_high_value = df.loc[last_high_candle, "high"]

# adding to a dict
market_structure = {"index_low": last_low_candle, "index_high": last_high_candle,
                    "value_low": last_low_value, "value_high": last_high_value}

# finding first row that is lower than swing low
a = df.loc[(last_low_candle - 1):, "low"].lt(last_low_value).idxmin()
# debug
if df.loc[a, "low"] > last_low_value:
    pass
else:
    market_structure["index_low"] = None
    market_structure["value_low"] = None

# Check to find the first row that is higher than swing high value
b = df.loc[(last_high_candle - 1):, "high"].lt(last_high_value).idxmin()
# debug

if df.loc[b, "high"] < last_high_value:
    pass
else:
    market_structure["index_high"] = None
    market_structure["value_high"] = None

# adding type of market structure
if market_structure["index_high"] and market_structure["index_low"] != None:

    # if we have swing high before swing low
    if market_structure["index_high"] > market_structure["index_low"]:
        market_structure["type"] = "low"
    else:
        market_structure["type"] = "high"

else:
    market_structure["type"] = None

# plotting points
if market_structure["index_low"] != None:
    plotter.draw_line(x1=len(df) - market_structure["index_low"] -1, y1=market_structure["value_low"],
                      x2=len(df),y2=market_structure["value_low"])

if market_structure["index_high"]!= None:
    plotter.draw_line(x1=len(df) - market_structure["index_high"]-1, y1=market_structure["value_high"],
                      x2=len(df),y2=market_structure["value_high"])

plotter.show()

print(time.time() - st)
print(market_structure)