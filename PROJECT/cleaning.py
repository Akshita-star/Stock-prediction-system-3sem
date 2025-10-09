import pandas as pd
import yfinance as yf
from datetime import date
import streamlit as st
import matplotlib.pyplot as plt

start = "2012-01-01"
end = date.today()

st.title("📊 StockOracle")
st.write("\n" * 2)

stock_list = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "ITC.NS", "BHARTIARTL.NS", "WIPRO.NS", "HINDUNILVR.NS", "AAPL"
]

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data

# --- Stock selection ---
stock_symbol = st.selectbox(
    "Select Stock Symbol:",
    options=stock_list,
    index=None
)

st.write("\n" * 2)
st.write("🧐 Unable to find your stock? Type manually below 👇")
manual_symbol = st.text_input("Enter Stock Symbol:", placeholder="e.g., RELIANCE.NS, AAPL, etc.")
final_symbol = manual_symbol.strip() if manual_symbol.strip() else stock_symbol
search = st.button("Search")

if search and final_symbol:
    data = load_data(final_symbol)

    if not data.empty:

        # (1) --- STOCK STATISTICS ---
        st.subheader(f"📈 {final_symbol} - Stock Statistics")
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

        # # (2) --- TIME PERIOD CHART ---
        period_options = {"1 Month": 30,
        "6 Months": 182,
        "1 Year": 365,
        "5 Years": 1825,
        "10 Years": 3650
        }

        period_label = st.radio(
        "Select Period for Chart:",
        list(period_options.keys()),
        horizontal=True
        )
    

        days = period_options[period_label]

        # Ensure 'Date' is datetime
        data["Date"] = pd.to_datetime(data["Date"])
        last_date = data["Date"].max()
        start_period = last_date - pd.Timedelta(days=days)

        # Filter data for selected period
        filtered_data = data[data["Date"] >= start_period].copy()

        # Calculate moving averages
        filtered_data["MA50"] = filtered_data["Close"].rolling(window=50).mean()
        filtered_data["MA200"] = filtered_data["Close"].rolling(window=200).mean()

        # Drop rows where Volume is NaN to prevent errors
        filtered_data = filtered_data.dropna(subset=["Volume", "Close"])

        # Convert Series to list for plotting
        dates = filtered_data["Date"]
        close_prices = filtered_data["Close"]
        ma50 = filtered_data["MA50"]
        ma200 = filtered_data["MA200"]
        volumes = filtered_data["Volume"].astype(float)

        # Plotting
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Price & Moving Averages   
        ax1.plot(dates, close_prices, label="Close Price", color="blue")
        ax1.plot(dates, ma50, label="50-day MA", color="orange", linestyle="--")
        ax1.plot(dates, ma200, label="200-day MA", color="green", linestyle="--")
        ax1.set_ylabel("Price (₹)")
        ax1.set_xlabel("Date")
        ax1.legend(loc="upper left")
        ax1.set_title(f"{final_symbol} Price Chart ({period_label})")

        # Volume bars
        ax2 = ax1.twinx()
        ax2.bar(dates, volumes, color="gray", alpha=0.2, label="Volume")
        ax2.set_ylabel("Volume")
        ax2.set_ylim(bottom=0)

        # Improve x-axis formatting
        fig.autofmt_xdate()

        # Show plot in Streamlit
        st.pyplot(fig)

        # (4) --- RAW DATA ---
        st.subheader("📜 Raw Data")
        st.write(filtered_data.tail(20))

    else:
        st.warning(f"No data found for {final_symbol}. Please check ticker spelling or exchange suffix.")
