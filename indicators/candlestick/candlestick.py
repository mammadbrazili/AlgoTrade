import pandas as pd
from visualization.plotter import Plotter
from indicators.abstracts.indicator import IndicatorLogic


class CandleStickIndicatorLogic(IndicatorLogic):


    @staticmethod
    def visualize(meta_data: dict, data: dict):
        df = data["price"]
        patterns = data["patterns"]

        bu_engulf = patterns[patterns["bu_engulf"]]
        be_engulf = patterns[patterns["be_engulf"]]
        bu_darkcloud = patterns[patterns["bu_darkcloud"]]
        be_darkcloud = patterns[patterns["be_darkcloud"]]
        shooting_star = patterns[patterns["shooting_star"]]
        inverted_hammer = patterns[patterns["inverted_hammer"]]
        three_inside_down = patterns[patterns["three_inside_down"]]
        three_inside_up = patterns[patterns["three_inside_up"]]

        # plotting candlesticks
        plotter = Plotter()
        plotter.plot_candlestick(df)

        # plotting patterns
        for i in bu_engulf.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "high"], width=0.5, height=0.5, background_color="blue")

        for i in be_engulf.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "low"], width=0.5, height=0.5, background_color="orange")

        for i in bu_darkcloud.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "high"], width=0.5, height=0.5, background_color="purple")

        for i in be_darkcloud.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "low"], width=0.5, height=0.5, background_color="yellow")

        for i in shooting_star.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "high"], width=0.5, height=0.5, background_color="lightcoral")

        for i in inverted_hammer.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "low"], width=0.5, height=0.5, background_color="khaki")

        for i in three_inside_up.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "low"], width=0.5, height=0.5, background_color="purple")

        for i in three_inside_down.index.tolist():
            plotter.draw_label(text=None, x=i, y=df.loc[i, "high"], width=0.5, height=0.5, background_color="white")

        plotter.show()

    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]

        # basic calculations
        prev_candle = df.shift(1)
        prev_candle_bodysize = abs(prev_candle["open"] - prev_candle["close"])
        current_candle_bodysize = abs(df["open"] - df["close"])
        upper_shadow = abs(df["high"] - ((df["close"] + df["open"]) / 2))
        lower_shadow = abs(df["low"] - ((df["close"] + df["open"]) / 2))
        lookback = df.shift(3)
        next_candle = df.shift(-1)
        def engulfing(df):
            # defining bearish scenario
            mask1 = prev_candle["open"] > prev_candle["close"]  # last candle should be red
            mask2 = df["open"] < df["close"]  # current candle should be green
            mask3 = df["high"] > prev_candle["high"]
            mask4 = prev_candle_bodysize < abs(df["open"] - df["close"])  # current candle should have a larger body
            df["bu_engulf"] = mask1 & mask2 & mask3 & mask4

            # defining bearish scenario
            mask_1 = prev_candle["open"] < prev_candle["close"]  # last candle should be green
            mask_2 = df["open"] > df["close"]  # current candle should be red
            mask_3 = df["low"] < prev_candle["low"]
            mask4 = prev_candle_bodysize < abs(df["open"] - df["close"])  # current candle should have a larger body
            df["be_engulf"] = mask_1 & mask_2 & mask_3 & mask4

            return df[["bu_engulf", "be_engulf"]]
        engulf = engulfing(df)

        def dark_cloud(df):
            # defining Bearish reversal ( last candle is green )
            mask_1 = prev_candle["open"] < prev_candle["close"]  # last candle should be green
            mask_2 = df["open"] > df["close"]  # current candle should be red
            mask_3 = df["open"] > prev_candle["close"]  # Gap Up Condition
            mask_4 = df["close"] < (prev_candle["open"] + prev_candle["close"]) / 2
            # the current candle should be closed lower than 50% of last candle body size
            df["be_darkcloud"] = mask_1 & mask_2 & mask_3 & mask_4

            # defining Bullish reversal (Last candle is red)
            mask1 = prev_candle["open"] > prev_candle["close"]  # last candle should be red
            mask2 = df["open"] < df["close"]  # current candle should be green
            mask3 = df["open"] < prev_candle["close"]  # Gap Down Condition
            mask4 = df["close"] > (prev_candle["open"] + prev_candle["close"]) / 2
            # the current candle should be closed higher than 50% of last candle body size
            df["bu_darkcloud"] = mask1 & mask2 & mask3 & mask4

            return df[["bu_darkcloud", "be_darkcloud"]]
        darkcloud = dark_cloud(df)


        def shooting_star(df):
            mask1 = upper_shadow > 2 * current_candle_bodysize
            # upper shadow should be at least more than twice of the body
            mask2 = upper_shadow > lower_shadow  # upper shadow should be more than lower shadow
            mask3 = lookback["open"] < df["open"]  # we should be in uptrend
            # mask4 = df["open"] > prev_candle ["close"]            # Gap Up Condition

            df["shooting_star"] = mask1 & mask2 & mask3
            return df["shooting_star"]
        shootingstar = shooting_star(df)

        def inverted_hammer(df):
            mask1 = upper_shadow > 2 * current_candle_bodysize
            # upper shadow shoud be at least more than twice of the body
            mask2 = upper_shadow > lower_shadow  # upper shadow should be more than lower shadow
            mask3 = lookback["open"] > df["open"]  # we should be in downtrend
            # mask4 = df["open"] < prev_candle["close"]             # Gap down Condition

            df["inverted_hammer"] = mask1 & mask2 & mask3
            return df["inverted_hammer"]
        inverted_hammer = inverted_hammer(df)

        def three_inside_down(df):
            mask1 = prev_candle["open"] < prev_candle["close"]
            # last candle should be green
            mask2 = df["open"] > df["close"]  # current candle should be red
            mask3 = next_candle["open"] > next_candle["close"]  # next candle should be red
            # the current candle should be closed lower than 50% of last candle body size
            mask4 = df["close"] < (prev_candle["open"] + prev_candle["close"]) / 2
            mask5 = df["close"] > prev_candle["open"]  # the second candle shouldn't engulf the first candle
            mask6 = next_candle["close"] < prev_candle["low"]
            # the third candle should be closed lower than first(bullish)
            # candle

            df["three_inside_down"] = mask1 & mask2 & mask3 & mask4 & mask5 & mask6
            return df["three_inside_down"]
        three_inside_down = three_inside_down(df)

        def three_inside_up(df):
            mask1 = prev_candle["open"] > prev_candle["close"]
            # last candle should be red
            mask2 = df["open"] < df["close"]  # current candle should be green
            mask3 = next_candle["open"] < next_candle["close"]  # next candle should be green
            # the current candle should be closed higher than 50% of last candle body size
            mask4 = df["close"] > (prev_candle["open"] + prev_candle["close"]) / 2
            mask5 = df["close"] < prev_candle["open"]  # the second candle shouldn't engulf the first candle
            mask6 = next_candle["close"] > prev_candle["high"]  # the third candle should be closed higher than first(
            # bullish) candle

            df["three_inside_up"] = mask1 & mask2 & mask3 & mask4 & mask5 & mask6
            return df["three_inside_up"]
        three_inside_up = three_inside_up(df)

        return df[["three_inside_up","three_inside_down", "inverted_hammer","shooting_star",
                   "bu_darkcloud", "be_darkcloud", "bu_engulf", "be_engulf"]]
