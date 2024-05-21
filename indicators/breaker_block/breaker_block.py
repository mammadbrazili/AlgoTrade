from indicators.abstracts.indicator import IndicatorLogic
import pandas as pd
from visualization.plotter import Plotter

class BreakerBlockIndicatorLogic(IndicatorLogic):
    @staticmethod
    def visualize(meta_data: dict, data: dict):
        df = data["price"]
        df["breaker_block"] = data["breaker_block"]

        breaker_block = df[df["breaker_block"]]

        # plot candlesticks
        plotter = Plotter()
        plotter.plot_candlestick(df)

        # for Plotting
        breaker_block_value = breaker_block["close"].tolist()
        breaker_block_candle = breaker_block.index.tolist()
        for timestamp, price in zip(breaker_block_candle, breaker_block_value):
            plotter.draw_label(text=None, x=timestamp, y=price, width=0.5, height=0.5, background_color="orange")

        plotter.show()



    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]
        choch = data["choch"]
        choch_up_candle = choch["choch_up_candle"]
        choch_down_candle = choch["choch_down_candle"]

        df["breaker_block"] = False

        # breaker blocks occur at pivots which had choch
        up_breaker_block = list(choch_up_candle.keys())
        down_breaker_block = list(choch_down_candle.keys())

        # we should check that after price mitigate the block, whether it's touched or not
        up_end = list(choch_up_candle.values())
        down_end = list(choch_down_candle.values())

        for i in range(len(down_breaker_block)):
            bb_index = down_breaker_block[i]
            start_span = down_end[i]
            span = df.iloc[start_span: start_span + 10]
            mask = df.loc[bb_index, "low"] > span["close"]
            if mask.any():  # the breaker block is mitigated
                continue
            else:
                # check if block is touched or not
                mask = span["low"] <= df.loc[bb_index, "high"]
                if mask.any():
                    df.loc[bb_index, "breaker_block"] = True

        for i in range(len(up_breaker_block)):
            bb_index = up_breaker_block[i]
            start_span = up_end[i]
            span = df.iloc[start_span: start_span + 10]
            mask = df.loc[bb_index, "high"] < span["close"]
            if mask.any():  # the breaker block is mitigated
                continue
            else:
                # check if the block is touched or not
                mask = span["high"] >= df.loc[bb_index, "low"]
                if mask.any():
                    df.loc[bb_index, "breaker_block"] = True
        return df["breaker_block"]


