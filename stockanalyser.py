from graphs import DisplayGraphs

import streamlit as st 
import os
from pathlib import Path
from win32api import GetSystemMetrics


 
mag7 = os.listdir("graphs/figures")
current_dir = Path(__file__).parent
filepath = current_dir / "graphs" / "figures"


st.title("1 Year Stock Performance")

ticker = st.selectbox("Enter Stock Ticker:", mag7, key = 0).upper() #Get the ticker input and capitalise


graph_display = DisplayGraphs.DisplayGraphs(mag7)
graph_display.selected_ticker = ticker

graph_display.displayGraphOnUserSelect()
from_month = st.selectbox("View from(in months)", [ 6 , 3, 1], width = int(GetSystemMetrics(0) *0.05), key = 1)
graph_display.from_month = from_month
graph_display.setViewFromMonth()



