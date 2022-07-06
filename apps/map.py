from dash import dcc
from dash import html
from app import app

from shapely import wkt                     # Geometry manipulation
from pysal.lib import weights               # Spatial weights
from pysal.explore import esda              # Exploratory Spatial analytics
from shapely.geometry import Point
from sqlalchemy import create_engine        # Sql manipulation
from dash.dependencies import Input, Output

import pandas as pd                         # Tabular data manipulation
import geopandas as gpd                     # Spatial data manipulation
import plotly.express as px
import dash_bootstrap_components as dbc

import warnings
warnings.filterwarnings("ignore")

DB_USERNAME = 'postgres' # Replace with the username you just created
DB_PASSWORD = 'Team227pry_' # Replace with the password you just created

engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@ds4a-team227-test.cqkc95x5yyj2.us-east-1.rds.amazonaws.com/crimen_bga', max_overflow=20)

cols = [
        "ano",
        "conducta",
        "fecha_mes",
        "orden",
        "longitud",
        "latitud",
    ]

df = pd.read_sql_table("crimen_base_ex_mod",engine,columns=cols)

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

def map_time():
    join1 = join.groupby(['fecha_mes', 'neigh']).orden.count().reset_index().rename({'orden':'crime_count'}, axis=1)

    fig = px.choropleth_mapbox(join1, geojson=cell, locations='neigh', color='crime_count',
                               color_continuous_scale="Viridis",
                               animation_frame='fecha_mes',
                               mapbox_style="carto-positron",
                               zoom=11, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )
    return fig

def database_set_up(db):
    count = db.groupby(['neigh']).count()['orden'].reset_index()
    count.rename(columns={'orden':'crim_by_neigh'}, inplace=True)
    db = db.merge(count).drop_duplicates(subset='neigh', keep="last")[['orden', 'neigh', 'geometry', 'crim_by_neigh']]

    # Generate W from the GeoDataFrame
    w = weights.distance.KNN.from_dataframe(db, k=8)

    # Row-standardization
    w.transform = 'R'

    # Spatial lag calculation
    db['w_crim_by_neigh'] = weights.spatial_lag.lag_spatial(w, db['crim_by_neigh'])

    # Standar deviation for crim_by_neigh
    db['crim_by_neigh_std'] = ( db['crim_by_neigh'] - db['crim_by_neigh'].mean())
    db['w_crim_by_neigh_std'] = ( db['w_crim_by_neigh'] - db['crim_by_neigh'].mean())

    lisa = esda.moran.Moran_Local(db['crim_by_neigh'], w)

    # Assign new column with local statistics on-the-fly
    db['Is'] = lisa.Is

    db['q'] = lisa.q
    db.q = db.q.map({1: 'HH', 2: 'LH', 3: 'LL', 4: 'HL'})

    labels = pd.Series(
        1 * (lisa.p_sim < 0.05), # Assign 1 if significant, 0 otherwise
        index=db.index           # Use the index in the original data
    )

    # Recode 1 to "Significant and 0 to "Non-significant"
    # Assign labels to `db` on the fly
    db['cl'] = labels.map({1: 'Significant', 0: 'Non-Significant'})

    db['q_sig'] = lisa.q * labels
    db.q_sig = db.q_sig.map({0: 'ns', 1: 'HH', 2: 'LH', 3: 'LL', 4: 'HL'})

    return db

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Crimes by month", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='time-map', figure=map_time(), className='graphtamañomapa', style={'width':'500px', 'height':'500px'})
        ]
    ),
    class_name='card border-primary cardtamañomapa',
)

card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Spatial lag", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='spatial_lag_std_plot-map', figure={},style={'width':'600px', 'height':'600px'}),
        ]
    ),
    style={"width": '100%'},class_name='card border-primary',
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Crimes distribution", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='moran_subplot1-map', figure={},style={'width':'600px', 'height':'600px'}),
        ]
    ),
    style={"width": '100%'},class_name='card border-primary',
)

card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Moran's I values by zone", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='moran_subplot2-map', figure={},style={'width':'600px', 'height':'600px'}),
        ]
    ),
    style={"width": '100%'},class_name='card border-primary',
)

card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Significance of crime zones", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='moran_subplot3-map', figure={},style={'width':'600px', 'height':'600px'}),
        ]
    ),
    style={"width": '100%'},class_name='card border-primary',
)

card5 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Significant moran's I values by zone", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='moran_subplot4-map', figure={},style={'width':'700px', 'height':'700px'}),
        ]
    ),
    style={"width": '100%'},class_name='card border-primary',
)

