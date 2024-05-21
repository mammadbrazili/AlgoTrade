from abc import ABC, abstractmethod
from datetime import datetime
from pytz import timezone
import time


class StrategyLogic(ABC):
    @staticmethod
    @abstractmethod
    def logic(symbol: str, symbol_type: str, meta_data: dict, data: dict, timeframe: str, timestamp: int):
        """
        Main logic method of strategy

        :param symbol: name of the symbol
        :type symbol: str

        :param symbol_type: type of symbol asset
        :type symbol_type: str

        :param timestamp: timestamp of the candle
        :type timestamp: int

        :param timeframe: timeframe of indicator
        :type timeframe: str

        :param meta_data: metadata
        :type meta_data: dict

        :param data: a dictionary including price and indicator data
        :param data: dict

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
    def get_trading_session():
        utc_timestamp = time.time()
        # Define time zones for each city
        tokyo_tz = timezone('Asia/Tokyo')
        sydney_tz = timezone('Australia/Sydney')
        london_tz = timezone('Europe/London')
        new_york_tz = timezone('America/New_York')

        utc_datetime = datetime.utcfromtimestamp(utc_timestamp)

        tokyo_time = utc_datetime.astimezone(tokyo_tz)
        sydney_time = utc_datetime.astimezone(sydney_tz)
        london_time = utc_datetime.astimezone(london_tz)
        new_york_time = utc_datetime.astimezone(new_york_tz)

        tokyo_open = tokyo_time.replace(hour=9, minute=0, second=0)
        tokyo_close = tokyo_time.replace(hour=15, minute=0, second=0)

        sydney_open = sydney_time.replace(hour=9, minute=0, second=0)
        sydney_close = sydney_time.replace(hour=15, minute=0, second=0)

        london_open = london_time.replace(hour=8, minute=0, second=0)
        london_close = london_time.replace(hour=16, minute=0, second=0)

        new_york_open = new_york_time.replace(hour=8, minute=0, second=0)
        new_york_close = new_york_time.replace(hour=16, minute=0, second=0)

        if tokyo_open <= tokyo_time < tokyo_close:
            return "Tokyo"
        elif sydney_open <= sydney_time < sydney_close:
            return "Sydney"
        elif london_open <= london_time < london_close:
            return "London"
        elif new_york_open <= new_york_time < new_york_close:
            return "NewYork"
        else:
            return None
