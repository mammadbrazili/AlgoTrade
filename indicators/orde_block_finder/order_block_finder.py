from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter
import pandas as pd

class OrderBlockFinderIndicatorLogic(IndicatorLogic):
    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]
        df["bearish_ob"] = data["order_block"]["bearish_ob"]
        df["bullish_ob"] = data["order_block"]["bullish_ob"]

        def to_dict(df):
            df["bullish_high"] = None
            df["bearish_low"] = None
            df["bullish_low"] = None
            df["bearish_high"] = None

            bullish_ob = df[df["bullish_ob"]]
            bullish_ob["bullish_low"] = bullish_ob["low"]
            bullish_ob["bullish_high"] = bullish_ob["high"]
            bullish_ob_candle = bullish_ob.index.tolist()
            df.loc[bullish_ob_candle, "bullish_low"] = bullish_ob["bullish_low"]
            df.loc[bullish_ob_candle, 'bullish_high'] = bullish_ob["bullish_high"]

            bearish_ob = df[df["bearish_ob"]]
            bearish_ob["bearish_low"] = bearish_ob["low"]
            bearish_ob["bearish_high"] = bearish_ob["high"]
            bearish_ob_candle = bearish_ob.index.tolist()
            df.loc[bearish_ob_candle, "bearish_low"] = bearish_ob["bearish_low"]
            df.loc[bearish_ob_candle, "bearish_high"] = bearish_ob["bearish_high"]

            bu_ob_dict = bullish_ob.to_dict(orient="index")
            be_ob_dict = bearish_ob.to_dict(orient="index")
            return {"bullish": bu_ob_dict, "bearish": be_ob_dict}
        answer = to_dict(df)
        bu_ob_dict = answer["bullish"]
        be_ob_dict = answer["bearish"]

        result_dict = {"ob_bullish": None, "ob_bearish": None, "ob_bullish_high": None,
                       "ob_bullish_low": None, "ob_bearish": None, "ob_bearish_low": None,
                       'ob_bullish_touch': None, "ob_bearish_touch": None,
                       "ob_bullish_index": None, "ob_bearish_index": None}

        for i in reversed(list(bu_ob_dict.keys())):
            span = df.iloc[i+5 :df.index[-1]]
            mask = bu_ob_dict[i]["low"] > span["close"]
            if mask.any():
                continue
            else:
                result_dict["ob_bullish"] = True
                result_dict["ob_bullish_high"] = bu_ob_dict[i]["high"]
                result_dict["ob_bullish_low"] = bu_ob_dict[i]["low"]
                result_dict["ob_bullish_index"] = df.index[-1] - i
                mask = span["low"] <= bu_ob_dict[i]["high"]
                if mask.any():
                    result_dict["ob_bullish_touch"] = True
                else:
                    result_dict["ob_bullish_touch"] = False
                break

        for i in reversed(list(be_ob_dict.keys())):
            span = df.iloc[i+5: df.index[-1]]
            mask = be_ob_dict[i]["high"] < span["close"]
            if mask.any():
                continue
            else:
                result_dict["ob_bearish"] = True
                result_dict["ob_bearish_high"] = be_ob_dict[i]["high"]
                result_dict["ob_bearish_low"] = be_ob_dict[i]["low"]
                result_dict["ob_bearish_index"] = df.index[-1] - i
                mask = span["high"] >= be_ob_dict[i]["low"]
                if mask.any():
                    result_dict["ob_bearish_touch"] = True
                else:
                    result_dict["ob_bearish_touch"] = False
                break

        return result_dict