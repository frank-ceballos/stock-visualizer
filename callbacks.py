import plotly.graph_objs as go
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output

from app import app

# For styles
from assets.Styles import DashComponentStyles

###############################################################################
#                             1. Web App Styling                              #
###############################################################################
# Get colors
colors = DashComponentStyles().colors


@app.callback(Output('Close-Line-Graph', 'figure'),
              [Input('Ticker-Picker', 'value')])
def updateCloseLineGraph(stocks, start, end):
    # Get data
    df = getStockClose(stocks)
    
    # Filter by date
    if start != 'None' and start != None:
        # Define start date
        start_date = f'{start}-01-01'
        
        # Define mask
        mask = df.index > start_date
    
        # Filter data by date
        df = df.loc[mask]
    
    # Define traces list
    traces = []
    
    # Add line traces
    for stock in stocks:
        # Set column label
        column_label = stock + ' ' + 'Close'
        
        # Create trace
        temp_trace = go.Scatter(
                                x = df.index,
                                y = df[column_label],
                                name = stock
                                )
        # Append trace
        traces.append(temp_trace)
    print(f'THE START DATE IS: {df.index[0]}')
    # Set layout
    layout = go.Layout(paper_bgcolor = colors['foreground'],
                        plot_bgcolor = colors['foreground'], font = dict(family='Courier New, monospace', size=14, color = colors['text']),
                        xaxis = dict(range = [df.index[0], df.index[-1]],
                                    showgrid=True,
                                    gridwidth=0.01, gridcolor=colors['gridlines'],
                                    showline=False, linewidth=1, linecolor=colors['text']),
                        height = 450,
                        margin = {'l': 40, 'r': 40, 'b': 10, 't': 10, 'pad': 4},
                        legend = dict( orientation = 'h', x = 0, y = 1.1),
                        showlegend=True,
                        hovermode = 'x', hoverlabel = dict(font = dict(family='Courier New, monospace', size=14, color = colors['text']))
                        )
    
    # Create two subplots 
    figure = make_subplots(rows = 1 , cols = 1)
    
    # Add to top subplot
    for trace in traces:
        figure.add_trace(trace, row = 1, col = 1)
    
    # Update figure layout
    figure.update_layout(layout)
    
    return figure