import pandas as pd
from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter

class TrendFinderIndicatorLogic(IndicatorLogic):
    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]
        df["major_stl"] = data["bos"]["major_stl"]
        df["major_sth"] = data["bos"]["major_sth"]

