import time
from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter
import pandas as pd

class StaticSupportResistanceIndicatorLogic(IndicatorLogic):
    """
    Interface for Finding Static Support & Resistance calculations
    """

    @staticmethod
    def visualize(data: dict):
        """
        Visualization pipeline for indicator

        :param meta_data: any data not related to price data and needed for calculations.
        :type meta_data: dict

        :param data: price or indicator data
        :type data: dict

        """
        price = data["price_candle"]
        levels = data["indicator"]

        # plot candlesticks
        plotter = Plotter()
        plotter.plot_candlestick(price)

        # plotting levels
        for i in levels.dropna().tolist():
            plotter.draw_hline(y=i , color="r")
        plotter.show()


    @staticmethod
    def logic(meta_data: dict, data: dict, time_frame: str):
        """
        Support & Resistance indicator logic & calculations

        :param time_frame: timeframe of indicator
        :type time_frame: str

        :param meta_data: any data not related to price data and needed for calculations.
        :type meta_data: dict

        :param data: price or indicator data
        :type data: dict

        :return: a dict concluding ma & upper/lower curve panda series
        """
        # finding prices
        price = data["price"]

        # achieving the window length through meta_data
        length = meta_data["length"]

        # finding resistances
        max_values = price['high'].rolling(window=length, min_periods=1, center=True).max()
        is_local_max = (price['high'] >= max_values)
        resistance = price["high"][is_local_max]

        # finding key resistances(keep if the differences between to levels > average candle size )
        # average candle size calculations
        avg = (price["high"] - price["low"]).mean()
        mean = pd.DataFrame(avg).T

        # calculating key resistances
        # adding mean row to resistance dataframe
        resistance = pd.concat([resistance, mean], ignore_index=True)

        def key_resistance(column):
            column = column.dropna()
            mean = column.iloc[-1]
            key_resistance = column[abs(column.diff()) > mean][:-1]
            return key_resistance
        key_resistance = resistance.apply(key_resistance)

        # findning supports
        min_values = price['low'].rolling(window=length, min_periods=1, center=True).min()
        is_local_min = (price['low'] <= min_values)
        support = price["low"][is_local_min]

        # calculating key supports
        # adding mean row to support dataframe
        support = pd.concat([support, mean], ignore_index=True)

        def key_support(column):
            column = column.dropna()
            mean = column.iloc[-1]
            key_support = column[abs(column.diff()) > mean][:-1]
            return key_support
        key_support = support.apply(key_support)

        # adjoin levels
        levels = pd.concat([key_support, key_resistance], ignore_index=True)

        # filtering agin
        levels = pd.concat([levels, mean], ignore_index=True)

        def key_levels(column):
            column = column.dropna()
            mean = column.iloc[-1]
            key_levels = column[abs(column.diff()) > mean][:-1]
            return key_levels

        key_levels = levels.apply(key_levels)

        return key_levels


# testing to check all -symbols and their levels

# meta_data = {"length": 5}
# data = {"price" :pd.read_csv("C:/signal/signal_khosro/symbol_df.csv", index_col=0, header=[0, 1])}
# time_frame = "1H"
# start = time.time()
# a = StaticSupportResistanceIndicatorLogic()
# a.logic(meta_data, data, time_frame)
# end= time.time()
# l = end - start
# print(a.logic(meta_data, data, time_frame)["AAPL"].dropna())
# print(l)
