import warnings
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import patches as patches
from .vis_config import VisConfig
import io

warnings.filterwarnings("ignore")


class Plotter:
    """
    Visualization tools to test indicators results
    """

    def __init__(self, secondaries_num: int = 0, secondaries_titles: list = None):
        """
        :param secondaries_num: number of secondary plots
        :type secondaries_num: int

        :param secondaries_titles: title of secondary plots
        :type secondaries_titles: list

        """
        plt.style.use('dark_background')
        size = (VisConfig.width, VisConfig.main_size + VisConfig.secondary_size * secondaries_num)
        ratios = [VisConfig.main_size] + [VisConfig.secondary_size] * secondaries_num
        fig, ax = plt.subplots(1 + secondaries_num, 1, height_ratios=ratios, figsize=size, dpi=VisConfig.dpi)
        self.fig = fig
        if secondaries_num == 0:
            self.main = ax
            self.secondaries = []
        else:
            self.main = ax[0]
            self.secondaries = ax[1:]

        self._set_theme(secondaries_titles)
        self._set_grid()
        self._set_margin()

    def _set_theme(self, secondaries_titles: list):
        """
        Sets the color and theme of the plot

        :param secondaries_titles: titles of secondary plots
        :type secondaries_titles: list
        """
        background_color = VisConfig.background_color
        for i, a in enumerate(self.secondaries):
            a.set_title(secondaries_titles[i], fontsize=VisConfig.text_fontsize)
            a.set_facecolor(background_color)
            a.tick_params(axis='both', which="major", labelsize=VisConfig.label_fontsize)
        self.main.set_title("Price", fontsize=VisConfig.text_fontsize)
        self.main.set_facecolor(background_color)
        self.main.tick_params(axis='both', which="major", labelsize=VisConfig.label_fontsize)
        self.fig.set_facecolor(background_color)

    def _set_grid(self):
        """
        Sets grid for main plot
        """
        plt.rcParams['grid.color'] = VisConfig.grid_color
        self.main.grid(alpha=VisConfig.grid_alpha)

    def _set_margin(self):
        """
        Sets margin of plot
        """
        self.fig.tight_layout()

    def _get_plot(self, subplot: str):
        """
        Gets a plot by string input of subplot name or index

        :param subplot: name of index of subplot
        :type subplot: str

        :return: specified plot
        """
        if subplot == "main":
            ax = self.main
        else:
            ax = self.secondaries[int(subplot)]
        return ax

    def plot_candlestick(self, data: pd.DataFrame(), candle_body_width: float = VisConfig.default_body_size
                         , candle_wick_width: float = VisConfig.default_wick_size, color_up=VisConfig.default_up_color
                         , color_down=VisConfig.default_down_color):
        """
        Plots candle sticks

        :param data: pandas dataframe of price data
        :type data: Dataframe

        :param candle_body_width: width of the body of the candle
        :type candle_body_width: float

        :param candle_wick_width: width of the wick of the candle
        :type candle_wick_width: float

        :param color_up: color of positive candles
        :type color_up: str

        :param color_down: color of negative candles
        :type color_down: str

        """
        up = data[data["close"] >= data["open"]]
        down = data[data["close"] < data["open"]]

        print(len(up))
        print(len(down))

        self.main.bar(up.index, up["close"] - up["open"], candle_body_width, bottom=up["open"], color=color_up)
        self.main.bar(up.index, up["high"] - up["close"], candle_wick_width, bottom=up["close"], color=color_up)
        self.main.bar(up.index, up["low"] - up["open"], candle_wick_width, bottom=up["open"], color=color_up)

        self.main.bar(down.index, down["close"] - down["open"], candle_body_width, bottom=down["open"],
                      color=color_down)
        self.main.bar(down.index, down["high"] - down["open"], candle_wick_width, bottom=down["open"], color=color_down)
        self.main.bar(down.index, down["low"] - down["close"], candle_wick_width, bottom=down["close"],
                      color=color_down)

    def draw_line(self, x1: float, x2: float, y1: float, y2: float, subplot: str = "main",
                  color=VisConfig.default_line_color
                  , width: float = VisConfig.default_line_width, marker: str = VisConfig.default_line_marker):
        """
        Draws a line on a plot given two point coordinates.

        :param x1: x of first point
        :type x1: float

        :param x2: x of second point
        :type x2: float

        :param y1: y of first point
        :type y1: float

        :param y2: y of second point
        :type y2: float

        :param subplot: name of index of subplot
        :type subplot: str

        :param color: color of the line
        :type color: str

        :param width: width of the line
        :type width: float

        :param marker: marker marking points of the line
        :type marker: str

        """
        ax = self._get_plot(subplot)
        ax.plot([x1, x2], [y1, y2], marker=marker, color=color, linewidth=width)

    def draw_hline(self, y: float, subplot: str = "main", color=VisConfig.default_line_color,
                   width: float = VisConfig.default_line_width):
        """
        Draws a horizontal line across plot.

        :param y: y of the line
        :type y: float

        :param subplot: name or index of subplot
        :type subplot: str

        :param color: color of line
        :type color: str

        :param width: width of the line
        :type width: float

        """
        ax = self._get_plot(subplot)
        xmin, xmax = ax.get_xlim()
        ax.hlines(y, color=color, linewidth=width, xmin=xmin, xmax=xmax)

    def draw_vline(self, x: float, subplot: str = "main", color=VisConfig.default_line_color,
                   width: float = VisConfig.default_line_width):
        """
        Draws a vertical line across plot.

        :param x: x of the line
        :type x: float

        :param subplot: name or index of subplot
        :type subplot: str

        :param color: color of line
        :type color: str

        :param width: width of the line
        :type width: float

        """
        ax = self._get_plot(subplot)
        ymin, ymax = ax.get_ylim()
        ax.vlines(x, color=color, linewidth=width, ymin=ymin, ymax=ymax)

    def plot(self, data: pd.Series, subplot: str = "main", color=VisConfig.default_plot_color
             , width=VisConfig.default_plot_width, marker=VisConfig.default_line_marker):
        """
        Plots a data line on the specified.

        :param data: data of the plot
        :type data: Series

        :param subplot: name or index of subplot
        :type subplot: str

        :param color: color of data line
        :type color: str

        :param width: width of data line
        :type width: float

        :param marker: marker of data line
        :type marker: str
        """
        ax = self._get_plot(subplot)
        ax.plot(data, color=color, linewidth=width, marker=marker)

    def draw_label(self, text: str, width: float, height: float, x: float, y: float, subplot: str = "main"
                   , background_color=VisConfig.default_label_color
                   , text_color=VisConfig.default_label_text_color):
        """
        Draws a rectangle label on specified subplot
        :param text: text of label
        :type text: str

        :param width: width of label
        :type width: float

        :param height: height of label
        :type height: float

        :param x: x position of label
        :type x: float

        :param y: y position of label
        :type y: float

        :param subplot: name or index of subplot
        :type subplot: str

        :param background_color: color of label background
        :type background_color: str

        :param text_color: color of label text
        """
        ax = self._get_plot(subplot)
        # noinspection PyTypeChecker
        # since rectangle position is lower left, we reduce these values to make position center of label
        rect = patches.FancyBboxPatch((x - width / 2, y - height / 2), width, height, facecolor=background_color)
        ax.add_patch(rect)
        ax.annotate(text, (x, y), color=text_color, fontsize=VisConfig.text_fontsize, va='center', ha='center')

    def fill(self, line_1: pd.Series, line_2: pd.Series, subplot="main", fill_color='green', fill_alpha=0.3):
        """
        Fills area between the two lines
        :param line_1: the higher line
        :type line_1: Series:

        :param line_2: the lower line
        :type line_2: Series:

        :param subplot: name or index of subplot
        :type subplot: str

        :param fill_color: color of area
        :param fill_alpha: alpha of area
        """
        ax = self._get_plot(subplot)
        ax.fill_between(line_1.index, line_1, line_2, color=fill_color, alpha=fill_alpha)

    @staticmethod
    def buffer():
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    @staticmethod
    def show():
        plt.show()
