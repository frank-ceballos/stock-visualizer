import pandas as pd

# To grab stock data
import yfinance as fyf
from pandas_datareader import data as pdr
fyf.pdr_override() # <-- Here is the fix

# To create datetime objects 
import datetime
from datetime import date, timedelta


def get_ticker_data(ticker):
    """ 
    Get financial data for specified ticker starting from 2000 to present date.

    ticker: str
        Ticker label
    """

    # Yahoo Finance
    # Set start and end dates
    start = datetime.datetime(2000, 1, 1)
    end   = date.today()
    
    # Grab data
    data = pdr.get_data_yahoo(ticker, start = start, end = end)
    
    # Decompose data
    values = data.values
    dates = data.index
    
    # Get columns labels
    columns = data.columns.tolist()
    
    # Put dataframe
    df = pd.DataFrame(values, columns = columns, index = dates)
    
    # Return
    return df