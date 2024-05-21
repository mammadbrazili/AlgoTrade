import pandas as pd
df = pd.read_csv("C:/signal/signal_khosro/symbol_df.csv", index_col=0, header=[0, 1])
df.index = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)
# getting one symbol for visualization
df = df.swaplevel(axis=1).sort_index(axis=1)["AAPL"]
df = df.iloc[:100]

def calculate_rsi(data, window=14):
    delta = df["close"].diff()
    gain = delta.copy()
    loss = delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = gain.rolling(window).mean()
    avg_loss = abs(loss.rolling(window).mean())
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
df["RSI"] = calculate_rsi(df)

import time
st = time. time()
data_stl_prev = df.shift(1)
data_stl_next = df.shift(-1)
data_stl_mask = ((df['low'] < data_stl_prev["low"]) & (df['low'] < data_stl_next["low"]))
stl_value = df[data_stl_mask]
stl_prev = stl_value.shift(1)
stl_next = stl_value.shift(-1)
itl_mask = ((stl_value["low"] < stl_prev["low"]) & (stl_value["low"] < stl_next["low"]))
itl_value = stl_value[itl_mask]

# finding ITH
data_sth_prev = df.shift(1)
data_sth_next = df.shift(-1)
data_sth_mask = ((df['high'] > data_sth_prev["high"]) & (df['high'] > data_sth_next["high"]))
sth_value = df[data_sth_mask]
sth_prev = sth_value.shift(1)
sth_next = sth_value.shift(-1)
ith_mask = ((sth_value["high"] > sth_prev["high"]) & (sth_value["high"] > sth_next["high"]))
ith_value = sth_value[ith_mask]
next_candle_h = ith_value.shift(-1)
# print(st-time.time())

mask1 = next_candle_h["high"] > ith_value["high"]   # price is making higher high
mask2 =  next_candle_h["RSI"] < ith_value["RSI"]    # rsi is making lower low
regular_bearish = ith_value[mask1 & mask2]

next_candle_l = itl_value.shift(-1)
mask1 = next_candle_l["low"] < itl_value["low"]  # price is making lower low
mask2 = next_candle_l["RSI"] > itl_value["RSI"]  # rsi is going up
regular_bullish = itl_value[mask1 & mask2]
print(st-time.time())