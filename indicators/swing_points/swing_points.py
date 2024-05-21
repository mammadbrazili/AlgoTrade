import time

from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter
import pandas as pd

class SwingPointsIndicatorLogic(IndicatorLogic):
    """
    Interface for Finding Swing Points calculations
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
        kind = meta_data["kind"]
        swing_points = data["indicator"][kind]
        if kind == "stl":
            color = "lightcoral"
        elif kind == "sth":
            color = "limegreen"
        elif kind == "itl":
            color = "orange"
        elif kind == "ith":
            color = "royalblue"
        elif kind == "ltl":
            color = "yellow"
        elif kind == "lth":
            color = "purple"
        swing_points_price = swing_points.values
        swing_points_timestamp = swing_points.index


        # plot candlesticks
        plotter = Plotter()
        plotter.plot_candlestick(df)

        # plotting swing points
        for timestamp, price in zip(swing_points_timestamp, swing_points_price):
            plotter.draw_label(text= None, x=timestamp, y=price, width=0.5, height=0.5, background_color=color)

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
        # finding prices
        df = data["price"]

        # achieving the swing point's kind through meta_data
        kind = meta_data["kind"]

        # finding Short_Term_Low's (STL) --> if a candle's low, is lower than both next and previous lows
        if kind == "stl":
            data_stl_prev = df["low"].shift(1)
            data_stl_next = df['low'].shift(-1)
            data_stl_mask = ((df['low'] < data_stl_prev) & (df['low'] < data_stl_next))
            stl_value = df["low"][data_stl_mask]
            return {"stl": stl_value}

        # finding Short_Term_High's (STH) --> if a candle's high, is higher than both next and previous high
        elif kind == "sth":
            data_sth_prev = df["high"].shift(1)
            data_sth_next = df['high'].shift(-1)
            data_sth_mask = ((df['high'] > data_sth_prev) & (df['high'] > data_sth_next))
            sth_value = df["high"][data_sth_mask]
            return {"sth": sth_value}

        # finding Intermediate_Term_Low (ITL) --> if a STL is lower than both next and previous STL
        elif kind == "itl":
            # finding STL
            data_stl_prev = df["low"].shift(1)
            data_stl_next = df['low'].shift(-1)
            data_stl_mask = ((df['low'] < data_stl_prev) & (df['low'] < data_stl_next))
            stl_value = df["low"][data_stl_mask]

            # finding ITL
            def itl_finder(column):
                stl_value_drop = column.dropna()
                stl_prev = stl_value_drop.shift(1)
                stl_next = stl_value_drop.shift(-1)
                itl_mask = ((stl_value_drop < stl_prev) & (stl_value_drop < stl_next))
                itl_value = stl_value_drop[itl_mask]
                return itl_value

            # if we have multi symbols
            if isinstance(stl_value, pd.DataFrame):
                itl_value = stl_value.apply(itl_finder)
            # if we have one symbol
            else:
                stl_prev = stl_value.shift(1)
                stl_next = stl_value.shift(-1)
                itl_mask = ((stl_value < stl_prev) & (stl_value < stl_next))
                itl_value = stl_value[itl_mask]

            return {"itl": itl_value}

        # finding Intermediate_Term_High (ITH) --> if a STH is higher than both next and previous STH
        elif kind == "ith":
            # finding STH
            data_sth_prev = df["high"].shift(1)
            data_sth_next = df['high'].shift(-1)
            data_sth_mask = ((df['high'] > data_sth_prev) & (df['high'] > data_sth_next))
            sth_value = df["high"][data_sth_mask]

            # finding ITH
            def ith_finder(column):
                sth_value_drop = column.dropna()
                sth_prev = sth_value_drop.shift(1)
                sth_next = sth_value_drop.shift(-1)
                ith_mask = ((sth_value_drop > sth_prev) & (sth_value_drop > sth_next))
                ith_value = sth_value_drop[ith_mask]
                return ith_value

            # if we have multi symbols
            if isinstance(sth_value, pd.DataFrame):
                ith_value = sth_value.apply(ith_finder)
            #if we have one symbol
            else:
                sth_prev = sth_value.shift(1)
                sth_next = sth_value.shift(-1)
                ith_mask = ((sth_value > sth_prev) & (sth_value > sth_next))
                ith_value = sth_value[ith_mask]
            return {"ith": ith_value}

        # finding Long_Term_low (LTL) --> If an ITL is lower than both next and previous ITL
        elif kind == "ltl":
            # finding STL
            data_stl_prev = df["low"].shift(1)
            data_stl_next = df['low'].shift(-1)
            data_stl_mask = ((df['low'] < data_stl_prev) & (df['low'] < data_stl_next))
            stl_value = df["low"][data_stl_mask]

            # finding ITL
            def itl_finder(column):
                stl_value_drop = column.dropna()
                stl_prev = stl_value_drop.shift(1)
                stl_next = stl_value_drop.shift(-1)
                itl_mask = ((stl_value_drop < stl_prev) & (stl_value_drop < stl_next))
                itl_value = stl_value_drop[itl_mask]
                return itl_value

            # if we have multi symbols
            if isinstance(stl_value, pd.DataFrame):
                itl_value = stl_value.apply(itl_finder)
            # if we have one symbol
            else:
                stl_prev = stl_value.shift(1)
                stl_next = stl_value.shift(-1)
                itl_mask = ((stl_value < stl_prev) & (stl_value < stl_next))
                itl_value = stl_value[itl_mask]

            # finding LTL
            def ltl_finder(column):
                itl_value_drop = column.dropna()
                itl_prev = itl_value_drop.shift(1)
                itl_next = itl_value_drop.shift(-1)
                ltl_mask = ((itl_value_drop < itl_prev) & (itl_value_drop < itl_next))
                ltl_value = itl_value_drop[ltl_mask]

                return ltl_value

            if isinstance(itl_value, pd.DataFrame):
                ltl_value = itl_value.apply(ltl_finder)

            else:
                itl_prev = itl_value.shift(1)
                itl_next = itl_value.shift(-1)
                ltl_mask = ((itl_value < itl_prev) & (itl_value < itl_next))
                ltl_value = itl_value[ltl_mask]
            return {"ltl": ltl_value}

        # finding Long_Term_High (LTH) --> If an ITH is higher than both next and previous ITH
        elif kind == "lth":
            # finding STH
            data_sth_prev = df["high"].shift(1)
            data_sth_next = df['high'].shift(-1)
            data_sth_mask = ((df['high'] > data_sth_prev) & (df['high'] > data_sth_next))
            sth_value = df["high"][data_sth_mask]

            # finding ITH
            def ith_finder(column):
                sth_value_drop = column.dropna()
                sth_prev = sth_value_drop.shift(1)
                sth_next = sth_value_drop.shift(-1)
                ith_mask = ((sth_value_drop > sth_prev) & (sth_value_drop > sth_next))
                ith_value = sth_value_drop[ith_mask]
                return ith_value

            # if we have multi symbols
            if isinstance(sth_value, pd.DataFrame):
                ith_value = sth_value.apply(ith_finder)
            #if we have one symbol
            else:
                sth_prev = sth_value.shift(1)
                sth_next = sth_value.shift(-1)
                ith_mask = ((sth_value > sth_prev) & (sth_value > sth_next))
                ith_value = sth_value[ith_mask]

            # finding LTH
            def lth_finder(column):
                ith_value_drop = column.dropna()
                ith_prev = ith_value_drop.shift(1)
                ith_next = ith_value_drop.shift(-1)
                lth_mask = ((ith_value_drop > ith_prev) & (ith_value_drop > ith_next))
                lth_value = ith_value_drop[lth_mask]

                return lth_value

            if isinstance(ith_value, pd.DataFrame):
                lth_value = ith_value.apply(lth_finder)

            else:
                ith_prev = ith_value.shift(1)
                ith_next = ith_value.shift(-1)
                lth_mask = ((ith_value > ith_prev) & (ith_value > ith_next))
                lth_value = ith_value[lth_mask]
            return {"lth": lth_value}

        elif kind == "all":
            # finding STL
            data_stl_prev = df["low"].shift(1)
            data_stl_next = df['low'].shift(-1)
            data_stl_mask = ((df['low'] < data_stl_prev) & (df['low'] < data_stl_next))
            stl_value = df["low"][data_stl_mask]

            # finding ITL
            def itl_finder(column):
                stl_value_drop = column.dropna()
                stl_prev = stl_value_drop.shift(1)
                stl_next = stl_value_drop.shift(-1)
                itl_mask = ((stl_value_drop < stl_prev) & (stl_value_drop < stl_next))
                itl_value = stl_value_drop[itl_mask]
                return itl_value

            # if we have multi symbols
            if isinstance(stl_value, pd.DataFrame):
                itl_value = stl_value.apply(itl_finder)
            # if we have one symbol
            else:
                stl_prev = stl_value.shift(1)
                stl_next = stl_value.shift(-1)
                itl_mask = ((stl_value < stl_prev) & (stl_value < stl_next))
                itl_value = stl_value[itl_mask]

            # finding LTL
            def ltl_finder(column):
                itl_value_drop = column.dropna()
                itl_prev = itl_value_drop.shift(1)
                itl_next = itl_value_drop.shift(-1)
                ltl_mask = ((itl_value_drop < itl_prev) & (itl_value_drop < itl_next))
                ltl_value = itl_value_drop[ltl_mask]

                return ltl_value

            if isinstance(itl_value, pd.DataFrame):
                ltl_value = itl_value.apply(ltl_finder)

            else:
                itl_prev = itl_value.shift(1)
                itl_next = itl_value.shift(-1)
                ltl_mask = ((itl_value < itl_prev) & (itl_value < itl_next))
                ltl_value = itl_value[ltl_mask]

            # finding STH
            data_sth_prev = df["high"].shift(1)
            data_sth_next = df['high'].shift(-1)
            data_sth_mask = ((df['high'] > data_sth_prev) & (df['high'] > data_sth_next))
            sth_value = df["high"][data_sth_mask]

            # finding ITH
            def ith_finder(column):
                sth_value_drop = column.dropna()
                sth_prev = sth_value_drop.shift(1)
                sth_next = sth_value_drop.shift(-1)
                ith_mask = ((sth_value_drop > sth_prev) & (sth_value_drop > sth_next))
                ith_value = sth_value_drop[ith_mask]
                return ith_value

            # if we have multi symbols
            if isinstance(sth_value, pd.DataFrame):
                ith_value = sth_value.apply(ith_finder)
            #if we have one symbol
            else:
                sth_prev = sth_value.shift(1)
                sth_next = sth_value.shift(-1)
                ith_mask = ((sth_value > sth_prev) & (sth_value > sth_next))
                ith_value = sth_value[ith_mask]


            # finding LTH
            def lth_finder(column):
                ith_value_drop = column.dropna()
                ith_prev = ith_value_drop.shift(1)
                ith_next = ith_value_drop.shift(-1)
                lth_mask = ((ith_value_drop > ith_prev) & (ith_value_drop > ith_next))
                lth_value = ith_value_drop[lth_mask]

                return lth_value

            if isinstance(ith_value, pd.DataFrame):
                lth_value = ith_value.apply(lth_finder)

            else:
                ith_prev = ith_value.shift(1)
                ith_next = ith_value.shift(-1)
                lth_mask = ((ith_value > ith_prev) & (ith_value > ith_next))
                lth_value = ith_value[lth_mask]


            return {"stl": stl_value, "sth": sth_value, "itl": itl_value, "ith": ith_value,
                    "ltl": ltl_value, "lth": lth_value}

# testing to check all -symbols and all swing points

# meta_data = {"kind": "all"}
# data = {"price" :pd.read_csv("C:/signal/signal_khosro/symbol_df.csv", index_col=0, header=[0, 1])}
# time_frame = "1H"
# start = time.time()
# a = SwingPointsIndicatorLogic()
# a.logic(meta_data, data, time_frame)
# end= time.time()
# l = end - start
# print(l)