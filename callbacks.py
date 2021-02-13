import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output

from app import app

# For styles
from assets.Styles import DashComponentStyles

from datetime import date, timedelta

from finance.tools import get_ticker_data

# My Finace Tools
from finance.tools import get_SMA, get_EMA

###############################################################################
#                             1. Web App Styling                              #
###############################################################################
# Get colors
colors = DashComponentStyles().colors

@app.callback(Output('Close-Line-Graph', 'figure'),
              [Input('Ticker-Picker', 'value'),
              Input('MovAvg-Picker', 'value')])
def updateCloseLineGraph(ticker, moving_averages):
    if ticker == None:
        ticker = 'GOOG'

    # Get data
    data = get_ticker_data(ticker)
        
    # Create trace
    candlestick_trace = go.Candlestick(
                            x = data.index,
                            open = data['Open'],          
                            high  = data["High"],
                            low   = data["Low"],
                            close = data["Close"],
                            name = ticker,
                            increasing = dict(fillcolor = colors['bullish'], line = dict(color = colors['bullish'])),
                            decreasing = dict(fillcolor = colors['bearish'], line = dict(color = colors['bearish'])),
                            whiskerwidth = 0.05,
                            line = dict(width = 1),
                            hoverlabel = dict(bgcolor = colors['hoverBackground'],
                                              font = dict(family='Courier New, monospace', size=8, color = colors['text']),
                                              bordercolor = colors['hoverBorder']),
                            )

    # Add moving averages
    close_data = data['Close']
    ma_traces = get_moving_average(moving_averages, close_data)

    # Set Volume Chart Colors
    volumeColors = []
    
    for i in range(len(data.Close)):
        if i != 0:
            if data.Close[i] > data.Close[i-1]:
                volumeColors.append(colors['bullish'])
            else:
                volumeColors.append(colors['bearish'])
        else:
            volumeColors.append(colors['bearish'])
    
    # Add Volume Chart
    trace_volume = go.Bar(x = data.index, y = data.Volume,
                          marker = dict(color = volumeColors),
                          marker_line =  dict(color = volumeColors),
                          yaxis = 'y', name = 'Volume',
                          hoverlabel = dict(font = dict(family='Courier New, monospace', 
                                            size=8,
                                            color = colors['text'])))
    
    # Set x-axis range
    start_date = date.today() - timedelta(days=360)
    end_date = date.today()

    # Get y-axis Candlesticks Chart
    start_price, end_price = get_yrange(start_date, end_date, data, 'Close')

    # Get y-axis Volume Chart
    start_volume, end_volume = get_yrange(start_date, end_date, data, 'Volume')

    # Set layout
    layout = go.Layout(paper_bgcolor = colors['graphBackgroud'],
                        plot_bgcolor = colors['graphBackgroud'], font = dict(family='Courier New, monospace', size=14, color = colors['text']),
                        xaxis = dict(range = [start_date, end_date],
                                    showgrid=True,
                                    gridwidth=0.01, gridcolor=colors['gridlines'],
                                    showline=False, linewidth=1, linecolor=colors['text']),
                        yaxis = dict(range = [start_price, end_price], title='USD'),
                        yaxis2 = dict(range = [start_volume, end_volume], title = 'Volume'),
                        height = 750,
                        margin = {'l': 40, 'r': 40, 'b': 10, 't': 10, 'pad': 4},
                        legend = dict( orientation = 'h', x = 0, y = 1.1),
                        showlegend=True,
                        hovermode = 'x', hoverlabel = dict(font = dict(family='Courier New, monospace', size=14, color = colors['text']))
                        )

    # Create two subplots 
    figure = make_subplots(rows = 5, cols = 1, shared_xaxes=True,
    specs=[
        [{'rowspan':4}],
        [None],
        [None],
        [None],
        [{}],
    ])
    
    # Add to top subplot
    figure.append_trace(candlestick_trace, row = 1, col = 1)
    figure.append_trace(trace_volume, row = 5, col = 1)
    
    # Moving averages to subplots
    for ma_trace in ma_traces:
        if len(ma_traces) >= 1:
            figure.add_trace(ma_trace, row = 1, col = 1)

    # Update figure layout
    figure.update_layout(layout, xaxis_rangeslider_visible=False)
    
    return figure


