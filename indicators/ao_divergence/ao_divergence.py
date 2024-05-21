from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter
import pandas as pd
import matplotlib.pyplot as plt
import time

class AoDivergenceIndicatorLogic(IndicatorLogic):
    """
    Interface for Finding Divergences in Awesome Oscillator
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
        df = data["price"]
        df["ao"] = data["ao"]
        df["itl"] = data["swings"]["itl"]
        df["ith"] = data["swings"]["ith"]
        df["bearish_divergence"] = data["divergence"]["bearish_divergence"]
        df["bullish_divergence"] = data["divergence"]["bullish_divergence"]

        ith_value = df[df["ith"]]
        itl_value = df[df["itl"]]
        bullish_divergence = df[df["bullish_divergence"]]
        bearish_divergence = df[df["bearish_divergence"]]
        bearish_divergence_indexes = list(bearish_divergence.to_dict(orient="index").keys())
        bearish_divergence_list = []

        for i in bearish_divergence_indexes:
            bearish_div_dict = {}
            # finding last pivot values
            last_pivot_index = list(ith_value.loc[:i - 1].to_dict(orient="index"))[-1]
            last_pivot_ao = df.loc[last_pivot_index, "ao"]
            last_pivot_high = df.loc[last_pivot_index, "high"]
            bearish_div_dict[f"divergence"] = {"last_index": last_pivot_index, "index": i,
                                               "last_ao": last_pivot_ao, "ao": df.loc[i, "ao"],
                                               "last_high": last_pivot_high, "high": df.loc[i, "high"]}
            bearish_divergence_list.append(bearish_div_dict)

        # bullish
        bullish_divergence_indexes = list(bullish_divergence.to_dict(orient="index").keys())
        bullish_divergence_list = []

        for i in bullish_divergence_indexes:
            bullish_div_dict = {}
            # finding last pivot values
            last_pivot_index = list(itl_value.loc[:i - 1].to_dict(orient="index"))[-1]
            last_pivot_ao = df.loc[last_pivot_index, "ao"]
            last_pivot_low = df.loc[last_pivot_index, "low"]
            bullish_div_dict[f"divergence"] = {"last_index": last_pivot_index, "index": i,
                                               "last_ao": last_pivot_ao, "ao": df.loc[i, "ao"],
                                               "last_low": last_pivot_low, "low": df.loc[i, "low"]}
            bullish_divergence_list.append(bullish_div_dict)

        # plotting candlestick
        plotter = Plotter()
        plotter.plot_candlestick(df)
        # plotting divergence lines on candlestick chart
        for i in range(len(bullish_divergence_list)):
            plotter.draw_line(x1=bullish_divergence_list[i]["divergence"]["last_index"],
                              x2=bullish_divergence_list[i]["divergence"]["index"],
                              y1=bullish_divergence_list[i]["divergence"]["last_low"],
                              y2=bullish_divergence_list[i]["divergence"]["low"],
                              color="blue")

        for i in range(len(bearish_divergence_list)):
            plotter.draw_line(x1=bearish_divergence_list[i]["divergence"]["last_index"],
                              x2=bearish_divergence_list[i]["divergence"]["index"],
                              y1=bearish_divergence_list[i]["divergence"]["last_high"],
                              y2=bearish_divergence_list[i]["divergence"]["high"],
                              color="orange")

        # plotting ao
        colors = ['green' if df["ao"][i] > df["ao"][i - 1] else 'red' for i in range(df.index[0]+1, df.index[-1])]
        plt.figure(figsize=(15, 8))
        plt.bar(df["ao"].index[1:], df["ao"][1:], color=colors)
        # plotting divergence lines on ao
        for i in range(len(bullish_divergence_list)):
            x1 = bullish_divergence_list[i]["divergence"]["last_index"]
            x2 = bullish_divergence_list[i]["divergence"]["index"]
            y1 = bullish_divergence_list[i]["divergence"]["last_ao"]
            y2 = bullish_divergence_list[i]["divergence"]["ao"]

            plt.plot([x1, x2], [y1, y2], color="blue")

        for i in range(len(bearish_divergence_list)):
            x1 = bearish_divergence_list[i]["divergence"]["last_index"]
            x2 = bearish_divergence_list[i]["divergence"]["index"]
            y1 = bearish_divergence_list[i]["divergence"]["last_ao"]
            y2 = bearish_divergence_list[i]["divergence"]["ao"]
            plt.plot([x1, x2], [y1, y2], color="orange")
        plt.figure(figsize=(15, 8))

        plt.show()
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
        # calculating AO
        ao = data["ao"]
        df["ao"] = ao
        df["itl"] = data["swings"]["itl"]
        df["ith"] = data["swings"]["ith"]

        itl_value = df[df["itl"]]
        ith_value = df[df["ith"]]

        # bullish divergence
        prev_candle_l = itl_value.shift(1)
        mask1 = prev_candle_l["low"] > itl_value["low"]  # price making lower low
        mask2 = prev_candle_l["ao"] < itl_value["ao"]  # ao going high
        mask3 = (prev_candle_l["ao"] < 0) & (itl_value["ao"] < 0)
        bullish_divergence = itl_value[mask1 & mask2 & mask3]

        # bearish divergence
        prev_candle_h = ith_value.shift(1)
        mask1 = prev_candle_h["high"] < ith_value["high"]  # price making higher high
        mask2 = prev_candle_h["ao"] > ith_value["ao"]  # ao going low
        mask3 = (prev_candle_h["ao"] > 0) & (ith_value["ao"] > 0)
        bearish_divergence = ith_value[mask1 & mask2 & mask3]

        # adding changes to dataframe
        df["bullish_divergence"] = False
        df['bearish_divergence'] = False
        bullish_divergence_candle = bullish_divergence.index.tolist()
        bearish_divergence_candle = bearish_divergence.index.tolist()

        df.loc[bearish_divergence_candle, "bearish_divergence"] = True
        df.loc[bullish_divergence_candle, "bullish_divergence"] = True

        return df[["bullish_divergence", "bearish_divergence"]]

