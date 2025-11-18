#(6)-----COMPARING-----
    if final_symbol:
    data = load_data(final_symbol)

        if not data.empty:   
        st.write("\n"*3)
        compare_option = st.checkbox("Compare with another stock?")

        if compare_option:
            compare_symbol = st.text_input("Enter stock symbol to compare:", placeholder="e.g., TCS.NS")
    
            if compare_symbol.strip():
                compare_data = load_data(compare_symbol.strip())
        
                if not compare_data.empty:
                    # Filter by the same period as main stock
                    compare_recent = compare_data[compare_data['Date'] >= data['Date'].max() - timedelta(days=days)].copy()
            
                    # Calculate daily returns
                    compare_recent['Daily Return %'] = compare_recent['Close'].pct_change() * 100
            
                    # Plot comparison
                    st.subheader(f"Daily Returns Comparison ({final_symbol} vs {compare_symbol.strip()})")
                    plt.figure(figsize=(12,5))
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



        # --- RAW DATA ---
        st.subheader(" Raw Data")
        st.dataframe(data)

        #-----actual versus predicted plot----
        st.write("**ACTUAL VS PREDCITED GRAPH TO COME**")
    else:
        st.warning(f" No valid data found for '{final_symbol}'. Please check ticker spelling or exchange suffix.")

        

