# import dash_core_components as dcc
from datetime import date
from dash import dcc
from dash import html

from shapely import wkt                     # Geometry manipulation
from shapely.geometry import Polygon, Point
from dash.dependencies import Input, Output

import geopandas as gpd                     # Spatial data manipulation
import plotly.express as px
import pandas as pd
from app import app
import numpy as np
from sqlalchemy import create_engine, text

import dash_bootstrap_components as dbc

import warnings
warnings.filterwarnings("ignore")

DB_USERNAME = 'postgres' # Replace with the username you just created
DB_PASSWORD = 'Team227pry_' # Replace with the password you just created

engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@ds4a-team227-test.cqkc95x5yyj2.us-east-1.rds.amazonaws.com/crimen_bga', max_overflow=20)

cols = [
        "nom_comuna",
        "conducta",
        "fecha",
        "fecha_mes",
        "movil_agresor",
        "movil_victima",
        "categ_crimen",
        "dia_semana",
        "orden",
        "longitud",
        "latitud",
    ]

df = pd.read_sql_table("crimen_base_ex",engine,columns=cols)

df['fechaconvert'] = pd.to_datetime(df['fecha'], format="%m/%d/%Y")

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



card = dbc.Card(
    dbc.CardBody(
        [
           html.H4("Title", id="card-title"),
             html.H2("100", id="card-value"),
            html.P("Description", id="card-description")
       ]
    )
 )

card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Top macrocategories of crime", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-barplot', figure={},style={'width':'700px'}),

        ]
    ),
    style={"width": "100%"},class_name='card border-primary',
)

carddoble = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Spatial distribution of crime", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='mapa', figure={},style={'width':'700px','height':'1000px'}),

        ]
    ),
    style={"width": "100%","height": "100%"},class_name='card border-primary',
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Total of crimes ocurred in Bucaramanga by month", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-time-serie', figure={},style={'width':'700px'}),

        ]
    ),
    style={"width": "100%",'marginTop':'1.5rem'},class_name='card border-primary',
)


card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Parallel categories victim/attacker transportation", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-paralell', figure={},style={'width':'700px'}),

        ]
    ),
    style={"width": "100%"},class_name='card border-primary',
)



card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Distribution of crime over day of week normalized", className="card-title",style={'textAlign':'center'}),
            dcc.Graph(id='my-heat-map', figure={},style={'width':'700px'}),
        ]
    ),
    style={"width": "100%"},class_name='card border-primary',
)

layout = html.Div([

    html.Div([

        html.Div(
            html.Span('Crime counter',
                      style={'fontFamily': 'Inter','fontStyle': 'normal', 'fontWeight': '400','fontSize': '20px', 'lineHeight': '24px', 'color': '#FFFFFF'}),
            className='CrimeCounterTitle'),
        html.Div([
            html.Span(children={},className='crimeCounterNumber',id='CrimeCountNumber'),
            html.Img(src=app.get_asset_url('imagenes/ExtraIcons/IconStatistics.png'),style={'padding':'5px'})
        ],className='crimeCounter'),

        html.Div([

             html.Div([
                html.Span('Date',className='leftnavBarInputFont'),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2020, 9, 19),
                #initial_visible_month=date(2017, 8, 5),
                start_date=date(2010,1,1),
                end_date=date(2021,12,31),
                with_portal=True,
                style={'width':'180px','zIndex':'100'},
                ),
            ]),


            html.Div([
             html.Span("Neighborhood",className='leftnavBarInputFont'),
            dcc.Dropdown(options=[{'label': 'All', 'value': 'All'}]+[{'label': str(x), 'value': str(x)} for x in list(df.nom_comuna.unique())],id='nomComuna-dropdown',style={'width':'180px'}, clearable=False,
                persistence=True, persistence_type='local',value='All'),                
            ],style={'paddingTop':'10px'}),

            html.Div([
             html.Span("Criminal offense",className='leftnavBarInputFont'),
            dcc.Dropdown(options=[{'label': 'All', 'value': 'All'}]+[{'label': str(x), 'value': str(x)} for x in list(df.conducta.unique())], id='nomConducta-dropdown',style={'width':'180px',"display": "inline-block"}, clearable=False,
                persistence=True, persistence_type='local',optionHeight=100,value='All'),                 
            ],style={'paddingTop':'10px'}),

        
        
        ],style={'top':'300px','position':'absolute','paddingLeft':'28px'}),

        

    ],className='leftnavBar'),

    html.Div([
        html.H2('Crime statistics'),
    ],className='TituloSecciones'),

    dbc.Row([
       dbc.Col([carddoble],style={'marginTop':'1.5rem'}), dbc.Col([card1,card2],style={'marginTop':'1.5rem'}), dbc.Col([card3],style={'marginTop':'1.5rem'}),dbc.Col([card4],style={'marginTop':'1.5rem'}),
    ],style={'marginLeft':'300px','display':'flex','justifyContent':'space-between','marginRight':'100px','flexWrap':'wrap','marginBottom':'50px'}),

])

