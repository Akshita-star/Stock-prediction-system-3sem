import streamlit as st
import yfinance as yf

st.title("StackOracle")
st.write("\n"*2)

# Rename 'list' to 'stock_list'
stock_list = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "ITC.NS", "BHARTIARTL.NS", "WIPRO.NS", "HINDUNILVR.NS","JIO","ICC"
]

# Stock selection
stock_symbol = st.selectbox(
    "Enter or Select Stock Symbol:",
    options=stock_list,
    index=None,
    placeholder="Type or choose stock..."
)
search = st.button("Search")

if stock_symbol and search:
    st.success(f"You selected: **{stock_symbol}**")

    # --- Placeholder for statistics ---
    st.subheader("Stock Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open", "₹2,000", "+1.2%", delta_color="normal")  # All this data will be fetched using yfinance
    with col2:
        st.metric("Close", "₹2,050", "+2.5%", delta_color="normal")
    with col3:
        st.metric("Change", "+₹50", "+2.5%", delta_color="inverse")

    # Time period selection
    period_options = {
    "1 Month": "1mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "10 Years": "10y"
    }
    period_choice = st.radio(
    "Select Time Period:",
    options=list(period_options.keys()),  # convert dict keys to list
    horizontal=True)
    st.subheader(f"{stock_symbol} Price Chart ({period_choice})")
    st.write("CHART TO BE DRAWN ACCOORDING TO TIMESTAMP")
 
    # --- Placeholder for additional plots ---
    st.subheader("Additional Analysis")
    st.write("If any other charts to be drawn, place them below this section")

    #PREDICTION AND ALSO DRAW CHART FOR ACTUAL AND PREDICTION BBY THIS

    # --- Compare with another stock ---
    compare_symbol = st.selectbox(
    "Compare with another stock:",
    options=stock_list,
    index=None,
    placeholder="Type or choose stock..."
    )
    st.write("Compare with another plot")

    st.subheader("Profit/Losses")
    st.write("Profit/Loss chart type")

    # --- Raw data at end ---
    st.subheader("Raw Data")
    st.write("Fetch raw data here using yfinance")
