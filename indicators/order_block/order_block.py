from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter
import pandas as pd
import time
class OrderBlockIndicatorLogic(IndicatorLogic):
    """
    Interface for Finding Order Blocks and Choch
    """

    @staticmethod
    def visualize(meta_data: dict, data: dict):
        """
        Visualization pipeline for indicator

        :param meta_data: any data not related to price data and needed for calculations.
        :type meta_data: dict

        :param data: price or indicator data
        :type data: dict

        """
        # yahoo finance data
        df = data["price"]
        order_blocks = data["order_block"]

        df["bullish_ob"] = order_blocks["bullish_ob"]
        df["bearish_ob"] = order_blocks["bearish_ob"]
        bullish_ob = df[df["bullish_ob"]]
        bearish_ob = df[df["bearish_ob"]]

        # plot candlesticks
        plotter = Plotter()
        plotter.plot_candlestick(df)

        # fractal movement
        major_sth = df[df["major_sth"]]
        major_stl = df[df["major_stl"]]
        major_stl_index = major_stl.index.tolist()
        major_sth_index = major_sth.index.tolist()
        major_stl_value = major_stl["low"].values.tolist()
        major_sth_value = major_sth["high"].values.tolist()
        major_stls = pd.DataFrame({"value": major_stl_value})
        major_stls = major_stls.set_index(pd.Index(major_stl_index))
        major_sths = pd.DataFrame({"value": major_sth_value})
        major_sths = major_sths.set_index(pd.Index(major_sth_index))
        major_pivots = pd.concat([major_stls, major_sths]).sort_index()
        plotter.plot(major_pivots["value"])

        # for Plotting
        bearish_ob_value = bearish_ob["high"].tolist()
        bearish_ob_candle = bearish_ob.index.tolist()
        for timestamp, price in zip(bearish_ob_candle, bearish_ob_value):
            plotter.draw_label(text=None, x=timestamp, y=price, width=0.5, height=0.5, background_color="orange")

        bullish_ob_price = bullish_ob["low"].tolist()
        bullish_ob_candle = bullish_ob.index.tolist()
        for timestamp, price in zip(bullish_ob_candle, bullish_ob_price):
            plotter.draw_label(text=None, x=timestamp, y=price, width=0.5, height=0.5, background_color="blue")


        plotter.show()

    @staticmethod
    def logic(meta_data: dict, data: dict, time_frame: str):
        """
        Swing Points indicator logic & calculations

        :param time_frame: timeframe of indicator
        :type time_frame: str

        :param meta_data: any data not related to price data and needed for calculations.
        :type meta_data: dict

        :param data: price or indicator data
        :type data: dict

        :return: a dict concluding ma & upper/lower curve panda series
        """

        df = data["price"]
        df["sth"] = data["swings"]["sth"]
        df["stl"] = data["swings"]["stl"]


        # in next step we want to delete consecutive sth/stl in rows
        sth = df[df["sth"]]
        stl = df[df["stl"]]
        # adjoining high and low pivots
        pivots = pd.concat([stl, sth]).sort_index()

        # deleting rows if a candle is both stl or sth
        mask1 = pivots["stl"] != pivots["sth"]
        pivots = pivots[mask1].reset_index()
        # keep the lowest value of stl, if we have consecutive stl
        pivots["group"] = (pivots["stl"] != pivots["stl"].shift()).cumsum()
        d = pivots.groupby("group").min()

        # keep the highest value of sth if we have consecutive sth
        d.reset_index(drop=True, inplace=True)
        d["group"] = (d["sth"] != d["sth"].shift()).cumsum()
        d = pivots.groupby("group").max()

        # final pivots dataframe (in which there is no 2 sth or stl continuously )
        # reminder : timestamp column name is "index"
        pivots = d.reset_index()

        # bearish order block
        next_pivot = pivots.shift(-1)
        prev_pivot = pivots.shift(1)
        mask2 = (next_pivot["low"] < prev_pivot["low"]) & (pivots["low"] > prev_pivot["low"])
        pivots["bearish_ob"] = mask2
        # bullish_ob
        mask1 = (next_pivot["high"] > prev_pivot["high"]) & (pivots["high"] < prev_pivot["high"])
        pivots["bullish_ob"] = mask1

        # applying changes to dataframe
        df["bullish_ob"] = False
        df["bearish_ob"] = False
        bullish_ob_candles = pivots[pivots["bullish_ob"]]["index"].tolist()
        df.loc[bullish_ob_candles, "bullish_ob"] = True

        bearish_ob_candles = pivots[pivots["bearish_ob"]]["index"].tolist()
        df.loc[bearish_ob_candles, "bearish_ob"] = True

        return df[["bearish_ob", "bullish_ob"]]

