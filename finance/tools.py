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
