import pickle
from pathlib import Path
import streamlit as st 
import os
import sys
sys.path.append(str(Path(__file__).parent))
from utils.finance_utils import maxProfit

class DisplayGraphs:
    def __init__(self, tickers_to_use: list):
        """
        The purpose of this class is to handle the displaying of our graphs created from graph.ipynb into the streamlit web app
        Attributes:
            tickers_to_use (list): List of stock tickers we are using to display(in this project we are using the mag7).
            selected_ticker (str): Currently selected ticker to display, default value is the first value from tickers_to_use so we have something to display
            from_month (int): Currently selected number of months to view from for the data, default is 12, because that is the furthest we have. This is to ensure that users can view recent data more closely
            __figures (dict): Dictionary mapping tickers to their loaded matplotlib figures.
        """
        self.__figures = {}
        self.tickers_to_use = tickers_to_use
        self.selected_ticker = tickers_to_use[0]
        self.from_month = 12

        try:
            for stock in self.tickers_to_use:
                #Reading all the figures that we have created in graph.ipynb and storing it inside the figures list
                with open(Path(__file__).parent /  "figures" / stock, "rb") as f:
                    fig = pickle.load(f)
                    self.__figures[stock] = fig
        except AttributeError:
            print("tickers_to_use cannot be undefined!")
        except FileNotFoundError:
            print(f"Figure file for {stock} not found in 'figures' folder.")
        except pickle.UnpicklingError:
            print(f"Failed to load figure for {stock}.")
        
            
    def displayGraphOnUserSelect(self):
        """
        Displays the graph for the currently selected ticker in the Streamlit app.
        Shows a selectbox for viewing trends over different time ranges (12, 6, 1 month).
        """
        if self.selected_ticker:
            st.subheader(f"Trends from  {self.selected_ticker}")
            st.markdown("Predictions are reflected as dotted lines")
            st.pyplot(self.__figures[self.selected_ticker])
        else:
            st.write("Ticker not found")
    
    def setViewFromMonth(self):
        try:
            if self.from_month > 0 and type(self.from_month) == int:
                ax = self.__figures[self.selected_ticker].axes[0] # Get the first Axes object
                st.subheader(f"Showing from {self.from_month} months ago")
                ax.set_xlim(ax.lines[0].get_xdata()[20 * self.from_month * -1],  ax.lines[0].get_xdata()[-1]) # Set x-axis limits to show last 'from_month' months
                st.pyplot(self.__figures[self.selected_ticker])
            else:
                st.write("Invalid month input!")
        except KeyError:
            st.write("Ticker not found")
        except IndexError:
            st.write("Not enough data to display for the selected month range")
        

    def displayDailyReturns(self):
        """
        Displays the daily returns graph for the currently selected ticker in the Streamlit app.
        """
        try:
            if self.selected_ticker:
                st.subheader(f"Daily Returns of {self.selected_ticker}")
                st.pyplot(self.__figures[self.selected_ticker + "_Daily_Return_Distribution"])
            else:
                st.write("Ticker not found")
        except KeyError:
            st.write("Daily returns figure not found for the selected ticker")
        except Exception as e:
            st.write(f"An error occurred: {e}")
    
    def calculateMaxProfit(self, moving_average_window):
        """
        Calculates the maximum profit that could be achieved from a list of stock prices.
        This function assumes you can buy and sell the stock multiple times to maximize profit.
        
        Args:
            prices (list): A list of stock prices where each price represents the stock price on a given day.
        Returns:
            int: The maximum profit that could be achieved.
        """
        if moving_average_window not in [30, 90, 180]:
            raise ValueError("moving_average_window must be one of the following values: 30, 90, 180")
        
        ax = self.__figures[self.selected_ticker].axes[0] # Get the first Axes object
        lines_by_name = {line.get_label(): line for line in ax.get_lines()}
        line = lines_by_name.get(f"Predicted using {moving_average_window} days")
        prices = line.get_ydata() if line else []
        maxProfitPrice = maxProfit(prices)
        try:
            maxProfitPrice = maxProfitPrice.round(2)
        except AttributeError: # in case maxProfitPrice is an int
            maxProfitPrice = maxProfitPrice

        return maxProfitPrice
        
