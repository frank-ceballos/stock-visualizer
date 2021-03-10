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

# Imoprt app
from app import app
from layout import layout1
from callbacks import *

# GEt finance tools
from finance.tools import get_nasdaq_data

# For web hosting
import gunicorn

###############################################################################
#                              Grab NASDAQ DATA                               #
###############################################################################
get_nasdaq_data()

###############################################################################
#                              8. Make Web App                                #
###############################################################################

# Edit layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')],
    id = 'maindiv')

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
         return layout1
    else:
         return layout1


# Run app
if __name__ == '__main__':
    app.run_server(port=8080,host='0.0.0.0', debug = False)