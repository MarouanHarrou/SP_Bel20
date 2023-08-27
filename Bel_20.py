
import yfinance as yf
import pandas as pd


bfx = yf.Ticker("^BFX")
bel_20 = bfx.history(period="1y")
bel = pd.DataFrame(bel_20)
bel["date"] = bel.index.strftime("%Y-%m-%d")



# bel["diff %"] = ((bel["Close"] - bel["Open"])/ bel["Open"]) * 100


print(bel)