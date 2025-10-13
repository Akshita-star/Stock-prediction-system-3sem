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

# --- MAIN LOGIC ---
if final_symbol:
    data = load_data(final_symbol)

    if not data.empty:
     
    #(1)--- STOCK STATISTICS ---
        st.subheader(f" {final_symbol} - Stock Statistics")
        col1, col2, col3 = st.columns(3)

        latest_row = data.iloc[-1]
        prev_row = data.iloc[-2] if len(data) > 1 else latest_row

        open_price = float(latest_row["Open"])
        close_price = float(latest_row["Close"])
        prev_close = float(prev_row["Close"])

        change = close_price - prev_close
        percent_change = (change / prev_close * 100) if prev_close != 0 else 0

        open_display = f"₹{open_price:,.2f}"
        close_display = f"₹{close_price:,.2f}"
        change_display = f"{'+' if change >= 0 else ''}₹{change:,.2f}"
        percent_display = f"{percent_change:+.2f}%"

        with col1:
            st.metric("Open", open_display, f"{(open_price - prev_close) / prev_close * 100:+.2f}%")
        with col2:
            st.metric("Close", close_display, percent_display)
        with col3:
            st.metric("Change", change_display, percent_display)

        st.write("**PREDICTION ITEMS HERE YET TO COMEE**")


        # --- TIME PERIOD SELECTION ---
        st.subheader("Select Time Period")
        period_options = {
            "1 Month": 30,
            "6 Months": 182,
            "1 Year": 365,
            "5 Years": 1825,
        }
        period_label = st.radio("Period:", list(period_options.keys()), horizontal=True)
        days = period_options[period_label]

        # Filter data by date
        start_date = data['Date'].max() - timedelta(days=days)
        recent_data = data[data['Date'] >= start_date]
        

        #------PREDICTION GRAPH TO COME-------
        st.write("**PREDICTION CHART YET TO COME**")

        # (2)-------MAIN CHART------------
        st.subheader(f" {final_symbol} Price Chart ({period_label})")
        plt.figure(figsize=(12, 5))
        plt.plot(recent_data['Date'], recent_data['Close'], label='Close Price', color='blue')
        plt.plot(recent_data['Date'], recent_data['Open'], label='Open Price', color='orange', alpha=0.7)
        plt.title(f"{final_symbol} Stock Price Over {period_label}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        #(3)------volume-------
        st.subheader(f"{final_symbol} Volume Chart ({period_label})")
        plt.figure(figsize=(12, 5))
        plt.plot(recent_data['Date'], recent_data['Volume'], label='Volume', color='lightgreen')
        plt.title(f"{final_symbol} Trading Volume Over {period_label}")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        #(4)-------Calculate Moving Averages-------
        recent_data['MA10'] = recent_data['Close'].rolling(10).mean()
        recent_data['MA50'] = recent_data['Close'].rolling(50).mean()

        st.subheader(f" {final_symbol} Moving Averages ({period_label})")
        plt.figure(figsize=(12, 5))
        plt.plot(recent_data['Date'], recent_data['Close'], label='Close Price', color='blue')
        plt.plot(recent_data['Date'], recent_data['MA10'], label='MA10 (10-day)', color='orange')
        plt.plot(recent_data['Date'], recent_data['MA50'], label='MA50 (50-day)', color='green')
        plt.title(f"{final_symbol} Close Price with Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        #(5)-------daily high low----
        st.subheader(f"{final_symbol} Daily High-Low Spread ({period_label})")
        plt.figure(figsize=(12, 5))
        plt.plot(recent_data['Date'], recent_data['Close'], label='Close Price', color='blue')
        plt.title(f"{final_symbol} Daily High-Low Spread")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # --- RAW DATA ---
        st.subheader(" Raw Data")
        st.dataframe(data)

        #-----actual versus predicted plot----
        st.write("**ACTUAL VS PREDCITED GRAPH TO COME**")
    else:
        st.warning(f" No valid data found for '{final_symbol}'. Please check ticker spelling or exchange suffix.")










