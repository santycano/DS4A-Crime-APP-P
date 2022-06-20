# import dash_core_components as dcc
from turtle import width
from dash import dcc
import dash_bootstrap_components as dbc
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import statistics, map, preditor, inicio  




app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Header([
        dcc.Link(html.Img(src=app.get_asset_url('imagenes/ds4a.png'),className="ds4aimage"),href='/apps/indice'),
        html.Img(src=app.get_asset_url('imagenes/imageCstatisctis.png')),
        dcc.Link('Crime statistics', href='/apps/statistics',className="likns"),
        html.Img(src=app.get_asset_url('imagenes/imageCmap.png')),
        dcc.Link('Crime map', href='/apps/map',className="likns"),
        html.Img(src=app.get_asset_url('imagenes/imageCpredictor.png')),
        dcc.Link('Crime predictor', href='/apps/preditor',className="likns"),
    ], className="rowfld",style={'backgroundColor': '#FBF336', 'height': '120px','width':'100%'}),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/statistics':
        return statistics.layout
    if pathname == '/apps/map':
        return map.layout
    if pathname == '/apps/preditor':
        return preditor.layout
    else:
        return inicio.layout


if __name__ == '__main__':
    app.run_server(debug=True)