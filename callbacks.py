import plotly.graph_objs as go
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output

from app import app

# For styles
from assets.Styles import DashComponentStyles

from datetime import date, timedelta

from finance.tools import get_ticker_data

###############################################################################
#                             1. Web App Styling                              #
###############################################################################
# Get colors
colors = DashComponentStyles().colors

@app.callback(Output('Close-Line-Graph', 'figure'),
              [Input('Ticker-Picker', 'value')])
def updateCloseLineGraph(ticker):
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
    start_date = date.today() - timedelta(days=90)
    end_date = date.today()

    # Get y-axis Candlesticks Chart
    start_price, end_price = get_yrange(start_date, end_date, data, 'Close')

    # Get y-axis Volume Chart
    start_volume, end_volume = get_yrange(start_date, end_date, data, 'Volume')

    # Set layout
    layout = go.Layout(paper_bgcolor = colors['foreground'],
                        plot_bgcolor = colors['foreground'], font = dict(family='Courier New, monospace', size=14, color = colors['text']),
                        xaxis = dict(range = [start_date, end_date],
                                    showgrid=True,
                                    gridwidth=0.01, gridcolor=colors['gridlines'],
                                    showline=False, linewidth=1, linecolor=colors['text']),
                        yaxis = dict(range = [start_price, end_price]),
                        yaxis2 = dict(range = [start_volume, end_volume]),
                        height = 650,
                        margin = {'l': 40, 'r': 40, 'b': 10, 't': 10, 'pad': 4},
                        legend = dict( orientation = 'h', x = 0, y = 1.1),
                        showlegend=True,
                        hovermode = 'x', hoverlabel = dict(font = dict(family='Courier New, monospace', size=14, color = colors['text']))
                        )

    # Create two subplots 
    figure = make_subplots(rows = 2 , cols = 1, shared_xaxes=True)
    
    # Add to top subplot
    figure.add_trace(candlestick_trace, row = 1, col = 1)
    figure.add_trace(trace_volume, row = 2, col = 1)

    # Update figure layout
    figure.update_layout(layout, xaxis_rangeslider_visible=False)
    
    return figure



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