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

       
