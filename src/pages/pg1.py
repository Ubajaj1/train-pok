import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/',name='HOME')

#df = pd.read_csv('pokedex.csv')


layout = html.Div(
    [
        dbc.Row(
            [
             html.H3("Pokemon Trainer is a person who catches, "
                       "trains, cares for, and battles with Pokemon.",className="text-wrap", style={'textAlign':'left'})

            ]
                ),
        dbc.Row(
            [
                html.P("Follow these simple steps to become a Pokemon Trainer - ",className="fw-bold text-primary", style={'fontSize':22, 'textAlign':'left'})

                    ]
                ),
        dbc.Row(
            [
                html.P("1. Catch'em all ",className="fw-bold", style={'fontSize':18, 'textAlign':'left'})

                    ]
                ),
        dbc.Row(
            [
                html.P("2. Take your Pokemon to Battle ",className="fw-bold", style={'fontSize':18, 'textAlign':'left'})

                    ]
                ),
        dbc.Row(
            [
                html.P("3. Care for your Pokemon till it evolves",className="fw-bold", style={'fontSize':18, 'textAlign':'left'})

                    ]
                ),
        dbc.Row(
            [
                html.P("4. Create your own Pokemon",className="fw-bold", style={'fontSize':18, 'textAlign':'left'})

                    ]
                ),
        html.Hr(),
        dbc.Col([
        dbc.Row(
            [
                html.Iframe( width="560", height="315", src="https://www.youtube.com/embed/FlZoiCfegEo?si=b6Vbp-3CM6KZVwDd" ,title="YouTube video player", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share")


                    ]
                )],width=10),
        html.Hr()

    ])
