import pandas as pd
from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter

class ObSingleTimeFrameIndicatorLogic(IndicatorLogic):
    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]
        df["bearish_ob"] = data["order_block"]["bearish_ob"]
        df["bullish_ob"] = data["order_block"]["bullish_ob"]
        bullish_ob = df[df["bullish_ob"]]
        bearish_ob = df[df["bearish_ob"]]

        df["bullish_high"] = None
        df["bearish_low"] = None
        df["bullish_low"] = None
        df["bearish_high"] = None
        df["not_mitigated_bu_ob"] = False
        df["not_mitigated_be_ob"] = False

        bullish_ob_candle = bullish_ob.index.tolist()
        df.loc[bullish_ob_candle, "bullish_low"] = df.loc[bullish_ob_candle, "low"]
        df.loc[bullish_ob_candle, "bullish_high"] = df.loc[bullish_ob_candle, "high"]

        bearish_ob_candle = bearish_ob.index.tolist()
        df.loc[bearish_ob_candle, "bearish_low"] = df.loc[bearish_ob_candle, "low"]
        df.loc[bearish_ob_candle, "bearish_high"] = df.loc[bearish_ob_candle, "high"]

        # finding not mitigated bullish order blocks
        for i in bullish_ob.index.tolist():
            span = df.iloc[i+5:df.index[-1]]
            mask = df.loc[i, "low"] > span["close"]
            if mask.any():  # if True --> the bullish order block is mitigated
                continue
            else:
                # check the order block is touched or not
                mask = span["low"] <= df.loc[i, "high"]
                if mask.any():
                    df.loc[i, "not_mitigated_bu_ob"] = True
                break

        # finding not mitigated bearish order blocks
        for i in bearish_ob.index.tolist():
            span = df.iloc[i+5:df.index[-1]]
            mask = df.loc[i, "high"] < span["close"]
            if mask.any():  # if True --> the bearish order block is mitigated
                continue
            else:
                # check the order block is touched or not
                mask = span["high"] >= df.loc[i, "low"]
                if mask.any():
                    df.loc[i, "not_mitigated_be_ob"] = True
                break

        not_mitigated_be_ob = df[df["not_mitigated_be_ob"]]
        not_mitigated_bu_ob = df[df["not_mitigated_bu_ob"]]

        df["valid_bu_ob"] = False
        df["valid_be_ob"] = False

        # check if we have a lower order block for each not mitigated bearish OB --> it means we have 2 BOS
        for i in not_mitigated_be_ob.index.tolist():
            # get the value of order block
            order_block_low = df.loc[i, "low"]

            # finding the first bearish OB which is lower than this OB
            a = df.loc[i + 1:, "bearish_high"].lt(order_block_low).idxmax()
            df.loc[a, "valid_be_ob"] = True

        # check if we have a higher order block for each not mitigated bullish OB --> it means we have 2 BOS
        for i in not_mitigated_bu_ob.index.tolist():
            # get the value of order block
            order_block_high = df.loc[i, "high"]

            # finding the first bullish OB which is higher than this OB
            a = df.loc[i + 1:, "bullish_low"].gt(order_block_high).idxmax()
            df.loc[a, "valid_bu_ob"] = True

        # reindexing dataframe in reverse
        df = df.set_index(pd.Index(range(len(df)-1, -1, -1)))

        valid_be_ob = df[df["valid_be_ob"]].to_dict(orient="index")
        valid_bu_ob = df[df["valid_bu_ob"]].to_dict(orient="index")

        valid_ob = {"be_ob_index": None, "be_ob_high": None, "be_ob_low": None,
                    "bu_ob_index": None, "bu_ob_high": None, "bu_ob_low": None}

        if len(valid_be_ob.keys()) == 0:
            pass
        else:
            index = list(valid_be_ob.keys())[-1]
            valid_ob["be_ob_index"] = index
            valid_ob["be_ob_high"] = valid_be_ob[index]["high"]
            valid_ob["be_ob_low"] = valid_be_ob[index]["low"]

        if len(valid_bu_ob.keys()) == 0:
            pass
        else:
            index = list(valid_bu_ob.keys())[-1]
            valid_ob["bu_ob_index"] = index
            valid_ob["bu_ob_high"] = valid_bu_ob[index]["high"]
            valid_ob["bu_ob_low"] = valid_bu_ob[index]["low"]

        return valid_ob
