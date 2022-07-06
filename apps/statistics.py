import pathlib

from app import app
from dash import dcc
from dash import html
from click import style

from shapely import wkt                     # Geometry manipulation
from pysal.lib import weights               # Spatial weights
from pysal.explore import esda              # Exploratory Spatial analytics
from splot import esda as esdaplot          # Exploratory Spatial analytics
from sqlalchemy import create_engine, text  # Sql manipulation
from shapely.geometry import Polygon, Point
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd                         # Tabular data manipulation
import geopandas as gpd                     # Spatial data manipulation
import plotly.express as px
import dash_bootstrap_components as dbc

DB_USERNAME = 'postgres' # Replace with the username you just created
DB_PASSWORD = 'Team227pry_' # Replace with the password you just created

engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@ds4a-team227-test.cqkc95x5yyj2.us-east-1.rds.amazonaws.com/crimen_bga', max_overflow=20)

df = pd.read_sql_table("crimen_base_ex",engine)

df = df.astype({"armas_medios": "category", "barrios_hecho": "category", "zona": "category", "nom_comuna": "category", "dia_semana": "category",
                "descripcion_conducta": "category", "conducta": "category", "clasificaciones_delito": "category", "curso_de_vida": "category",
                "estado_civil_persona": "category", "genero": "category", "movil_agresor": "category", "movil_victima": "category","mes":"category"})

df["dia_semana"] = df["dia_semana"].cat.reorder_categories(["01. Lunes","02. Martes","03. Miércoles","04. Jueves",
                                                            "05. Viernes","06. Sábado","07. Domingo"])

cell = pd.read_sql_table("grid",engine)  # Grid read
df2 = df.dropna(subset=['latitud', 'longitud'])

crs = {'init':'epsg:4326'}

lat_lon = []
for i in zip(df2.longitud, df2.latitud):
    lat_lon.append(Point(eval(str(i))))

df2 = df2.drop(columns=['longitud', 'latitud'])

gdf = gpd.GeoDataFrame(df2, geometry=lat_lon, crs = crs)

# Geometry set up grid
cell['geometry'] = cell['geometry'].apply(wkt.loads)
geometry = cell.geometry
cell = cell.drop(['geometry'], axis=1)
cell = gpd.GeoDataFrame(cell, geometry=geometry, crs = crs)

join = gpd.sjoin(gdf, cell, how='left')

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfg = pd.read_csv(DATA_PATH.joinpath("opsales.csv"))

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-map', figure={},style={'width':'450px'}),
        ]
    ),
    style={"width": "28rem"},class_name='card border-primary',
)

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-map', figure={},style={'width':'450px'}),
        ]
    ),
    style={"width": "28rem"},class_name='card border-primary',
)

card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Moran I", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='moran-i', figure={},style={'width':'450px'}),
        ]
    ),
    style={"width": "28rem"},class_name='card border-primary',
)





