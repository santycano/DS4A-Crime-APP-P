
from dash import dcc

from dash import html,Dash

from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from apps import statistics, map, preditor, inicio  
# app = dash.Dash(__name__)
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Header([
        dcc.Link(html.Img(src=app.get_asset_url('imagenes/ds4a.png'),className="ds4aimage"),href='/apps/indice'),
        html.Img(src=app.get_asset_url('imagenes/imageCstatisctis.png')),
        dcc.Link('Crime statistics', href='/apps/statistics',className="likns"),
        html.Img(src=app.get_asset_url('imagenes/imageCmap.png')),
        dcc.Link('Spatial analysis', href='/apps/map',className="likns"),
        html.Img(src=app.get_asset_url('imagenes/imageCpredictor.png')),
        dcc.Link('Crime clustering', href='/apps/preditor',className="likns"),
    ], className="rowfld",style={'backgroundColor': '#FBF336', 'height': '120px','width':'100%','position':'fixed','top':'0','zIndex':'100'}),
    html.Div(id='page-content', children=[],style={'marginTop':'170px'})
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
    app.run_server(debug=False)