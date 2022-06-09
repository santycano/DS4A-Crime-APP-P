# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()


# dfg = pd.read_csv(DATA_PATH.joinpath("opsales.csv"))

layout = html.Div([
    html.H1('General Product Sales', style={"textAlign": "center"}),

    html.Div([
        
        html.H1('Pruebaamapa')
    ], className='row'),

    
])