layout = html.Div([

    html.Div([

        html.Div(
            html.Span('Crime counter',
                      style={'fontFamily': 'Inter','fontStyle': 'normal', 'fontWeight': '400','fontSize': '20px', 'lineHeight': '24px', 'color': '#FFFFFF'}),
            className='CrimeCounterTitle'),
        html.Div([
            html.Span('11.530',className='crimeCounterNumber'),
            html.Img(src=app.get_asset_url('imagenes/ExtraIcons/IconStatistics.png'),style={'padding':'5px'})
        ],className='crimeCounter'),

        html.Div([
             html.Div([
                html.Span('Year',className='leftnavBarInputFont'),
                 dcc.Dropdown(options=['Crimenes domesticos', 'Hurto y lesiones personales', 'Homicidio y otras lesiones',
                                       'Lesiones en accidente de transito', 'Secuestro y relacionados'],
                              id='crime-dropdown',style={'width':'180px'},value='Hurto y lesiones personales',
                              clearable=False,persistence=True, persistence_type='local',),
             ]),

            html.Div([
                html.Span('Month',className='leftnavBarInputFont'),
                dcc.Dropdown(id='year-dropdown', value=2010, clearable=False,
                             persistence=True, persistence_type='session',
                             options=[{'label': x, 'value': x} for x in sorted(df.ano.unique())], style={'width':'180px'}),
            ],style={'paddingTop':'10px'}),

            html.Div([
                html.Span('Day',className='leftnavBarInputFont'),
                dcc.Dropdown(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], id='Day',style={'width':'180px'}),
            ],style={'paddingTop':'10px'}),

            html.Div([
                html.Span("Victim's gender",className='leftnavBarInputFont'),
                dcc.Dropdown(['Male', 'Female', 'Undefined'], id='gender',style={'width':'180px'}),
            ],style={'paddingTop':'10px'}),

            html.Div([
                html.Span("Neighborhood",className='leftnavBarInputFont'),
                dcc.Dropdown(['San Francisco', 'La Concordia', 'Provenza'], id='neighborhood',style={'width':'180px'}),
            ],style={'paddingTop':'10px'}),

            html.Div([
                html.Span("Criminal offense",className='leftnavBarInputFont'),
                dcc.Dropdown(['Robbery', 'Aggravated assault', 'Total violent crime'], id='offense',style={'width':'180px'}),
            ],style={'paddingTop':'10px'}),

            html.Div([
                html.Span("Victim's age",className='leftnavBarInputFont'),
                dcc.RangeSlider(0, 80, value=[0, 80],tooltip={"placement": "bottom", "always_visible": True})
            ],style={'paddingTop':'10px'}),

        ],style={'top':'300px','position':'absolute','paddingLeft':'28px'}),

    ],className='leftnavBar'),

    html.Div([
        html.H2('Crime statistics'),
    ],className='TituloSecciones'),

    dbc.Row([
        dbc.Col([card1],style={'marginTop':'1.5rem'}),
        dbc.Col([card],style={'marginTop':'1.5rem'}),
        dbc.Col([card],style={'marginTop':'1.5rem'}),
        dbc.Col([card],style={'marginTop':'1.5rem'})
    ],style={'marginLeft':'300px','display':'flex','justifyContent':'space-between','marginRight':'100px','flexWrap':'wrap'}),

])

@app.callback(
    Output(component_id='my-map', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='crime-dropdown', component_property='value')]
)
def display_value(year_chosen, crime_chosen):
    join1 = join[(join.categ_crimen == crime_chosen) & (join.ano == year_chosen)]
    join1 = join1.groupby(['neigh']).orden.count().reset_index().rename({'orden':'crime_count'}, axis=1)

    data = []

    for j in range(len(cell)):
        data.append([j, 0])

    data = np.array(data)

    for k in range(len(join1)):
        data[int(join1.values[k, 0]), 1] = int(join1.values[k, 1])

    join1 = pd.DataFrame(data, columns=['neigh', 'crime_count'])
    join1.neigh = join1.neigh.astype(int)
    join1.crime_count = join1.crime_count.astype(int)

    fig = px.choropleth_mapbox(join1, geojson=cell, locations='neigh', color='crime_count',
                               color_continuous_scale="Viridis",
                               range_color=(join1.crime_count.min(), join1.crime_count.max()),
                               mapbox_style="carto-positron",
                               zoom=12, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

@app.callback(
    Output(component_id='moran-i', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='crime-dropdown', component_property='value')]
)
def display_value(year_chosen, crime_chosen):
    join1 = join[(join.categ_crimen == crime_chosen) & (join.ano == year_chosen)]
    join1 = join1.groupby(['neigh']).orden.count().reset_index().rename({'orden':'crime_count'}, axis=1)

    data = []

    for j in range(len(cell)):
        data.append([j, 0])

    data = np.array(data)

    for k in range(len(join1)):
        data[int(join1.values[k, 0]), 1] = int(join1.values[k, 1])

    join1 = pd.DataFrame(data, columns=['neigh', 'crime_count'])
    join1.neigh = join1.neigh.astype(int)
    join1.crime_count = join1.crime_count.astype(int)

    fig = px.choropleth_mapbox(join1, geojson=cell, locations='neigh', color='crime_count',
                               color_continuous_scale="Viridis",
                               range_color=(join1.crime_count.min(), join1.crime_count.max()),
                               mapbox_style="carto-positron",
                               zoom=12, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

#%%
