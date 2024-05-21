from abc import ABC, abstractmethod
import time


class StrategyLogic(ABC):
    @staticmethod
    @abstractmethod
    def logic(meta_data: dict, data_lower: dict, data_higher: dict, timeframe_lower: str, timeframe_higher: str):
        """
        Main logic method of strategy

        :param timeframe_lower: lower timeframe of strategy
        :type timeframe_lower: str

        :param timeframe_higher: higher timeframe of strategy
        :type timeframe_higher: str

        :param meta_data: metadata
        :type meta_data: dict

        :param data_lower: a dictionary including price and indicator data of lower timeframe
        :param data_lower: dict

        :param data_higher: a dictionary including price and indicator data of higher timeframe
        :param data_higher: dict

        :return: returns a dictionary containing harmonic pattern details for all symbols

        """
        pass

    @staticmethod
    def _get_time(timeframe: str):
        """
        Rounds time to timeframe

        :param timeframe: timeframe of indicator
        :return: rounded timestamp
        """
        current_time = time.time()
        rounded_time = int(current_time)

        if timeframe == "1m":
            rounded_time -= int(current_time) % 60
        elif timeframe == "5m":
            rounded_time -= int(current_time) % 300
        elif timeframe == "15m":
            rounded_time -= int(current_time) % 900
        elif timeframe == "30m":
            rounded_time -= int(current_time) % 1800
        elif timeframe == "1h":
            rounded_time -= int(current_time) % 3600
        elif timeframe == "4h":
            rounded_time -= int(current_time) % 14400
        elif timeframe == "1d":
            rounded_time -= int(current_time) % 86400
        elif timeframe == "1w":
            rounded_time -= int(current_time) % 604800
        elif timeframe == "1M":
            rounded_time -= int(current_time) % 2628000

        return rounded_time

    @staticmethod
    def is_last_candle(timeframe, timestamp):
        timeframe_to_minutes = {
            '1m': 1,
            '2m': 2,
            '5m': 5,
            '15m': 15,
            '30m': 30,
            '1h': 60,
            '4h': 240,
            '1d': 1440,
            '1w': 10080,
            '1M': 43200
        }

        current_timestamp = time.time()
        minutes_passed = (current_timestamp - timestamp) // 60
        candles_passed = minutes_passed // timeframe_to_minutes[timeframe]
        print(current_timestamp, timestamp, candles_passed)
        return candles_passed <= 1

    @staticmethod
    def get_lower_candle_length(timeframe_lower, timeframe_higher):
        timeframe_to_minutes = {
            '1m': 1,
            '2m': 2,
            '5m': 5,
            '15m': 15,
            '30m': 30,
            '1h': 60,
            '4h': 240,
            '1d': 1440,
            '1w': 10080,
            '1M': 43200
        }
        return int(timeframe_to_minutes[timeframe_higher]/timeframe_to_minutes[timeframe_lower])