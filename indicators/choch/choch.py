from indicators.abstracts.indicator import IndicatorLogic
import pandas as pd
from visualization.plotter import Plotter

class ChochIndicatorLogic(IndicatorLogic):

    @staticmethod
    def visualize(meta_data: dict, data: dict):
        df = data["price"]
        choch = data["choch"]

        # candlestick plot
        plotter = Plotter()
        plotter.plot_candlestick(df)

        choch_up_candle = choch["choch_up_candle"]
        choch_down_candle = choch["choch_down_candle"]

        # plotting choch from downtrend
        for i in range(len(choch_down_candle)):
            start_candle = list(choch_down_candle.keys())[i]
            end_candle = list(choch_down_candle.values())[i]
            start_value = df.loc[start_candle, "high"]
            end_value = df.loc[end_candle, "close"]
            plotter.draw_line(x1=start_candle, x2=end_candle, y1=start_value, y2=end_value)

        # plotting choch from uptrend
        for i in range(len(choch_up_candle)):
            start_candle = list(choch_up_candle.keys())[i]
            end_candle = list(choch_up_candle.values())[i]
            start_value = df.loc[start_candle, "low"]
            end_value = df.loc[end_candle, "close"]
            plotter.draw_line(x1=start_candle, x2=end_candle, y1=start_value, y2=end_value)


        plotter.show()

    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]
        df["sth"] = data["bos"]["major_sth"]
        df["stl"] = data["bos"]["major_stl"]

        # delete consecutive sth/stl in rows
        sth = df[df["major_sth"]]
        stl = df[df["major_stl"]]
        # adjoining high and low pivots
        pivots = pd.concat([stl, sth]).sort_index()

        # deleting rows if a candle is both stl or sth
        mask1 = pivots["stl"] != pivots["sth"]
        pivots = pivots[mask1].reset_index()
        # keep the lowest value of stl, if we have consecutive stls
        pivots["group"] = (pivots["stl"] != pivots["stl"].shift()).cumsum()
        d = pivots.groupby("group").min()

        # keep the highest value of sth if we have consecutive sths
        d.reset_index(drop=True, inplace=True)
        d["group"] = (d["sth"] != d["sth"].shift()).cumsum()
        d = pivots.groupby("group").max()

        # final pivots dataframe (in which there is no 2 sth or stl continuously )
        # reminder : timestamp column name is "index"
        pivots = d.reset_index()

        # choch
        two_next_pivot = pivots.shift(-2)
        two_prev_pivot = pivots.shift(2)
        # defining ITL
        mask1 = pivots["stl"] == True
        mask2 = two_next_pivot["low"] > pivots["low"]
        mask3 = two_prev_pivot["low"] > pivots["low"]
        pivots["ITL"] = mask1 & mask2 & mask3

        # defining ITH
        mask1 = pivots["sth"] == True
        mask2 = two_next_pivot["high"] < pivots["high"]
        mask3 = two_prev_pivot["high"] < pivots["high"]
        pivots["ITH"] = mask1 & mask2 & mask3

        # defining CHOCH from Uptrend --> in uptrend if a swing low (which is last pivot before ITH) mitigated,
        # it's a choch
        next_pivot = pivots.shift(-1)
        mask = next_pivot["ITH"] == True
        pivots["swing_low"] = mask

        # defining CHOCH from downtrend --> in downtrend if a swing high which is last pivot before ITL mitigated,
        # it's a CHOCH
        mask1 = next_pivot["ITL"] == True
        pivots["swing_high"] = mask1

        pivots = pivots.set_index("index")
        # Get the indices of rows with True values
        true_low = pivots[pivots['swing_low'] == True].index
        true_high = pivots[pivots['swing_high'] == True].index

        # Create an empty list to store the indices of rows make choch
        choch_up_candle = {}
        choch_down_candle = {}

        # Iterate over the swing low row indexes
        for index in true_low:
            # Get the value of the swing_low value
            swing_low_value = pivots.loc[index, 'low']

            # Check to find the first row that is lower than swing low value
            a = df.loc[index+1 : ,"low"].lt(swing_low_value).idxmax()
            if a:
                choch_up_candle.update({index : a})

        # Iterate over the swing high row indexes
        for index in true_high:
            # Get the value of the swing_low value
            swing_high_value = pivots.loc[index, 'high']

            # Check to find the first row that is higher than swing high value
            a = df.loc[index+1 : ,"high"].gt(swing_high_value).idxmax()
            if a:
                choch_down_candle.update({index : a})

        return {"choch_up_candle": choch_up_candle, "choch_down_candle": choch_down_candle}


