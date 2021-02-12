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
# * LAST UPDATE : August 1, 2020                                              *
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

# For web hosting
import gunicorn
