"""
This code was taken from another dashboard application. To check it out
visit: https://dash-gallery.plotly.host/dash-svm/

The source code can be found here:
https://github.com/plotly/dash-svm/blob/master/utils/dash_reusable_components.py

Thanks Xhlulu for writing this awesome code!
"""

from textwrap import dedent

import dash_core_components as dcc
import dash_html_components as html

# For styles
from assets.Styles import DashComponentStyles

# Get colors
colors = DashComponentStyles().colors

# Display utility functions
def _merge(a, b):
    return dict(a, **b)


def _omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


# Custom Display Components
def Card(children, **kwargs):
    return html.Section(
        children,
        style=_merge({
            'background': colors['foreground'],
            'font-color': 'white',         
            # Remove possibility to select the text for better UX
            'user-select': 'none',
            '-moz-user-select': 'none',
            '-webkit-user-select': 'none',
            '-ms-user-select': 'none'
        }, kwargs.get('style', {})),
        **_omit(['style'], kwargs)
    )


def FormattedSlider(**kwargs):
    return html.Div(
        style=kwargs.get('style', {}),
        children=dcc.Slider(**_omit(['style'], kwargs))
    )


def NamedSlider(name, **kwargs):
    return html.Div(
        style={'padding': '20px 10px 25px 4px'},
        children=[
            html.P(f'{name}:'),
            html.Div(
                style={'margin-left': '6px'},
                children=dcc.Slider(**kwargs)
            )
        ]
    )


def NamedDropdown(name, **kwargs):
    for key, value in kwargs.items():
        if key == 'style':
            temp_style = value
            temp_style.update({'margin-left': '3px'})
        else:
            temp_style = {'margin-left': '3px'}
            
    return html.Div(
        style={'margin': '10px 0px'},
        children=[
            html.P(
                children=f'{name}:',
                style= temp_style
            ),

            dcc.Dropdown(**kwargs)
        ]
    )


def NamedRadioItems(name, **kwargs):
    return html.Div(
        style={'padding': '20px 10px 25px 4px'},
        children=[
            html.P(children=f'{name}:'),
            dcc.RadioItems(**kwargs)
        ]
    )


# Non-generic
def DemoDescription(filename, strip=False):
    with open(filename, 'r') as file:
        text = file.read()

    if strip:
        text = text.split('<Start Description>')[-1]
        text = text.split('<End Description>')[0]

    return html.Div(
            className='row',
            style={
                'padding': '15px 30px 27px',
                'margin': '45px auto 45px',
                'width': '100%',
                'max-width': '1024px',
                'borderRadius': 5,
                'border': 'thin lightgrey solid',
                'font-family': 'Roboto, sans-serif'
            },
            children=dcc.Markdown(dedent(text))
    )