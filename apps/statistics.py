# import dash_core_components as dcc
from datetime import date
from click import style
from dash import dcc
# import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

import sqlalchemy
from sqlalchemy import create_engine, text


DB_USERNAME = 'postgres' # Replace with the username you just created
DB_PASSWORD = 'Team227pry_' # Replace with the password you just created

engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@ds4a-team227-test.cqkc95x5yyj2.us-east-1.rds.amazonaws.com/crimen_bga', max_overflow=20)



df = pd.read_sql_table("crimen_base_ex",engine)

# df = df.astype({"armas_medios": "category", "barrios_hecho": "category", "zona": "category", "nom_comuna": "category", "dia_semana": "category",  

# "descripcion_conducta": "category", "conducta": "category", "clasificaciones_delito": "category", "curso_de_vida": "category",  

# "estado_civil_persona": "category", "genero": "category", "movil_agresor": "category", "movil_victima": "category","mes":"category"}) 

df2= pd.read_sql_table("crimen_base_ex_mod",engine)



# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


dfg = pd.read_csv(DATA_PATH.joinpath("opsales.csv"))

# card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H4("Title", id="card-title"),
#             html.H2("100", id="card-value"),
#             html.P("Description", id="card-description")
#         ]
#     )
# )

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title",style={'textAlign':'center'}),
            # dcc.Graph(id='my-map', figure={},style={'width':'450px'}),
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
                html.Span('Date',className='leftnavBarInputFont'),
            # dcc.Dropdown(options=[{'label': x, 'value': x} for x in sorted(dfg["Order Country"].unique())], id='country-dropdown',style={'width':'180px'},value='India', clearable=False,
            #     persistence=True, persistence_type='local',),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2017, 9, 19),
                initial_visible_month=date(2017, 8, 5),
                end_date=date(2017, 8, 25),
                style={'width':'180px','zIndex':'100'},
                ),
            ]),




            
            # html.Div([
            #  html.Span('Month',className='leftnavBarInputFont'),
            # dcc.Dropdown(id='pymnt-dropdown', value='DEBIT', clearable=False,
            #     persistence=True, persistence_type='session',
            #     options=[{'label': x, 'value': x} for x in sorted(dfg["Type"].unique())],style={'width':'180px'}),

            # ],style={'paddingTop':'10px'}),



            # html.Div([
            #  html.Span('Day',className='leftnavBarInputFont'),
            # dcc.Dropdown(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], id='Day',style={'width':'180px'}),    
           
            # ],style={'paddingTop':'10px'}),

            # html.Div([
            #  html.Span("Victim's gender",className='leftnavBarInputFont'),
            # dcc.Dropdown(['Male', 'Female', 'Undefined'], id='gender',style={'width':'180px'}),                
            # ],style={'paddingTop':'10px'}),

            html.Div([
             html.Span("Neighborhood",className='leftnavBarInputFont'),
            dcc.Dropdown(options=[{'label': str(x), 'value': str(x)} for x in list(df.nom_comuna.unique())]+ [{'label': 'All', 'value': 'All'}], id='nomComuna-dropdown',style={'width':'180px'}, clearable=False,
                persistence=True, persistence_type='local',),                
            ],style={'paddingTop':'10px'}),

            html.Div([
             html.Span("Criminal offense",className='leftnavBarInputFont'),
            dcc.Dropdown(options=[{'label': str(x), 'value': str(x)} for x in list(df.conducta.unique())]+ [{'label': 'All', 'value': 'All'}], id='nomConducta-dropdown',style={'width':'180px',"display": "inline-block"}, clearable=False,
                persistence=True, persistence_type='local',optionHeight=100),                 
            ],style={'paddingTop':'10px'}),

            # html.Div([
            #  html.Span("Victim's age",className='leftnavBarInputFont'),
            # dcc.RangeSlider(0, 80, value=[0, 80],tooltip={"placement": "bottom", "always_visible": True})
            # ],style={'paddingTop':'10px'}),
        
        
        ],style={'top':'300px','position':'absolute','paddingLeft':'28px'}),


    ],className='leftnavBar'),

    html.Div([
    html.H2('Crime statistics'),

    ],className='TituloSecciones'),









    


    #  html.H1('General Product Sales', style={"textAlign": "center"}),

    # html.Div([
    #     html.Div([
    #         html.Pre(children="Payment type", style={"fontSize":"150%"}),
    #         dcc.Dropdown(
    #             id='pymnt-dropdown', value='DEBIT', clearable=False,
    #             persistence=True, persistence_type='session',
    #             options=[{'label': x, 'value': x} for x in sorted(dfg["Type"].unique())]
    #         )
    #     ], className='six columns'),

    #     html.Div([
    #         html.Pre(children="Country of destination", style={"fontSize": "150%"}),
    #         dcc.Dropdown(
    #             id='country-dropdown', value='India', clearable=False,
    #             persistence=True, persistence_type='local',
    #             options=[{'label': x, 'value': x} for x in sorted(dfg["Order Country"].unique())]
    #         )
    #         ], className='six columns'),
    # ], className='row'),

    # dcc.Graph(id='my-map', figure={},style={'width':'500px','marginLeft':'300px'}),
    dbc.Row([
        dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'}),dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'}), dbc.Col([card],style={'marginTop':'1.5rem'})
    ],style={'marginLeft':'300px','display':'flex','justifyContent':'space-between','marginRight':'100px','flexWrap':'wrap','marginBottom':'50px'}),

    # dbc.Row([
    #     dbc.Col([card]), dbc.Col([card]), dbc.Col([card])
    # ],style={'marginLeft':'300px','display':'flex','justify-content':'space-between','marginRight':'100px','marginTop':'50px','flexWrap':'wrap'}),
])


# @app.callback(
#     Output(component_id='my-map', component_property='figure'),
#     [Input(component_id='pymnt-dropdown', component_property='value'),
#      Input(component_id='country-dropdown', component_property='value')]
# )
# def display_value(pymnt_chosen, country_chosen):
#     dfg_fltrd = dfg[(dfg['Order Country'] == country_chosen) &
#                     (dfg["Type"] == pymnt_chosen)]
#     dfg_fltrd = dfg_fltrd.groupby(["Customer State"])[['Sales']].sum()
#     dfg_fltrd.reset_index(inplace=True)
#     fig = px.choropleth(dfg_fltrd, locations="Customer State",
#                         locationmode="USA-states", color="Sales",
#                         scope="usa")
#     return fig