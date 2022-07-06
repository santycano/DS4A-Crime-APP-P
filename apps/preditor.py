from dash import dcc
from dash import html
from app import app

from shapely import wkt                     # Geometry manipulation
from shapely.geometry import Point
from sqlalchemy import create_engine        # Sql manipulation
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd                         # Tabular data manipulation
import geopandas as gpd                     # Spatial data manipulation
import plotly.express as px
import dash_bootstrap_components as dbc

import warnings
warnings.filterwarnings("ignore")

DB_USERNAME = 'postgres' # Replace with the username you just created
DB_PASSWORD = 'Team227pry_' # Replace with the password you just created

engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@ds4a-team227-test.cqkc95x5yyj2.us-east-1.rds.amazonaws.com/crimen_bga', max_overflow=20)

cols = [
    "nom_comuna",
    "ano",
    "categ_crimen",
    "longitud",
    "latitud",
    "cluster_predicted"
]

cluster = pd.read_sql_table("cluster",engine,columns=cols)

cell = pd.read_sql_table("grid",engine)  # Grid read
df2 = cluster.dropna(subset=['latitud', 'longitud'])

crs={'init':'epsg:4326'}

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

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Cluster map", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='cluster-map', figure={}, className='graphtamañomapa', style={'width':'700px', 'height':'700px'})
        ]
    ),
    style={"width": '100%'}, class_name='card border-primary cardtamañomapa'
)

card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Crime category by cluster", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='crime_category', figure={},style={'width':'600px', 'height':'600px'}),
        ]
    ),
    style={"width": '100%'},class_name='card border-primary',
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Cluster distribution by comuna", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='comuna_by_cluster', figure={},style={'width':'600px', 'height':'600px'}),
        ]
    ),
    style={"width": '100%'},class_name='card border-primary',
)

layout = html.Div([

    html.Div([

        html.Div([

            html.Div([
                html.Span('Year',className='leftnavBarInputFont'),
                dcc.Dropdown([2014, 2015, 2016, 2017, 2018, 2019], value=2015, id='year-dropdown',style={'width':'180px'})
            ])
       
        ],style={'top':'300px','position':'absolute','paddingLeft':'28px'}),

    ],className='leftnavBar'),

    html.Div([
    html.H2('Crime clustering'),

    ],className='TituloSecciones'),

    dbc.Row([
        dbc.Col([card],style={'marginTop':'1.5rem'})
    ],style={'marginLeft':'236px','display':'flex','justifyContent':'center','marginBottom':'50px','flexWrap':'wrap'}),

    dbc.Row([
        dbc.Col([card1],style={'marginTop':'1rem', 'marginLeft':'0.5rem'}),
        dbc.Col([card2],style={'marginTop':'1rem', 'marginLeft':'0.5rem'})
    ],style={'marginLeft':'236px','display':'flex','justifyContent':'space-around','marginBottom':'50px','flexWrap':'wrap'})

])

@app.callback(
    Output(component_id='cluster-map', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value')]
)
def cluster_map(year_chosen):
    join1 = join[join.ano == year_chosen].groupby(['neigh']).cluster_predicted.agg(pd.Series.mode).reset_index(name = "cluster_predicted")
    join1.loc[-1]=[254,0]
    join1.cluster_predicted = join1.cluster_predicted.apply(lambda x:np.max(x))
    join1['cluster_predicted']=join1['cluster_predicted'].astype(int)
    fig = px.choropleth_mapbox(join1, geojson=cell, locations='neigh', color='cluster_predicted',
                               color_continuous_scale="Viridis",
                               mapbox_style="carto-positron",
                               zoom=12, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output(component_id='crime_category', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value')]
)
def crime_category_by_cluster(year_chosen):
    stack_cluster= cluster[cluster.ano == year_chosen].groupby(["cluster_predicted","categ_crimen"]).size().reset_index()
    stack_cluster["Proportion"] = cluster[cluster.ano == year_chosen].groupby(["cluster_predicted","categ_crimen"]).size().groupby(level=0).apply(lambda x:100 *x/float(x.sum())).values
    stack_cluster.rename(columns={0:"count","cluster_predicted":"cluster","categ_crimen":"Crime Category"},inplace=True)
    fig= px.bar(stack_cluster,x="cluster",y="count",color="Crime Category",barmode="stack")
    return fig

@app.callback(
    Output(component_id='comuna_by_cluster', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value')]
)
def comuna_by_cluster(year_chosen):
    stack_comunas = cluster[cluster.ano == year_chosen].groupby(["nom_comuna","cluster_predicted"]).size().reset_index()
    stack_comunas["Proportion"] = cluster[cluster.ano == year_chosen].groupby(["nom_comuna","cluster_predicted"]).size().groupby(level=0).apply(lambda x:100 *x/float(x.sum())).values
    stack_comunas.rename(columns={0:"count","cluster_predicted":"cluster","nom_comuna":"comuna"},inplace=True)
    fig= px.bar(stack_comunas,x="comuna",y="count",color="cluster",barmode="stack",
                color_continuous_scale="viridis")
    return fig