from indicators.abstracts.indicator import IndicatorLogic
class AOIndicatorLogic(IndicatorLogic):

    @staticmethod
    def visualize(meta_data: dict, data: dict):
        pass

    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]
        short_period = meta_data["short_period"]
        long_period = meta_data["long_period"]
        # Calculate the simple moving averages (SMAs)
        sma_short = df["close"].rolling(window=short_period).mean()
        sma_long = df["close"].rolling(window=long_period).mean()
        # Calculate the Awesome Oscillator (AO)
        ao = sma_short - sma_long
        return ao


