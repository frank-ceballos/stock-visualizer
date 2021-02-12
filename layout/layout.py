
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
#                             3. Web App Styling                              #
###############################################################################
# Get colors
colors = DashComponentStyles().colors

# Dropdown Style
styleDropdown = DashComponentStyles().styleDropdown

# Card style
style_card1 = DashComponentStyles().ticker_picker_card



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