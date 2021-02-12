
# To import packages a directory above
import sys
import os
sys.path.append(os.path.realpath('..'))

# For visualization
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_table
import dash_components.dashReusableComponents as drc
from dash.dependencies import Input, Output, ALL, State

# For styles
from assets.Styles import DashComponentStyles


###############################################################################
#                             1. Web App Styling                              #
###############################################################################
# Get colors
colors = DashComponentStyles().colors

# Dropdown Style
styleDropdown = DashComponentStyles().styleDropdown

# Card style
style_card1 = DashComponentStyles().ticker_picker_card
style_card2 = DashComponentStyles().style_card2



###############################################################################
#                               2. Nav Bar                                    #
###############################################################################

# Define navigation bar
navBar = dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='assets/logo.png', height="55px",
                                             className="ml-2")),
                            dbc.Col(dbc.NavbarBrand("TRIFORCE ANALYTICS", className="ml-2", style={'font-size':'25px',
                                                                                                   'font-weight':550},
                                                    href = 'https://www.frank-ceballos.com')),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="https://plot.ly",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
            ],
            color=colors['navBackground'],
            dark=True,
            
        )

###############################################################################
#                                3. Dropdowns                                 #
###############################################################################

# Define Ticker Dropdown
Market = {'AAPL': 'AAPL',
          'GOOG': 'GOOG',
          'MSFT': 'MSFT'}

MarketOptions = [{'label': key, 'value': Market[key]} for key in Market]

TickerDropdown = html.Div(dcc.Dropdown(
    id = 'Ticker-Picker',
    options = MarketOptions,
    searchable = True,
    multi = True,
    value = ['GOOG'],
    style = styleDropdown,
    placeholder = 'Search markets...'
), className = 'Dropdown')


row1 = dbc.Row([
            dbc.Col(html.Div(TickerDropdown), width = 9, style = {'padding':0, 'margin':0}),
               ],style = {'padding':0, 'margin':0}
    )

topCardRows = [row1]

topCardDiv = dbc.Row([dbc.Col(drc.Card(html.Div(topCardRows,
                    className='rowDiv'), 
                    style = style_card1,
                    className='cardCustom'), width=2),
                       ])


###############################################################################
#                                4. Graphs                                 #
###############################################################################
candle_chart = dbc.Row([
                      dbc.Col(drc.Card(html.Div(
                                dcc.Graph(id = 'Close-Line-Graph'), className='rowDiv'),style = style_card2, 
                          className='cardCustom'), width=5),
                      ])

###############################################################################
#                                 9. Callbacks                                #
###############################################################################

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
