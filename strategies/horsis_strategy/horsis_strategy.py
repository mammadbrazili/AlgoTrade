from strategies.abstracts.strategy import StrategyLogic
from strategies.abstracts.signal import Signal

class HorsisStrategyLogic(StrategyLogic):
    @staticmethod
    def logic(symbol: str, symbol_type: str, meta_data: dict, data: dict, timeframe: str, timestamp: int):
        valid_blocks = data["valid_blocks"]
        signal = Signal()
        signal.strategy_name = "horsis"
        signal.symbol_type = symbol_type
        signal.session = HorsisStrategyLogic.get_trading_session()
        signal.timeframes = [timeframe]
        signal.indicators_info["data"] = valid_blocks
        signal.status = "pending"
        signal.activate_type = "normal"


        valid_bullish_ob = []
        valid_bearish_ob = []
        for i in valid_blocks:
            if i["direction"] == "bullish":
                valid_bullish_ob.append(i)
            elif i["direction"] == "bearish":
                valid_bearish_ob.append(i)

        # bearish signal
        if not len(valid_bearish_ob) == 0:
            signal.direction = "bearish"
            signal.entry = valid_bearish_ob[0]["be_ob_low"]
            signal.sl = valid_bearish_ob[0]["be_ob_high"]
            signal.timestamps_discovery = {timeframe: timestamp}
            signal.tp_not_done = [signal.entry - 3 * (signal.sl - signal.entry) ,
                                  signal.entry - 5 * (signal.sl - signal.entry),
                                  signal.entry - 7.5 * (signal.sl - signal.entry)]

        # bullish signal
        if not len(valid_bullish_ob) == 0:
            signal.direction = "bullish"
            signal.entry = valid_bullish_ob[0]["bu_ob_high"]
            signal.sl = valid_bearish_ob[0]["bu_ob_low"]
            signal.timestamps_discovery = {timeframe: timestamp}
            signal.tp_not_done = [signal.entry + 3*(signal.entry - signal.sl),
                                  signal.entry + 5*(signal.entry - signal.sl),
                                  signal.entry + 7.5*(signal.entry - signal.sl)]

        signal = signal.validate()
        return signal.to_dict()
