from plotter import Plotter
import yfinance as yf
import pandas as pd

# getting data
start_date = '2023-3-20'
end_date = '2023-4-20'
ticker = "TSLA"
df: pd.DataFrame = yf.download(ticker, start_date, end_date, interval="1h")
df.reset_index(inplace=True)
df.columns = map(str.lower, df.columns)

# initiating plotter
plotter = Plotter(secondaries_num=3, secondaries_titles=["Rsi", "Macd", "Stoch"])

# plot candlesticks
plotter.plot_candlestick(df)

# plot a custom line
plotter.draw_line(0, 50, 180, 200)

# plot horizontal and vertical lines
plotter.draw_hline(180)
plotter.draw_vline(50)

# plotting lines
plotter.plot(df["close"], subplot="0")
plotter.plot(df["low"], subplot="1", color="yellow")
plotter.plot(-df["open"], subplot="2", color="white")

# fill area
plotter.fill(df["high"], df["low"])
plotter.plot(df["high"], color="green")
plotter.plot(df["low"], color="green")

# draw a label
plotter.draw_label("hi", 4, 4, 100, 180)

# show label
plotter.show()