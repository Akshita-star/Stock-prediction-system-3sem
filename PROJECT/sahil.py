 
if final_symbol:
    data = load_data(final_symbol)

    if not data.empty:
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

        #(5)------daily returns-------
        recent_data['Daily Return %'] = recent_data['Close'].pct_change() * 100
        st.subheader(f"{final_symbol} Daily Returns (%) ({period_label})")
        plt.figure(figsize=(12,5))
        plt.plot(recent_data['Date'], recent_data['Daily Return %'], color='purple')
        plt.title(f"{final_symbol} Daily Returns (%)")
        plt.xlabel("Date")
        plt.ylabel("Daily Return %")
        plt.grid(True)
        st.pyplot(plt)

        








