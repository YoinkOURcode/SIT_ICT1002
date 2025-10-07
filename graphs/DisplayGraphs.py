import pickle
from pathlib import Path
import streamlit as st 


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
            st.pyplot(self.__figures[self.selected_ticker])
        else:
            st.write("Ticker not found")
    
    def setViewFromMonth(self):
        if self.from_month > 0 and type(self.from_month) == int:
            ax = self.__figures[self.selected_ticker].axes[0] 
            st.subheader(f"Showing from {self.from_month} months ago")
            ax.set_xlim(ax.lines[0].get_xdata()[20 * self.from_month * -1],  ax.lines[0].get_xdata()[-1])
            st.pyplot(self.__figures[self.selected_ticker])
        else:
            st.write("Invalid month input!")


            





    

    
                




    # ax.set_xlim(ax.lines[0].get_xdata()[12 * 5 * -1],  ax.lines[0].get_xdata()[-1])

