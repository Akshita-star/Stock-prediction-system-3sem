import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# --- CONFIG ---
start = "2012-01-01"
end = date.today()

st.set_page_config(page_title="StockOracle", layout="wide")
st.title("📊 StockOracle")
st.write("\n" * 2)

# --- STOCK OPTIONS ---
stock_list = [
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS", "BANKBARODA.NS", "PNB.NS", "INDUSINDBK.NS", "IDFCFIRSTB.NS",
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS", "LT.NS", "ULTRACEMCO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS",
    "ADANIENT.NS", "ADANIPORTS.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "COALINDIA.NS", "NTPC.NS", "POWERGRID.NS", "ONGC.NS", "IOC.NS", "BPCL.NS",
    "ASIANPAINT.NS", "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS", "MARUTI.NS", "TATAMOTORS.NS", "EICHERMOT.NS", "HEROMOTOCO.NS",
    "BAJAJ-AUTO.NS", "SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS", "APOLLOHOSP.NS", "M&M.NS", "DMART.NS", "GRASIM.NS", "HAVELLS.NS",
    "BERGEPAINT.NS", "PIDILITIND.NS", "DABUR.NS", "GODREJCP.NS", "TITAN.NS", "INDIGO.NS", "ZOMATO.NS", "PAYTM.NS", "NYKAA.NS", "DELHIVERY.NS",
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "NFLX", "INTC", "AMD","JPM", "GS", "BAC", "C", "MS","BABA", "SONY", "NKE", "DIS", "PEP", "KO", "MCD", "PFE", "V", "MA"
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
        st.subheader(f"{final_symbol} - Stock Statistics")
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

        # ==============================
        # (2) 📈 PREDICTION SECTION + GRAPH
        # ==============================
        st.subheader("📊 Stock Movement Probability Prediction")

        # --- Feature Engineering ---
        data['Return'] = data['Close'].pct_change()
        data['MA5'] = data['Close'].rolling(5).mean()
        data['MA10'] = data['Close'].rolling(10).mean()
        data['MA20'] = data['Close'].rolling(20).mean()
        data['Volatility'] = data['Return'].rolling(10).std()
        data['Open_Close_Change'] = (data['Close'] - data['Open']) / data['Open']
        data['Volume_Change'] = data['Volume'].pct_change()

        # ✅ Replace inf/-inf with NaN
        data.replace([np.inf, -np.inf], np.nan, inplace=True)

        # ✅ Drop rows with NaN after all features are ready
        data.dropna(inplace=True)

        # --- Target Variable ---
        data['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

        # --- Features and Target ---
        features = ['Return', 'MA5', 'MA10', 'MA20', 'Volatility', 'Open_Close_Change', 'Volume_Change']
        X = data[features]
        y = data['Target']

        # ✅ Ensure X has only finite values
        X = X.replace([np.inf, -np.inf], np.nan).dropna()
        y = y.loc[X.index]

        # --- Split Train/Test ---
        train_size = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
        y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

        # --- Model Training ---
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # --- Predict probability for each test date ---
        data.loc[X_test.index, "Predicted_Prob"] = model.predict_proba(X_test)[:, 1] * 100

        # --- Latest Prediction ---
        latest_prob = float(data["Predicted_Prob"].iloc[-1])
        prediction = "📈 Likely to Grow" if latest_prob > 50 else "📉 Likely to Decrease"

        # --- Replace Risk Level with Confidence ---
        confidence_display = f"{latest_prob:.2f}% Confidence"

        # --- Styled Result Box ---
        st.markdown(
        f"""
        <div style="
        background: linear-gradient(135deg, #f9f9f9, #fffbea);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        border: 3px solid #ffd54f;
        box-shadow: 0px 3px 15px rgba(0,0,0,0.15);
        margin-bottom: 25px;">
        <h2 style="color:#ff9800; font-weight:700; font-size:28px;">{prediction}</h2>
        <p style="font-size:22px; color:#333;">📊 Probability of Growth: 
            <b style="color:#00796b;">{confidence_display}</b>
        </p>
        <hr style="border:1px solid #ccc; width:80%;">
        <p style="font-size:18px; color:#555;">Model Used: 
            <b>Random Forest Classifier</b> (trained on past 80% data)
        </p>
        </div>
        """,
        unsafe_allow_html=True)


        # --- Predicted Probability Graph (Simulated Future Trend) ---
        st.subheader("Predicted Probability Graph (Next 7 Days Simulation)")

        # Generate simulated probability trend
        future_days = 20
        latest_prob = float(data["Predicted_Prob"].iloc[-1])

        # Random walk around latest probability
        sim_prob = [latest_prob]
        for _ in range(future_days-1):
            change = np.random.uniform(-5, 5)  # simulate realistic daily change
            next_prob = np.clip(sim_prob[-1] + change, 0, 100)  # keep within 0-100%
            sim_prob.append(next_prob)

        # Plot the simulated trend
        plt.figure(figsize=(12, 5))
        plt.plot(range(1, future_days+1), sim_prob, color='teal', marker='o', linewidth=2)
        plt.title(f"{final_symbol} - Simulated Future Up/Down Probability (%)")
        plt.xlabel("Future Days")
        plt.ylabel("Probability (%)")
        plt.xticks(range(1, future_days+1))
        plt.ylim(0, 100)
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)


        # ==============================
        # (3) Select Time Period
        # ==============================
        st.subheader("Select Time Period")
        period_options = {
                "1 Month": 30,
                "6 Months": 182,
                "1 Year": 365,
                "5 Years": 1825,
            }
        period_label = st.radio("Period:", list(period_options.keys()), horizontal=True)
        days = period_options[period_label]

        start_date = data['Date'].max() - timedelta(days=days)
        recent_data = data[data['Date'] >= start_date]

        # ==============================
        # (4) Price Chart
        # ==============================
        st.subheader(f"{final_symbol} Price Chart ({period_label})")
        plt.figure(figsize=(12, 5))
        plt.plot(recent_data['Date'], recent_data['Close'], label='Close Price', color='blue')
        plt.plot(recent_data['Date'], recent_data['Open'], label='Open Price', color='orange', alpha=0.7)
        plt.title(f"{final_symbol} Stock Price Over {period_label}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # ==============================
        # (5) Volume Chart
        # ==============================
        st.subheader(f"{final_symbol} Volume Chart ({period_label})")
        plt.figure(figsize=(12, 5))
        plt.plot(recent_data['Date'], recent_data['Volume'], label='Volume', color='lightgreen')
        plt.title(f"{final_symbol} Trading Volume Over {period_label}")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # ==============================
        # (6) Moving Averages
        # ==============================
        recent_data['MA10'] = recent_data['Close'].rolling(10).mean()
        recent_data['MA50'] = recent_data['Close'].rolling(50).mean()

        st.subheader(f"{final_symbol} Moving Averages ({period_label})")
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

        # ==============================
        # (7) Daily Returns
        # ==============================
        recent_data['Daily Return %'] = recent_data['Close'].pct_change() * 100
        st.subheader(f"{final_symbol} Daily Returns (%) ({period_label})")
        plt.figure(figsize=(12, 5))
        plt.plot(recent_data['Date'], recent_data['Daily Return %'], color='purple')
        plt.title(f"{final_symbol} Daily Returns (%)")
        plt.xlabel("Date")
        plt.ylabel("Daily Return %")
        plt.grid(True)
        st.pyplot(plt)

        # ==============================
        # (8) Compare Stocks
        # ==============================
        st.write("\n" * 3)
        compare_option = st.checkbox("Compare with another stock?")
        if compare_option:
            compare_symbol = st.text_input("Enter stock symbol to compare:", placeholder="e.g., TCS.NS")
            if compare_symbol.strip():
                compare_data = load_data(compare_symbol.strip())
                if not compare_data.empty:
                    compare_recent = compare_data[compare_data['Date'] >= data['Date'].max() - timedelta(days=days)].copy()
                    compare_recent['Daily Return %'] = compare_recent['Close'].pct_change() * 100

                    st.subheader(f"Daily Returns Comparison ({final_symbol} vs {compare_symbol.strip()})")
                    plt.figure(figsize=(12, 5))
                    plt.plot(recent_data['Date'], recent_data['Daily Return %'], label=final_symbol, color='purple')
                    plt.plot(compare_recent['Date'], compare_recent['Daily Return %'], label=compare_symbol.strip(), color='orange')
                    plt.title("Daily Returns Comparison")
                    plt.xlabel("Date")
                    plt.ylabel("Daily Return %")
                    plt.legend()
                    plt.grid(True)
                    st.pyplot(plt)
                else:
                    st.warning(f" No valid data found for '{compare_symbol.strip()}'.")

        # ==============================
        # (9) Raw Data
        # ==============================
        st.subheader("Raw Data")
        st.dataframe(data)

    else:
        st.warning(f" No valid data found for '{final_symbol}'. Please check ticker spelling or exchange suffix.") 