layout = html.Div([

    html.Div([

        html.Div(html.Span('Crime counter',style={'fontFamily': 'Inter','fontStyle': 'normal', 'fontWeight': '400','fontSize': '20px', 'lineHeight': '24px', 'color': '#FFFFFF'}),className='CrimeCounterTitle'),
        html.Div([
            html.Span('11.530',className='crimeCounterNumber'),
            html.Img(src=app.get_asset_url('imagenes/ExtraIcons/IconStatistics.png'),style={'padding':'5px'})

        ],className='crimeCounter'),

        html.Div([

            html.Div([
                html.Span('Year',className='leftnavBarInputFont'),
                dcc.Dropdown([2014, 2015, 2016, 2017, 2018, 2019], value=2014, id='year-dropdown',style={'width':'180px'}),
            ]),

            html.Div([
                html.Span('Type of crime',className='leftnavBarInputFont'),
                dcc.Dropdown(['HURTO A PERSONAS', 'LESIONES PERSONALES', 'VIOLENCIA INTRAFAMILIAR', 'HOMICIDIO'], value='HURTO A PERSONAS', id='crime-dropdown',style={'width':'180px'}),

            ],style={'paddingTop':'10px'}),

        ],style={'top':'300px','position':'absolute','paddingLeft':'28px'}),


    ],className='leftnavBar'),

    html.Div([
        html.H2('Spatial analysis'),

    ],className='TituloSecciones'),

    dbc.Row([
        dbc.Col([card],style={'marginTop':'1.5rem'})
    ],style={'marginLeft':'236px','display':'flex','justifyContent':'center','marginBottom':'50px','flexWrap':'wrap'}),

    dbc.Row([
        dbc.Col([card1],style={'marginTop':'1rem', 'marginLeft':'0.5rem'}),
        dbc.Col([card2],style={'marginTop':'1rem', 'marginLeft':'0.5rem'}),
    ],style={'marginLeft':'236px','display':'flex','justifyContent':'space-around','marginBottom':'50px','flexWrap':'wrap'}),

    dbc.Row([
        dbc.Col([card3],style={'marginTop':'1rem', 'marginLeft':'0.5rem'}),
        dbc.Col([card4],style={'marginTop':'1rem', 'marginLeft':'0.5rem'}),
    ],style={'marginLeft':'236px','display':'flex','justifyContent':'space-around','marginBottom':'50px','flexWrap':'wrap'}),

    dbc.Row([
        dbc.Col([card5],style={'marginTop':'1rem', 'marginLeft':'0.5rem'}),
    ],style={'marginLeft':'236px','display':'flex','justifyContent':'center','marginBottom':'50px','flexWrap':'wrap'}),
])

@app.callback(
    Output(component_id='spatial_lag_std_plot-map', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='crime-dropdown', component_property='value')]
)
def spatial_lag_std_plot(year_chosen, crime_chosen):
    db = join.copy()
    db = db[(db.conducta == crime_chosen) & (db.ano == year_chosen)]

    db = database_set_up(db)

    # Plot values
    fig = px.scatter(db, x="crim_by_neigh_std", y="w_crim_by_neigh_std", trendline="ols", title='Crime count by zone')

    # Add vertical and horizontal lines
    fig.add_hline(0)
    fig.add_vline(0)

    # Add text labels for each quadrant
    fig.add_annotation(x=db.crim_by_neigh_std.quantile(0.9), y=db.w_crim_by_neigh_std.quantile(0.9), text='HH', font=dict(size=20, color="red"))
    fig.add_annotation(x=db.crim_by_neigh_std.quantile(0.9), y=db.w_crim_by_neigh_std.quantile(0.1), text='HL', font=dict(size=20, color="red"))
    fig.add_annotation(x=db.crim_by_neigh_std.quantile(0.1), y=db.w_crim_by_neigh_std.quantile(0.9), text='LH', font=dict(size=20, color="red"))
    fig.add_annotation(x=db.crim_by_neigh_std.quantile(0.1), y=db.w_crim_by_neigh_std.quantile(0.1), text='LL', font=dict(size=20, color="red"))

    return fig

@app.callback(
    Output(component_id='moran_subplot1-map', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='crime-dropdown', component_property='value')]
)
def moran_subplot1(year_chosen, crime_chosen):
    db = join.copy()
    db = db[(db.conducta == crime_chosen) & (db.ano == year_chosen)]

    db = database_set_up(db)

    fig = px.choropleth_mapbox(db, geojson=cell, locations='neigh', color='Is',
                               color_continuous_scale=[(0.00, "blue"),   (0.045, "blue"),
                                                       (0.045, "pink"),   (0.06, "pink"),
                                                       (0.06, "purple"),(0.08, "purple"),
                                                       (0.08, "orange"), (0.10, "orange"),
                                                       (0.10, "yellow"), (1.00, "yellow")],
                               mapbox_style="carto-positron",
                               zoom=11, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )
    return fig

@app.callback(
    Output(component_id='moran_subplot2-map', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='crime-dropdown', component_property='value')]
)
def moran_subplot2(year_chosen, crime_chosen):
    db = join.copy()
    db = db[(db.conducta == crime_chosen) & (db.ano == year_chosen)]

    db = database_set_up(db)

    fig = px.choropleth_mapbox(db, geojson=cell, locations='neigh', color='q',
                               color_discrete_map={'HH':'#d7191c', 'LH':'#abd9e9','LL':'#2c7bb6','HL':'#fdae61'},
                               mapbox_style="carto-positron",
                               zoom=11, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )
    return fig

@app.callback(
    Output(component_id='moran_subplot3-map', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='crime-dropdown', component_property='value')]
)
def moran_subplot3(year_chosen, crime_chosen):
    db = join.copy()
    db = db[(db.conducta == crime_chosen) & (db.ano == year_chosen)]

    db = database_set_up(db)

    fig = px.choropleth_mapbox(db, geojson=cell, locations='neigh', color='cl',
                               mapbox_style="carto-positron",
                               zoom=11, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )
    return fig

@app.callback(
    Output(component_id='moran_subplot4-map', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='crime-dropdown', component_property='value')]
)
def moran_subplot4(year_chosen, crime_chosen):
    db = join.copy()
    db = db[(db.conducta == crime_chosen) & (db.ano == year_chosen)]

    db = database_set_up(db)

    fig = px.choropleth_mapbox(db, geojson=cell, locations='neigh', color='q_sig',
                               color_discrete_map={'HH':'#d7191c', 'LH':'#abd9e9','LL':'#2c7bb6','HL':'#fdae61', 'ns': 'lightgrey'},
                               mapbox_style="carto-positron",
                               zoom=11, center = {"lat": 7.12539, "lon": -73.1198},
                               opacity=0.5,
                               labels={'unemp':'unemployment rate'}
                               )
    return fig
