# from turtle import width
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

layout = html.Div([
    html.H1('Bucaramanga Crime Predictor', style={"textAlign": "center"},className='Cindex'),
    html.Img(src=app.get_asset_url('imagenes/banner1-4.jpg'),width='90%', style={'display':'block','margin':'auto','height':'400px'} ),
    # html.Img(src=app.get_asset_url('imagenes/bannerInicio.png'),width='83%', style={'display':'block','margin':'auto','height':'400px'} ),
    html.P([f'The crime is a complex and multifactorial issue, then the figth against crime need ways to focus the actions with the end of be more effective and efficient to focus police actions but also to focus social policie that impact poverty, unemployment and other variables that boost inequality. The Bucaramanga crime predictor is a tool that have the objective of give an inter-temporal comprehension of crime that afford the understanding of prevalent clusters and the emerging crime hotspots by mean of:' 
        ,html.Br(),'- General EDA of the crime dynamic in the city of Bucaramanga',
        html.Br(),'- Spatial Cluster Analysis of crime',
        html.Br(),'- Zone profiler that show the potential probability of being affected by the most prevalent crimes according to characteristics of the citizen.',

], className='parrafo'),
    html.Iframe(src='https://www.youtube.com/embed/bDJXR5S8Bso',referrerPolicy='no-referrer',width='66%',height='683',title="YouTube video player",allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture", style={'display':'block','margin':'auto'} ),
    # html.Iframe(src='https://www.youtube.com/embed/b7qZPMqHnl4',referrerPolicy='no-referrer',width='66%',height='683',title="YouTube video player",allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture", style={'display':'block','margin':'auto'} ),
    html.Button('Go to dashboard',className='botonGoto'),
    html.H1('Bucaramanga Dataset', style={"textAlign": "center"},className='Cindex'),
    html.P(['This project was made using data from the following sources:',html.Br(),html.Br(),
    '- Colombia open data-Crimes in Bucaramanga from January 2010 to December 2021 ',
    html.Br(),
    html.A('https://www.datos.gov.co/Seguridad-y-Defensa/40-Delitos-en-Bucaramanga-enero-2010-a-diciembre-d/75fz-q98y',href='https://www.datos.gov.co/Seguridad-y-Defensa/40-Delitos-en-Bucaramanga-enero-2010-a-diciembre-d/75fz-q98y'),
    html.Br(),
    html.P(['- National Census of population and Household 2018-DANE-Geostatistical National Framework',html.Br(),html.A('https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/visor-descarga-geovisores/',href='https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/visor-descarga-geovisores/')]),
    

    ], className='parrafo'),
    html.H1('Team 227 members', style={"textAlign": "center"},className='Cindex'),
    html.Div([
        # Daniela Box
        html.Div([
            html.Img(src=app.get_asset_url('imagenes/TeamMembers/Daniela.png'), className='MembersPhothos'),
            html.Span('Daniela Beltran',className='MemebersName'),
            html.Div([
                html.Img(src=app.get_asset_url('imagenes/MailIcon.png'), width='50px',height='50px',style={'padding':'5%'}),
                html.Img(src=app.get_asset_url('imagenes/LinkedinIcon.png'), width='50px',height='50px',style={'padding':'5%'}),                
            ],style={'width':'100%','display':'flex','margin':'auto','justifyContent':'center','alignItems':'center'})
       ], style={'display':'flex','margin':'auto','flexWrap': 'wrap','width':'225px','justifyContent':'center','alignItems':'center'}),
        # Daniela Box

        # David Box
        html.Div([
            html.Img(src=app.get_asset_url('imagenes/TeamMembers/David.png'), className='MembersPhothos'),
            html.Span('David Rivera',className='MemebersName'),
            html.Div([
                html.Img(src=app.get_asset_url('imagenes/MailIcon.png'), width='50px',height='50px',style={'padding':'5%'}),
                html.Img(src=app.get_asset_url('imagenes/LinkedinIcon.png'), width='50px',height='50px',style={'padding':'5%'}),                
            ],style={'width':'100%','display':'flex','margin':'auto','justifyContent':'center','alignItems':'center'})
       ], style={'display':'flex','margin':'auto','flexWrap': 'wrap','width':'225px','justifyContent':'center','alignItems':'center'}),
        # David Box

        # Juan Box
        html.Div([
            html.Img(src=app.get_asset_url('imagenes/TeamMembers/Juan.png'), className='MembersPhothos'),
            html.Span('Juan Gutierrez',className='MemebersName'),
            html.Div([
                html.Img(src=app.get_asset_url('imagenes/MailIcon.png'), width='50px',height='50px',style={'padding':'5%'}),
                html.Img(src=app.get_asset_url('imagenes/LinkedinIcon.png'), width='50px',height='50px',style={'padding':'5%'}),                
            ],style={'width':'100%','display':'flex','margin':'auto','justifyContent':'center','alignItems':'center'})
       ], style={'display':'flex','margin':'auto','flexWrap': 'wrap','width':'225px','justifyContent':'center','alignItems':'center'}),
        # Juan Box

        # Carlos Arbelaez
       html.Div([
            html.Img(src=app.get_asset_url('imagenes/TeamMembers/Carlos.png'), className='MembersPhothos'),
            html.Span('Carlos Arbeláez',className='MemebersName'),
            html.Div([
                html.Img(src=app.get_asset_url('imagenes/MailIcon.png'), width='50px',height='50px',style={'padding':'5%'}),
                html.Img(src=app.get_asset_url('imagenes/LinkedinIcon.png'), width='50px',height='50px',style={'padding':'5%'}),                
            ],style={'width':'100%','display':'flex','margin':'auto','justifyContent':'center','alignItems':'center'})
       ], style={'display':'flex','margin':'auto','flexWrap': 'wrap','width':'225px','justifyContent':'center','alignItems':'center'}),
        # Carlos Arbelaez


        # Fabian Box
       html.Div([
            html.Img(src=app.get_asset_url('imagenes/TeamMembers/Fabian.png'), className='MembersPhothos'),
            html.Span('Fabián Ramos',className='MemebersName'),
            html.Div([
                html.Img(src=app.get_asset_url('imagenes/MailIcon.png'), width='50px',height='50px',style={'padding':'5%'}),
                html.Img(src=app.get_asset_url('imagenes/LinkedinIcon.png'), width='50px',height='50px',style={'padding':'5%'}),                
            ],style={'width':'100%','display':'flex','margin':'auto','justifyContent':'center','alignItems':'center'})
       ], style={'display':'flex','margin':'auto','flexWrap': 'wrap','width':'225px','justifyContent':'center','alignItems':'center'}),
        # Fabian Box

        # Josue Cano
       html.Div([
            html.Img(src=app.get_asset_url('imagenes/TeamMembers/Josue.png'), className='MembersPhothos'),
            html.Span('Josue Cano',className='MemebersName'),
            html.Div([
                html.Img(src=app.get_asset_url('imagenes/MailIcon.png'), width='50px',height='50px',style={'padding':'5%'}),
                html.Img(src=app.get_asset_url('imagenes/LinkedinIcon.png'), width='50px',height='50px',style={'padding':'5%'}),                
            ],style={'width':'100%','display':'flex','margin':'auto','justifyContent':'center','alignItems':'center'})
       ], style={'display':'flex','margin':'auto','flexWrap': 'wrap','width':'225px','justifyContent':'center','alignItems':'center'}),
        # Josue Cano


        # Nicolas Box
       html.Div([
            html.Img(src=app.get_asset_url('imagenes/TeamMembers/Nicolas.png'), className='MembersPhothos'),
            html.Span('Nicolas Galvan',className='MemebersName'),
            html.Div([
                html.Img(src=app.get_asset_url('imagenes/MailIcon.png'), width='50px',height='50px',style={'padding':'5%'}),
                html.Img(src=app.get_asset_url('imagenes/LinkedinIcon.png'), width='50px',height='50px',style={'padding':'5%'}),                
            ],style={'width':'100%','display':'flex','margin':'auto','justifyContent':'center','alignItems':'center'})
       ], style={'display':'flex','margin':'auto','flexWrap': 'wrap','width':'225px','justifyContent':'center','alignItems':'center'}),
        # Nicolas Box

    
    ], style={'display':'flex'},className='Bloquedefotos'),
    
    
    
    
    html.Div([
        html.Img(src=app.get_asset_url('imagenes/Footer/image 15.png')),
        html.Img(src=app.get_asset_url('imagenes/Footer/image 17.png')),
        html.Img(src=app.get_asset_url('imagenes/Footer/image 16.png')),
        
    ], style={'display':'flex',    'height': '90px', 'justifyContent': 'space-evenly','paddingTop':'40px'})


    
])
