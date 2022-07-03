
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc

from app import app

# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()


# dfg = pd.read_csv(DATA_PATH.joinpath("opsales.csv"))

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-map', figure={},className='graphtamañomapa'),
            # html.H6("Card subtitle", className="card-subtitle"),
            # html.P(
            #     "Some quick example text to build on the card title and make "
            #     "up the bulk of the card's content.",
            #     className="card-text",
            # ),
            # dbc.CardLink("Card link", href="#"),
            # dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
   class_name='card border-primary cardtamañomapa',
)


card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-map', figure={},style={'width':'450px'}),
            # html.H6("Card subtitle", className="card-subtitle"),
            # html.P(
            #     "Some quick example text to build on the card title and make "
            #     "up the bulk of the card's content.",
            #     className="card-text",
            # ),
            # dbc.CardLink("Card link", href="#"),
            # dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
    style={"width": "28rem"},class_name='card border-primary',
)


layout = html.Div([
    # html.H1('General Product Sales', style={"textAlign": "center"}),

    html.Div([

        html.Div(html.Span('Crime counter',style={'fontFamily': 'Inter','fontStyle': 'normal', 'fontWeight': '400','fontSize': '20px', 'lineHeight': '24px', 'color': '#FFFFFF'}),className='CrimeCounterTitle'),
        html.Div([
            html.Span('11.530',className='crimeCounterNumber'),
            html.Img(src=app.get_asset_url('imagenes/ExtraIcons/IconStatistics.png'),style={'padding':'5px'})

        ],className='crimeCounter'),


        html.Div([

            html.Div([
                html.Span('Year',className='leftnavBarInputFont'),
            dcc.Dropdown(['2016', '2017', '2018','2019'], id='year',style={'width':'180px'}),
            ]),
            
            html.Div([
             html.Span('Month',className='leftnavBarInputFont'),
            dcc.Dropdown(['Janauary', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], id='Month',style={'width':'180px'}),

            ],style={'paddingTop':'10px'}),

            html.Div([
             html.Span('Day',className='leftnavBarInputFont'),
            dcc.Dropdown(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], id='Day',style={'width':'180px'}),    
            # dcc.Input(
            # id="day",
            # type="number",
            # placeholder="",
            # style={'height':'28px'},
            # )            
            ],style={'paddingTop':'10px'}),


            html.Div([
             html.Span("Criminal offense",className='leftnavBarInputFont'),
            dcc.Dropdown(['Robbery', 'Aggravated assault', 'Total violent crime'], id='offense',style={'width':'180px'}),                
            ],style={'paddingTop':'10px'}),
        
        
        ],style={'top':'300px','position':'absolute','paddingLeft':'28px'}),


    ],className='leftnavBar'),

    html.Div([
    html.H2('Spatial analysis'),

    ],className='TituloSecciones'),

    # dbc.Row([
    #     dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'}),dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'})
    # ],style={'marginLeft':'300px','display':'flex','justifyContent':'space-between','marginRight':'100px','flexWrap':'wrap'}),


    dbc.Row([
        dbc.Col([card],style={'marginTop':'1.5rem'})
    ],style={'marginLeft':'236px','display':'flex','justifyContent':'center','marginBottom':'50px','flexWrap':'wrap'}),

     dbc.Row([
        dbc.Col([card2],style={'marginTop':'1.5rem'}), dbc.Col([card2],style={'marginTop':'1.5rem'}), dbc.Col([card2],style={'marginTop':'1.5rem'}),dbc.Col([card2],style={'marginTop':'1.5rem'}), dbc.Col([card2],style={'marginTop':'1.5rem'}), dbc.Col([card2],style={'marginTop':'1.5rem'})
    ],style={'marginLeft':'336px','display':'flex','justifyContent':'space-between','marginRight':'100px','flexWrap':'wrap','marginBottom':'50px'}),


    # dcc.Graph(id='my-map', figure={}),
])





