import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import numpy as np

# We are going to import some Libs to realise our project, however it does possible 
# that some Libs wouldn't use these!!!

link = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies").text

soup = BeautifulSoup(link, "html.parser")    # We will import S&P symbol as well as name code

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

# Here, We have created our table in "df" variable with many informations regardings the symbol,
# Name, Sector and so on. We have put the rest of information of table to create the real impact 
# of correlation

latest_date = df["Date Added"].max()

# It's crucial to know the most recent date to achieve our correlation with a start date.

bfx = yf.Ticker("^BFX")
bel_20 = bfx.history(start=latest_date)
bel = pd.DataFrame(bel_20)


bel_date = [str(date)[:10] for date in bel.index]

bel["diff %"] = ((bel["Close"] - bel["Open"])/ bel["Open"]) * 100

bel.index = bel.index.strftime("%Y-%m-%d")
# We have a BEL 20 Market Index as refference. It length measures 47 --> Relevant information
# that goes reduce possible problem for following step!!!
# Moreover, we will change the date format in order to remove the time zone
# to be able to compare the dates between them

correlations = []


for sym in df["Symbol"]:
    
    print(sym)
    
    share = yf.Ticker(sym)
    interval = share.history(start=latest_date)

    share_one = []
    belgique = []
    
    if not interval.empty:

        df_SP = pd.DataFrame(interval)
        df_SP["diff %"] = ((df_SP["Close"] - df_SP["Open"]) / df_SP["Open"]) * 100

        df_SP.index = df_SP.index.strftime("%Y-%m-%d")
        
        for date_bfx in bel.index:
            for date_sp in df_SP.index:
                if date_bfx == date_sp:
                    shares = df_SP.loc[date_sp, "diff %"]
                    bele = bel.loc[date_bfx, "diff %"]
                    
                    share_one.append(shares)
                    belgique.append(bele)
                    
                    
                    
        correlation_matrix = np.corrcoef(belgique, share_one)[0, 1]
        if -0.3 < correlation_matrix > 0.3:
            print(f"{sym} est corréler à {correlation_matrix}")