def get_moving_average(moving_averages, close_data):
    ma_traces = []

    for MA in moving_averages:
        
         if MA == 'SMA50' :
             # Get SMA
             SMA50  = get_SMA(close_data, 50)
             
             # Get Trace
             trace_dummy = go.Scatter(x = SMA50.index,
                                      y = SMA50,
                                      mode='lines',
                                      name = MA,
                                      line = dict(color='magenta', width = 1),
                                      hoverlabel = dict(font = dict(family='Courier New, monospace', size=8, color = colors['text'])))
             # append
             ma_traces.append(trace_dummy)
         
         elif MA == 'SMA200' :
             # Get SMA
             SMA200 = get_SMA(close_data, 200)
             
             # Get Trace
             trace_dummy = go.Scatter(x = SMA200.index,
                                      y = SMA200,
                                      mode='lines',
                                      name = MA,
                                      line = dict(color='royalblue', width = 1),
                                      hoverlabel = dict(font = dict(family='Courier New, monospace', size=8, color = colors['text'])))
             # append
             ma_traces.append(trace_dummy)
             
         elif MA == 'EMA9' :
             # Get EMA
             EMA9 = get_EMA(close_data, 9)
             
             # Get Trace
             trace_dummy = go.Scatter(x = EMA9.index,
                                      y = EMA9,
                                      mode='lines',
                                      name = MA,
                                      line = dict(color='blueviolet', dash='dash', width = 1),
                                      hoverlabel = dict(font = dict(family='Courier New, monospace', size=8, color = colors['text'])))
             # append
             ma_traces.append(trace_dummy)
             
         elif MA == 'EMA20' :
             # Get EMA
             EMA20 = get_EMA(close_data, 20)
             
             # Get Trace
             trace_dummy = go.Scatter(x = EMA20.index,
                                      y = EMA20,
                                      mode='lines',
                                      name = MA,
                                      line = dict(color='orange', dash='dash', width = 1),
                                      hoverlabel = dict(font = dict(family='Courier New, monospace', size=8, color = colors['text'])))
             # append
             ma_traces.append(trace_dummy)

    return ma_traces
             


def get_yrange(start_date, end_date, data, column_label):

    # Get selected column
    selected_column = data[column_label]

    # Get max and min
    max_val = selected_column[start_date:end_date].max()
    min_val = selected_column[start_date:end_date].min()

    # Get range
    diff = max_val - min_val

    # Get delta
    delta = diff * 0.1

    # Define axis range
    y_start = min_val - delta
    if y_start < 0:
        y_start = 0
    
    y_end = max_val + delta

    return y_start, y_end


###############################################################################
#                                Ticker info                                  #
###############################################################################

@app.callback(Output('Ticker-Info', 'children'),
              [Input('Ticker-Picker', 'value')])
def update_ticker_info(ticker):
    # Read data
    nasdaq_info = pd.read_csv('data/nasdaq_info.csv')
    
    # Filter by ticker value
    nasdaq_info = nasdaq_info[nasdaq_info['symbol'] == ticker]

    # Get data
    name = nasdaq_info['name'].values[0]
    country = nasdaq_info['country'].values[0]
    ipo_year = nasdaq_info['ipoyear'].values[0]
    sector = nasdaq_info['sector'].values[0]
    industry = nasdaq_info['industry'].values[0]

    # Get info
    info = f"""
    {name}

    **Country**: {country}

    **IPO Year**: {ipo_year}

    **Sector**: {sector}

    **Industry**: {industry}
    """

    return info