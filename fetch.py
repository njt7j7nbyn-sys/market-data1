import yfinance as yf
import pandas as pd
from datetime import date

tickers = {
    "USD_INR": "USDINR=X", "GBP_USD": "GBPUSD=X", "EUR_USD": "EURUSD=X",
    "USD_CAD": "USDCAD=X", "USD_SGD": "USDSGD=X", "USD_MYR": "USDMYR=X",
    "USD_THB": "USDTHB=X", "USD_VND": "USDVND=X",
    "SENSEX": "^BSESN", "DOW_JONES": "^DJI", "BRENT": "BZ=F",
}

row = {"date": date.today().isoformat()}
for name, t in tickers.items():
    row[name] = round(yf.Ticker(t).history(period="5d")["Close"].dropna().iloc[-1], 4)

# FRED needs no API key for CSV downloads
payems = pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS")
row["NFP_LEVEL_K"] = payems.iloc[-1, 1]
row["NFP_CHANGE_K"] = round(payems.iloc[-1, 1] - payems.iloc[-2, 1], 1)
sofr = pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR")
row["MONEY_MARKET_SOFR"] = sofr.dropna().iloc[-1, 1]

try:
    df = pd.read_csv("data.csv")
    df = df[df["date"] != row["date"]]
    df = pd.concat([df, pd.DataFrame([row])])
except FileNotFoundError:
    df = pd.DataFrame([row])
df.to_csv("data.csv", index=False)
