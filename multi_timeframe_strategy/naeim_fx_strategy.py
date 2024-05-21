from multi_timeframe_strategy.abstract import StrategyLogic
from indicators.order_block.order_block import OrderBlockIndicatorLogic
from indicators.ao_divergence.ao_divergence import AoDivergenceIndicatorLogic

class OrderBlockStrategy(StrategyLogic):

    @staticmethod
    def logic(meta_data: dict, data_lower: dict, data_higher: dict, timeframe_lower: str, timeframe_higher: str):
        order_block_higher = data_higher["order_block"]
        price_higher = data_higher["price"]
        length_candle = OrderBlockStrategy.get_lower_candle_length(timeframe_lower, timeframe_higher)

        bullish_order_block = order_block_higher[order_block_higher["bullish_ob"]]
        bearish_order_block = order_block_higher[order_block_higher["bearish_ob"]]
        last_candle = price_higher.iloc[-1]
        last_candle_index = last_candle.index

        # bullish scenario
        last_bullish_ob = bullish_order_block.iloc[-1]
        last_bullish_ob_index = last_bullish_ob.index

        # last candle should touch order block area
        mask1 = last_candle["low"] <= last_bullish_ob_index["high"]
        # last candle close shouldn't engulf the block
        mask2 = last_candle["close"] > last_bullish_ob["low"]
        last_candle_condition = mask1 & mask2
        if last_candle_condition :
            ao_lower = data_lower["ao_divergence"]
            span = ao_lower.iloc[-length_candle:]
            if span["bullish_divergence"].any():
                entry = last_candle["low"]
                sl = last_bullish_ob["low"]
                tp = entry + 3*(abs(entry-sl))
                return True

        # bearish scenario
        last_bearish_ob = bearish_order_block.iloc[-1]
        # last candle should touch order block area
        mask1 = last_candle["high"] >= last_bearish_ob["low"]
        # last candle close shouldn't engulf the block
        mask2 = last_candle["close"] < last_bearish_ob["high"]
        last_candle_condition = mask1 & mask2

        if last_candle_condition:
            ao_lower = data_lower["ao_divergence"]
            ao_lower.iloc[length_candle]
            span = ao_lower.iloc[-length_candle:]
            if span["bearish_divergence"].any():
                entry = last_candle["high"]
                sl = last_bearish_ob["high"]
                tp = entry - 3*(abs(entry-sl))
                return True