@app.callback(
    Output(component_id='mapa', component_property='figure'),
    [Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date'),
     Input(component_id='nomComuna-dropdown', component_property='value'),
     Input(component_id='nomConducta-dropdown', component_property='value')]
)
def display_value(start_date,end_date,comuna,conducta):
    if  (comuna=='All') & (conducta=='All'):
        join1 = join[(join['fechaconvert'] <= end_date) & (join['fechaconvert'] >= start_date)]
        join1.reset_index(inplace=True)
    elif conducta=='All':
        join1 = join[(join['nom_comuna'] == comuna) & (join['fechaconvert'] <= end_date) & (join['fechaconvert'] >= start_date)]
        join1.reset_index(inplace=True)
    elif comuna=='All':
        join1 = join[(join['conducta'] == conducta) & (join['fechaconvert'] <= end_date) & (join['fechaconvert'] >= start_date)]
        join1.reset_index(inplace=True)
    else:
        join1 = join[(join['nom_comuna'] == comuna) & (join['conducta'] == conducta) & (join['fechaconvert'] <= end_date) & (join['fechaconvert'] >= start_date)]
        join1.reset_index(inplace=True)

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


## Barplot frequency macro categories

@app.callback(
    Output(component_id='my-barplot', component_property='figure'),
    [Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date'),
     Input(component_id='nomComuna-dropdown', component_property='value'),
     Input(component_id='nomConducta-dropdown', component_property='value')])
def display_barplot(start_date,end_date,comuna,conducta):
    if comuna=='All':
        dfg_fltrd = df[(df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    else:
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)    

    fig = px.bar(dfg_fltrd.categ_crimen.value_counts().sort_values(ascending=True).head(10), orientation="h",
                  color_discrete_sequence=px.colors.qualitative.Bold).update_layout(
        xaxis_title="Frequency", yaxis_title="Crime Macro-Category", title_x=0.5,
        template="simple_white")

    return fig



## Month Time serie of crime
@app.callback(
    Output(component_id='my-time-serie', component_property='figure'),
    [Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date'),
     Input(component_id='nomComuna-dropdown', component_property='value'),
     Input(component_id='nomConducta-dropdown', component_property='value')])

def display_ts(start_date,end_date,comuna,conducta):
    if  (comuna=='All') & (conducta=='All'):
        dfg_fltrd = df[(df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif conducta=='All':
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif comuna=='All':
        dfg_fltrd = df[(df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    else:
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)




    crimen_neto_mes = dfg_fltrd.groupby(["fecha_mes"])["orden"].count().reset_index()
    crimen_neto_mes["fecha_mes"] = crimen_neto_mes["fecha_mes"].astype("str")
    crimen_neto_mes["fecha_mes"] = pd.to_datetime(crimen_neto_mes["fecha_mes"])

    crimen_neto_mes.rename(columns={'fecha_mes': 'Month', 'orden': 'Quantity'}, inplace=True)

    fig = px.line(crimen_neto_mes, x="Month", y="Quantity").update_layout(
        title_x=0.5
    )

    return fig

## Paralell coordinates of weapons

@app.callback(
    Output(component_id='my-paralell', component_property='figure'),
    [Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date'),
     Input(component_id='nomComuna-dropdown', component_property='value'),
     Input(component_id='nomConducta-dropdown', component_property='value')])

def display_paralell(start_date, end_date, comuna, conducta):
    if  (comuna=='All') & (conducta=='All'):
        dfg_fltrd = df[(df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif conducta=='All':
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif comuna=='All':
        dfg_fltrd = df[(df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    else:
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)


    fig = px.parallel_categories(dfg_fltrd, dimensions=['movil_agresor', 'movil_victima']).update_layout(
        title_x=0.5
    )

    return fig


## Heatmap day of week

@app.callback(
    Output(component_id='my-heat-map', component_property='figure'),
    [Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date'),
     Input(component_id='nomComuna-dropdown', component_property='value'),
     Input(component_id='nomConducta-dropdown', component_property='value')])
def display_dayheatmap(start_date, end_date, comuna, conducta):
    if  (comuna=='All') & (conducta=='All'):
        dfg_fltrd = df[(df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif conducta=='All':
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif comuna=='All':
        dfg_fltrd = df[(df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    else:
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    

    cross = pd.crosstab(dfg_fltrd["categ_crimen"], dfg_fltrd["dia_semana"], normalize="index")
    cross = np.round(np.divide(cross, 1) * 100, 2)
    fig = px.imshow(cross, text_auto=True)

    return fig

@app.callback(
    Output(component_id='CrimeCountNumber',component_property='children'),
    [Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date'),
     Input(component_id='nomComuna-dropdown', component_property='value'),
     Input(component_id='nomConducta-dropdown', component_property='value')]
    )
def displayNumber(start_date, end_date, comuna, conducta):
    if  (comuna=='All') & (conducta=='All'):
        dfg_fltrd = df[(df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif conducta=='All':
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    elif comuna=='All':
        dfg_fltrd = df[(df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)
    else:
        dfg_fltrd = df[(df['nom_comuna'] == comuna) & (df['conducta'] == conducta) & (df['fechaconvert'] <= end_date) & (df['fechaconvert'] >= start_date)]
        dfg_fltrd.reset_index(inplace=True)

    contador=dfg_fltrd['orden'].count()
    return contador













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
