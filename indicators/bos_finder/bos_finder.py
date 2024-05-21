from indicators.abstracts.indicator import IndicatorLogic
from visualization.plotter import Plotter
import pandas as pd

class BosFinderIndicatorLogic(IndicatorLogic):

    @staticmethod
    def visualize(meta_data: dict, data: dict):
        df = data["price"]

        # candlestick plot
        plotter = Plotter()
        plotter.plot_candlestick(df)

        # plot pivots movement
        major_sth = df[df["major_sth"]]
        major_stl = df[df["major_stl"]]

        major_stl_index = major_stl.index.tolist()
        major_sth_index = major_sth.index.tolist()

        major_stl_value = major_stl["low"].values.tolist()
        major_sth_value = major_sth["high"].values.tolist()

        major_stls = pd.DataFrame({"value": major_stl_value})
        major_stls = major_stls.set_index(pd.Index(major_stl_index))

        major_sths = pd.DataFrame({"value": major_sth_value})
        major_sths = major_sths.set_index(pd.Index(major_sth_index))

        major_pivots = pd.concat([major_stls, major_sths]).sort_index()
        plotter.plot(major_pivots["value"])

        # plotting bos points
        bu_bos = df[df["bu_bos"]]
        be_bos = df[df["be_bos"]]
        for bu_bos_value, bu_bos_index in zip(bu_bos["high"].values.tolist(), bu_bos.index.tolist()):
            plotter.draw_label(text=None, x=bu_bos_index, y=bu_bos_value, width=0.5, height=0.5, background_color="white")

        for be_bos_value, be_bos_index in zip(be_bos["low"].values.tolist(), be_bos.index.tolist()):
            plotter.draw_label(text=None, x=be_bos_index, y=be_bos_value, width=0.5, height=0.5, background_color="blue")

        plotter.show()

    @staticmethod
    def logic(meta_data: dict, data: dict, timeframe: str):
        df = data["price"]
        df["sth"] = data["swings"]["sth"]
        df["stl"] = data["swings"]["stl"]
        # delete consecutive sth/stl in rows
        sth = df[df["sth"]]
        stl = df[df["stl"]]
        # adjoining high and low pivots
        pivots = pd.concat([stl, sth]).sort_index()

        # deleting rows if a candle is both stl or sth
        mask1 = pivots["stl"] != pivots["sth"]
        pivots = pivots[mask1].reset_index()
        # keep the lowest value of stl, if we have consecutive stls
        pivots["group"] = (pivots["stl"] != pivots["stl"].shift()).cumsum()
        d = pivots.groupby("group").min()

        # keep the highest value of sth if we have consecutive sths
        d.reset_index(drop=True, inplace=True)
        d["group"] = (d["sth"] != d["sth"].shift()).cumsum()
        d = pivots.groupby("group").max()

        # final pivots dataframe (in which there is no 2 sth or stl continously )
        pivots = d.reset_index().set_index("index")

        # adding major pivot points to the dataframe
        df["major_stl"] = False
        major_stl_candles = pivots[pivots["stl"]].index.tolist()
        df.loc[major_stl_candles, "major_stl"] = True

        df["major_sth"] = False
        major_sth_candles = pivots[pivots["sth"]].index.tolist()
        df.loc[major_sth_candles, "major_sth"] = True

        df["bu_bos"] = False
        next_pivot = pivots.shift(-1)
        two_next_pivot = pivots.shift(-2)
        mask = (two_next_pivot["high"] > pivots["high"]) & (next_pivot["high"] < pivots["high"])
        bu_bos = pivots[mask]

        # adding points to dataframe
        bu_bos_candles = bu_bos.index.tolist()
        df.loc[bu_bos_candles, "bu_bos"] = True

        # bearish bos
        df["be_bos"] = False
        mask = (two_next_pivot["low"] < pivots["low"]) & (next_pivot["low"] > pivots["low"])
        be_bos = pivots[mask]
        # adding points to dataframe
        be_bos_candles = be_bos.index.tolist()
        df.loc[be_bos_candles, "be_bos"] = True

        return df[["be_bos", "bu_bos","major_stl", "major_sth"]]