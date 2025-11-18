import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import streamlit as st
import matplotlib.pyplot as plt

# --- CONFIG ---
start = "2012-01-01"
end = date.today()

st.set_page_config(page_title="StockOracle", layout="wide")
st.title("📊 StockOracle")
st.write("\n" * 2)


# --- STOCK OPTIONS ---
stock_list = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "ITC.NS", "BHARTIARTL.NS", "WIPRO.NS", "HINDUNILVR.NS", "AAPL"
]

@st.cache_data
def load_data(ticker):
    """Fetch and cache stock data"""
    try:
        data = yf.download(ticker, start, end)
        data.reset_index(inplace=True)
        return data
    except Exception:
        return pd.DataFrame()

# --- STOCK INPUT ---
stock_symbol = st.selectbox(
    "Select Stock Symbol:",
    options=[" "] + stock_list,
    index=0,
    format_func=lambda x: x if x else " "
)
st.write("💡 Or type manually below:")
manual_symbol = st.text_input("Enter Stock Symbol:", placeholder="e.g., RELIANCE.NS, AAPL, etc.")
final_symbol = manual_symbol.strip() if manual_symbol.strip() else stock_symbol.strip()

