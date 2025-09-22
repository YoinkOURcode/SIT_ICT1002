from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import streamlit as st 
import yfinance as yf
import matplotlib.pyplot as plt
from git import Repo
 

st.title("5 Day Stock Performance")

end_date = datetime.now() #Finding the end date 
start_date = end_date - timedelta(days=7) #Finding 5 days before
ticker = st.text_input("Enter Stock Ticker:", value='META').upper() #Get the ticker input and capitalise

if ticker:
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=7)
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        
        if stock_data.empty:
            st.warning("No data found!")
        else:
            stock_data = stock_data.tail(5)
            stock_data['SMA'] = stock_data['Close'].rolling(window=5).mean(0)
            st.subheader(f"Last 5 Trading Days: {ticker}")
            st.dataframe(stock_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA']])
            
            fig, ax = plt.subplots()
            stock_data['Close'].plot(kind='line', marker='o', ax=ax)
            ax.set_title(f"{ticker} - Closing Price (Last 5 Days)")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.grid(True)

            st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred: {e}")