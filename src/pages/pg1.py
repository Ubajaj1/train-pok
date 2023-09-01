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
             html.P("A Pokemon Trainer is a person who catches, "
                       "trains, cares for, and battles with Pokemon.",className="fw-bold text-wrap", style={'fontSize':20, 'textAlign':'left'})

            ]
                ),
        dbc.Row(
            [
                html.P("Follow these simple steps to become a Pokemon Trainer - ",className="fw-bold", style={'fontSize':15, 'textAlign':'left'})

                    ]
                ),
        dbc.Row(
            [
                html.P("Step 1: Click on the Catch Tab to Catch your favourite Pokemon ",className="fw-bold", style={'fontSize':15, 'textAlign':'left'})

                    ]
                ),
        dbc.Row(
            [
                html.P("Step 2: Jump to the Compare Tab to Compare your Pokemon with other Pokemons ",className="fw-bold", style={'fontSize':15, 'textAlign':'left'})

                    ]
                ),
        dbc.Row(
            [
                html.P("Step 3: Next look at how your Pokemon evolves",className="fw-bold", style={'fontSize':15, 'textAlign':'left'})

                    ]
                ),
        html.Hr(),
        dbc.Row(
            [
                html.P("Space to insert trainer graphs",className="fw-bold", style={'fontSize':35, 'textAlign':'left'})

                    ]
                ),
        html.Hr(),
        dbc.Row([

            html.Img(src='assets/trainer-image-male.png',style={'height':'20%', 'width':'20%','align':'center'})

    ]),
    ]
)
