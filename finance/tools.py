import numpy as np
import pandas as pd
import requests

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

def get_nasdaq_data():
    """
    Grabs NASDAQ data and dumps into a csv. 
    
    This was taken from a comment in GitHub and written by Possum. All the
    credit goes to you bud.
                
    Parameters
    ----------
    
    None
        
    Example
    -------
    
    
    Attributes
    ----------
    
    None
    
    Author Information
    ------------------
    
    Frank Ceballos:
    LinkedIn: <https://www.linkedin.com/in/frank-ceballos/>

    Emil Tu
    GitHub: <https://github.com/Possums>
    """



    headers = {
        'authority': 'api.nasdaq.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'origin': 'https://www.nasdaq.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.nasdaq.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('tableonly', 'true'),
        ('limit', '25'),
        ('offset', '0'),
        ('download', 'true'),
    )

    r = requests.get('https://api.nasdaq.com/api/screener/stocks', 
    headers=headers, params=params)
    data = r.json()['data']
    df = pd.DataFrame(data['rows'], columns=data['headers'])
    df.to_csv('data/nasdaq_info.csv')

    print('NASDAQ data retrieved.')


def get_SMA(close_data, time_period):
    """Computes simple moving average (SMA) for the specified time_period.
    
    Parameters
    ----------
    
    close_data: Pandas Series
        Pandas Series object containing the close data (1-dimensional)
        
    time_period : int
        Number of days to consider for the SMA
    
    Returns
    ----------
    SMA: Pandas Series
        Pandas Series object that contains the simple moving average for the
        close_data.
        
    
    Example
    -------
   To compute a 10-day SMA for the close_data:
           
    # Compute 10-day SMA
    SMA10 = get_SMA(close_data, 10)
        
    Author Information
    ------------------
    Frank Ceballos
    LinkedIn: <https://www.linkedin.com/in/frank-ceballos/>
    
    Date: August, 31, 2019
    """
        
    # List to store moving average results
    SMA = list(range(0, len(close_data) - time_period))
    
    # Compute moving average
    for ii in range(len(SMA)):
        # Previous days index
        index = range(ii, ii + time_period)
        
        # Get data for previous days
        prev_days = close_data.iloc[index]
        
        # Sum previous days
        summation = np.sum(prev_days)
        
        # Get average
        avg = summation/time_period
        
        # Save results to list
        SMA[ii] = avg
         
    # Define column label
    label = f"{time_period}-SMA"
    
    # Get corresponding dates for moving_avg
    dates = close_data.index[time_period:]
    
    # Convert list into Pandas Series
    SMA = pd.Series(SMA, name = label, index = dates)
    
    return SMA


def get_EMA(close_data, time_period):
    """Computes exponential moving average (EMA) for the specified time_period.
    
    Parameters
    ----------
    
    close_data: Pandas Series
        Pandas Series object containing the close data (1-dimensional)
        
    time_period : int
        Number of days to consider for the SMA
    
    Returns
    ----------
    EMA: Pandas Series
        Pandas Series object that contains the exponential moving average for the
        close_data.
        
    
    Example
    -------
   To compute a 10-day EMA for the close_data:
           
    # Compute 10-day EMA
    EMA10 = get_EMA(close_data, 10)
        
    Author Information
    ------------------
    Frank Ceballos
    LinkedIn: <https://www.linkedin.com/in/frank-ceballos/>
    
    Date: August, 31, 2019
    """
    
    # List to store moving average results
    EMA = list(range(0, len(close_data) - time_period))
    
    # Calculate SMA to use as the first EMA
    initial_EMA = get_SMA(close_data, time_period)[0]
    
    # Calculate initial weight
    k = 2.0 / (time_period + 1)

    # Compute EMA
    for ii in range(len(EMA)):
        # Set index
        index = time_period + ii
        
        # Get current Close price
        close_temp = close_data[index]
        
        # Compute current EMA
        if ii == 0:
            EMA_temp = (close_temp - initial_EMA)*k + initial_EMA
        else:
            EMA_temp = (close_temp - EMA[ii-1])*k + EMA[ii-1]


        # Save results to list
        EMA[ii] = EMA_temp
        
    # Define column label
    label = f"{time_period}-EMA"
    
    # Get corresponding dates for moving_avg
    dates = close_data.index[time_period:]
    
    # Convert list into Pandas Series
    EMA = pd.Series(EMA, name = label, index = dates)
    
    return EMA
