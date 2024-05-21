import pandas as pd
import time
from indicators.abstracts.indicator import IndicatorLogic
class SwingPointsIndicatorLogic(IndicatorLogic):

    @staticmethod
    def visualize(meta_data: dict, data: dict):
        pass

    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]

        # finding stl
        prev_candle = df.shift(1)
        next_candle = df.shift(-1)
        stl_mask = (prev_candle["low"] > df["low"]) & (next_candle["low"] > df["low"])
        df["stl"] = stl_mask
        stl = df[df["stl"]]

        # finding sth
        sth_mask = (prev_candle["high"] < df["high"]) & (next_candle["high"] < df["high"])
        df["sth"] = sth_mask
        sth = df[df["sth"]]

        # finding itl
        df["itl"] = False
        prev_stl = stl.shift(1)
        next_stl = stl.shift(-1)
        itl_mask = (prev_stl["low"] > stl["low"]) & (next_stl["low"] > stl["low"])
        itl = stl[itl_mask]
        # re-assigning itl boolean value in dataframe
        itl_candle = itl.index.tolist()
        df.loc[itl_candle, "itl"] = True

        # finding ith
        df["ith"] = False
        prev_sth = sth.shift(1)
        next_sth = sth.shift(-1)
        ith_mask = (prev_sth["high"] < sth["high"]) & (next_sth["high"] < sth["high"])
        ith = sth[ith_mask]
        # re-assigning ith boolean value in dataframe
        ith_candle = ith.index.tolist()
        df.loc[ith_candle , "ith"] = True

        # finding ltl
        df["ltl"] = False
        prev_itl = itl.shift(1)
        next_itl = itl.shift(-1)
        ltl_mask = (prev_itl["low"] > itl["low"]) & (next_itl["low"] > itl["low"])
        ltl = itl[ltl_mask]
        # re-assigning ltl boolean value in dataframe
        ltl_candle = ltl.index.tolist()
        df.loc[ltl_candle , "ltl"] = True

        # finding lth
        df["lth"] = False
        prev_ith = ith.shift(1)
        next_ith = ith.shift(-1)
        lth_mask = (prev_ith["high"] < ith["high"]) & (next_ith["high"] < ith["high"])
        lth = ith[lth_mask]
        # re-assigning ith boolean value in dataframe
        lth_candle = lth.index.tolist()
        df.loc[lth_candle , "lth"] = True

        return df[["stl","sth", "itl", "ith", "ltl", "lth"]]


# meta_data = {"kind": "all"}
# df = pd.read_csv("C:/Users/chartbox-dev-3/Downloads/symbol_df.csv", index_col=0, header=[0, 1])
# df.index = pd.DatetimeIndex(df.index)
# df = df.reset_index(drop=True)
# # getting one symbol for visualization
# df = df.swaplevel(axis=1).sort_index(axis=1)["AAPL"]
# #df = df.iloc[:100]
#
# data = {"price" : df}
# time_frame = "1H"
# start = time.time()
# a = SwingPointsIndicatorLogic()
# answer = a.logic(meta_data, data, time_frame)
# end= time.time()
# l = end - start
# print(answer)
# print(l)