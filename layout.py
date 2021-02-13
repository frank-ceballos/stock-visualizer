
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
    multi = False,
    style = styleDropdown,
    placeholder = 'Search markets...'),
    className = 'Dropdown')


###############################################################################
#                          4. Dropdown Layouts                                #
###############################################################################

dropdownRow1 = dbc.Row([
            dbc.Col(html.Div(TickerDropdown), width = 12, 
                    style = {'padding':0, 'margin':0})],
            style = {'padding':0, 'margin':0}
            )

dropdownRows = [dropdownRow1]

dropdownCard = dbc.Row([dbc.Col(drc.Card(html.Div(dropdownRows ,
                    className='rowDiv'), 
                    style = style_card1,
                    className='cardCustom'), width=12),
                       ])


###############################################################################
#                            4. Graphs Layouts                                #
###############################################################################
candlestickCard = drc.Card(
    html.Div(
            dcc.Graph(id = 'Close-Line-Graph'), 
            className='rowDiv'),
    style = style_card2, 
    className='cardCustom')





###############################################################################
#                                4. layouts                                   #
###############################################################################

row1 = dbc.Row([
                dbc.Col(html.Div(dropdownCard), width=2),
                dbc.Col(candlestickCard, width=9)])

# Define layouts

layout1 = html.Div([
    navBar, row1,
    dcc.Link('Go to App 1', href='/apps/app1')
    ])
