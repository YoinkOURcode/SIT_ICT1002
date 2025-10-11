from graphs import DisplayGraphs

import streamlit as st 
import os
from pathlib import Path
from win32api import GetSystemMetrics


 
mag7_figs = os.listdir("graphs/figures") #Get all the stock tickers that we have figures for
mag7_options = [fig for fig in mag7_figs if not fig.endswith("_Daily_Return_Distribution")] #Filter out the daily return distribution graphs
current_dir = Path(__file__).parent
filepath = current_dir / "graphs" / "figures"


st.title("1 Year Stock Performance")

ticker = st.selectbox("Enter Stock Ticker:", mag7_options, key = 0).upper() #Get the ticker input and capitalise



graph_display = DisplayGraphs.DisplayGraphs(mag7_figs)

graph_display.selected_ticker = ticker
col1, col2, col3 = st.columns(3)
col1.metric("Max profit using SMA 30",graph_display.calculateMaxProfit(30))
col2.metric("Max profit using SMA 90", graph_display.calculateMaxProfit(90))
col3.metric("Max profit using SMA 180", graph_display.calculateMaxProfit(180))
st.write("Max profit is calculated by summing all positive price differences on prices predicted using SMA, assuming multiple buy-sell transactions.")
graph_display.displayGraphOnUserSelect()


from_month = st.selectbox("View from(in months)", [ 6 , 3, 1], width = int(GetSystemMetrics(0) *0.05), key = 1)
graph_display.from_month = from_month
graph_display.setViewFromMonth()

graph_display.displayDailyReturns()



