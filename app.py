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

# For visualization
import dash
import dash_bootstrap_components as dbc

# For web hosting
import gunicorn


###############################################################################
#                              8. Make Web App                                #
###############################################################################

# Define dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#app = dash.Dash(__name__)
app.title = 'TRIFORCE ANALYTICS'

# Use for deployment
application = app.server