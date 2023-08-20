import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import numpy as np

link = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies").text

soup = BeautifulSoup(link, "html.parser")

data_SP = []    # creation of list allow us to gather 
                # all of symbol or code in order to easier our work

# Using BeautifulSoup we are going to parse 
# a wiki website to retrieve all S&P 500 stock Symbols 

tbody_list = soup.find("tbody")

for tr in tbody_list.find_all("tr"):
    cols = tr.find_all("td")
    
    row_data = [col.text.strip() for col in cols]
    data_SP.append(row_data)
    
df_old = pd.DataFrame(data_SP, columns=["Symbol", "Name", "Sector", "Sub_Industry", "HeadQuaters", "Date Added", "CIK", "Founded"])
columns_remove = ["CIK", "Founded"]

df = df_old.drop(columns=columns_remove)
df = df.dropna()

latest_date = df["Date Added"].max()

bfx = yf.Ticker("^BFX")
bel_20 = bfx.history(start=latest_date)
bel = pd.DataFrame(bel_20)
bel["diff %"] = ((bel["Close"] - bel["Open"])/ bel["Open"]) * 100

BEL20 = bel["diff %"].values
print(bel.keys)


correlations = []

for sym in df["Symbol"]:
    share = yf.Ticker(sym)
    
    body = share.history(start=latest_date)
    
    df_SP = pd.DataFrame(body)
    
    df_SP["diff %"] = ((df_SP["Close"] - df_SP["Open"]) / df_SP["Open"]) * 100
    
    if first_date == df_SP["Date"]:
        print("ok")
    
    # SHARE = df["diff %"].values
#     correlation_matrix = np.corrcoef(BEL20, SHARE)[0, 1]
#     correlations.append(correlation_matrix)

# print(correlations)
# Using Pandas Lib we will determine the date of entry
# Why ? to start our correlation from this date