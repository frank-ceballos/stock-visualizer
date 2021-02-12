""" ***************************************************************************
# * File Description:                                                         *
# * Creates a simple dashboard that visualize historical stock data.          *
# *                                                                           *
# * The contents of this script are:                                          *
# * 1. Importing Libraries                                                    *
# *                                                                           *
# * --------------------------------------------------------------------------*
# * AUTHORS(S): Frank Ceballos <frank.ceballos123@gmail.com>                  *
# *           : David Sicilian                                                *
# * --------------------------------------------------------------------------*
# * DATE CREATED: June 1, 2020                                                *
# * LAST UPDATE : February 12, 2021                                           *
# * --------------------------------------------------------------------------*
# * NOTES:                                                                    *
# * ************************************************************************"""


###############################################################################
#                          1. Importing Libraries                             #
###############################################################################
# For data management
import pandas as pd
import numpy as np

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

# To grab stock data
import yfinance as fyf
from pandas_datareader import data as pdr
fyf.pdr_override() # <-- Here is the fix

# To create datetime objects 
import datetime
from datetime import datetime as dt

# For styles
from assets.Styles import DashComponentStyles

# For web hosting
import gunicorn


###############################################################################
#                             3. Web App Styling                              #
###############################################################################
# Get colors
colors = DashComponentStyles().colors

# Define fonts
fontProps = {'H1FontFamily': 'sans', 'H1FontSize':'100%',
             'H1FontWeight': 'lighter'}

# Dropdown Style
styleDropdown =  {'background':colors['navBackground'], 
                  'border-color': colors['bullish'], 
                  'color': 'white'}

# Card style
style_card1 = {'margin-bottom': 1, 'margin-top': 2, 'margin-right': 2,
              'margin-left': 2}


###############################################################################
#                               4. Nav Bar                                    #
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
#                            5. Top Card Dropdowns                            #
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


description = ''

row_description = dbc.Row([dbc.Col(html.Div(description, 
                style = {'font-size': 16, 'padding-bottom':12}), width=12)])

row1 = dbc.Row([
            dbc.Col(html.Div(TickerDropdown), width = 8),
               ]
    )
topCardRows = [row_description, row1]

topCardDiv = dbc.Row([dbc.Col(drc.Card(html.Div(topCardRows,
                    className='rowDiv'), 
                    style = style_card1,
                    className='cardCustom'), width=2),
                       ])

###############################################################################
#                              8. Make Web App                                #
###############################################################################

# Define dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(__name__)
app.title = 'TRIFORCE ANALYTICS'

# Edit layout
app.layout = html.Div(children = [navBar, topCardDiv], id = 'maindiv')

# Use for deployment
server = app.server

# Run app
if __name__ == '__main__':
    #app.run_server(debug=False)
    app.run_server(port=8090,host='0.0.0.0', debug = True)