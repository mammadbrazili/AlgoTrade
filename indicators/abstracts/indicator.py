from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict
import time


class IndicatorLogic(ABC):
    """
    Interface for indicator calculations
    """

    @staticmethod
    @abstractmethod
    def logic(
            meta_data: dict
            , data: dict
            , timeframe: str):
        """
        Main method for producing indicator raw results
        :param timeframe: timeframe of indicator
        :type timeframe: str

        :param meta_data: any data not related to price data and needed for calculations.
        :type meta_data: dict

        :param data: price or indicator data
        :type data: dict

        :return: a dict of raw indicator results.
        """
        pass

    @staticmethod
    def _get_time(timeframe: str):
        """
        Rounds time to timeframe
        :param timeframe: timeframe of indicator
        :type timeframe: str
        :return:
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
    @abstractmethod
    def visualize(meta_data: dict, data: dict):
        """
        Visualization pipeline for indicator
        :param meta_data: any data not related to price data and needed for calculations.
        :type meta_data: dict
        :param data: price or indicator data
        :type data: dict
        """
        pass
