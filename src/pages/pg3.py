import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash_daq as daq
import plotly.graph_objs as go
import os
import pathlib
from pathlib import Path


dash.register_page(__name__, name='COMPARE')

full_path = os.path.abspath(__file__)
#print(os.path.abspath(__file__))
parent_folder = Path(full_path).parents[2]
#PATH = pathlib.Path(__file__).parent
#print(PATH)
DATA_PATH = parent_folder.joinpath("src/data").resolve()
IMAGE_PATH= parent_folder.joinpath("src").resolve()


df = pd.read_csv(DATA_PATH.joinpath('pokedex.csv'))
df = df.drop('Unnamed: 0', axis=1)

df_images = pd.read_excel(DATA_PATH.joinpath('pokedex_images_subset.xlsx'))
df_images = df_images.drop('Unnamed: 0', axis=1)

pokemon_data = pd.merge(df, df_images, on=['pokedex_number', 'name'], how='left')


os.chdir(IMAGE_PATH)
# Layout
layout = dbc.Container([
    html.H1("Pokemon Comparison"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pokemon1',
                options=[{'label': name, 'value': name} for name in pokemon_data['name']],
                value=pokemon_data['name'][0]  # Default value
            ),
            dbc.Card(id='pokemon1-card', className="mt-4", style={'width': '30rem'})
        ], width=5),  # First column for the first dropdown and image

        dbc.Col([
            dcc.Dropdown(
                id='pokemon2',
                options=[{'label': name, 'value': name} for name in pokemon_data['name']],
                value=pokemon_data['name'][1]  # Default value
            ),
            dbc.Card(id='pokemon2-card', className="mt-4", style={'width': '30rem'}),
        ], width=5),  # Second column for the second dropdown and image
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                id='points-card-1',
                className="mt-4",
                style={'width': '18rem'}
            )
        ], width=3),
        dbc.Col([
            dbc.Card(
                id='catch-rate-pokemon1-card',
                className="mt-4",
                style={'width': '10rem'}
            )
        ], width=2),
        dbc.Col([
            dbc.Card(
                id='points-card-2',
                className="mt-4",
                style={'width': '18rem'}
            )
        ], width=3),
        dbc.Col([
            dbc.Card(
                id='friendship-rate-pokemon2-card',
                className="mt-4",
                style={'width': '10rem'}
            )
        ], width=2),

    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                id='speed-stats-card',
                className="mt-4",
                style={'width': '60rem'}
            )
        ], width=10),

    ]),
])


@callback(
    [Output('pokemon1-card', 'children'),
     Output('pokemon2-card', 'children'),
     Output('points-card-1', 'children'),
     Output('points-card-2', 'children'),
     Output('speed-stats-card', 'children'),
     Output('catch-rate-pokemon1-card', 'children'),
     Output('friendship-rate-pokemon2-card', 'children')],
    [Input('pokemon1', 'value'),
     Input('pokemon2', 'value')]
)
def update_pokemon_images(selected_pokemon1, selected_pokemon2):
    card1 = pokemon_data[pokemon_data['name'] == selected_pokemon1]
    # card1 =  data_pokemon1.to_dict('records')
    card2 = pokemon_data[pokemon_data['name'] == selected_pokemon2]
    # card2 = data_pokemon2.to_dict('records')
    height_style = {'color': 'green'}
    weight_style = {'color': 'blue'}

    card1_content = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src="assets/images/" + card1['name_split'] + ".png", top=True,
                            className="img-fluid rounded-start",
                        ),
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.P(f"{card1['name'].values[0]}", style=height_style),
                                html.H5("Height (M)", className='card-title'),
                                html.P(f"{card1['height_m'].values[0]}", style=height_style),
                                html.H5("Weight (KG)", className='card-title'),
                                html.P(f"{card1['weight_kg'].values[0]}", style=weight_style),
                            ]
                        ),
                    ),
                ],
            )
        ],
    )
    card2_content = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src="assets/images/" + card2['name_split'] + ".png", top=True,
                            className="img-fluid rounded-start",
                        ),
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.P(f"{card2['name'].values[0]}", style=height_style),
                                html.H5("Height (M)", className='card-title'),
                                html.P(f"{card2['height_m'].values[0]}", style=height_style),
                                html.H5("Weight (KG)", className='card-title'),
                                html.P(f"{card2['weight_kg'].values[0]}", style=weight_style),
                            ]
                        ),
                    ),
                ],
            )
        ],
    )
    points_card1_content = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Total Points", className='card-title'),
                dcc.Graph(
                    id='points-gauge-1',
                    config={'displayModeBar': False},
                    style={'height': '150px'},
                    figure={
                        'data': [
                            go.Indicator(
                                mode="number+gauge",
                                value=card1['total_points'].values[0],
                                domain={'x': [0, 1], 'y': [0, 1]},
                                gauge={
                                    'axis': {
                                        'visible': True,
                                        'range': [0, 1125],  # Fixed axis range
                                        'dtick': 225,  # Specify the tick interval
                                    },
                                    'bar': {'color': "blue"},
                                    'steps': [
                                        {'range': [0, 1125], 'color': "cyan"},
                                        {'range': [1125, 1125], 'color': "lightblue"},
                                        {'range': [1125, 1125], 'color': "blue"},
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': card1['total_points'].values[0]
                                    }
                                },
                                number={'valueformat': '.0f', 'font': {'size': 24}},
                            )
                        ],
                        'layout': go.Layout(
                            margin={'l': 20, 'r': 30, 'b': 30, 't': 30},
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                    }
                ),
            ]
        )
    )

    catch_rate_pokemon1 = card1['catch_rate'].values[0]
    catch_rate_pokemon2 = card2['catch_rate'].values[0]

    friendship_rate_pokemon1 = card1['base_friendship'].values[0]
    friendship_rate_pokemon2 = card2['base_friendship'].values[0]

    catch_rate_pokemon1_card_content = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Catch Rate", className='card-title'),
                html.P(f"{catch_rate_pokemon1}", style={'color': 'green'}),
                html.H5("Friendship", className='card-title'),
                html.P(f"{friendship_rate_pokemon1}", style={'color': 'green'}),
            ]
        )
    )

    friendship_rate_pokemon2_card_content = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Catch Rate", className='card-title'),
                html.P(f"{catch_rate_pokemon2}", style={'color': 'green'}),
                html.H5("Friendship", className='card-title'),
                html.P(f"{friendship_rate_pokemon2}", style={'color': 'green'}),
            ]
        )
    )

    stats_labels = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    stats_pokemon1 = [card1[label].values[0] for label in stats_labels]
    stats_pokemon2 = [card2[label].values[0] for label in stats_labels]

    # Create a grouped bar chart for the stats
    trace1 = go.Bar(
        x=stats_labels,
        y=stats_pokemon1,
        name=selected_pokemon1,
        marker={'color': 'rgba(55, 128, 191, 0.7)'},
    )
    trace2 = go.Bar(
        x=stats_labels,
        y=stats_pokemon2,
        name=selected_pokemon2,
        marker={'color': 'rgba(219, 64, 82, 0.7)'},
    )

    stats_fig = {
        'data': [trace1, trace2],
        'layout': go.Layout(
            barmode='group',
            title='Stats Comparison',
            xaxis={'title': 'Stats'},
            yaxis={'title': 'Value'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        ),
    }

    stats_card_content = dbc.Card(
        dbc.CardBody(
            [
                # html.H5("Stats Comparison", className='card-title'),
                dcc.Graph(
                    id='stats-fig-1',
                    config={'displayModeBar': False},
                    style={'height': '300px'},
                    figure=stats_fig
                ),
            ]
        )
    )
    points_card2_content = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Total Points", className='card-title'),
                dcc.Graph(
                    id='points-gauge-1',
                    config={'displayModeBar': False},
                    style={'height': '150px'},
                    figure={
                        'data': [
                            go.Indicator(
                                mode="number+gauge",
                                value=card2['total_points'].values[0],
                                domain={'x': [0, 1], 'y': [0, 1]},
                                gauge={
                                    'axis': {
                                        'visible': True,
                                        'range': [0, 1125],  # Fixed axis range
                                        'dtick': 225,  # Specify the tick interval
                                    },
                                    'bar': {'color': "blue"},
                                    'steps': [
                                        {'range': [0, 1125], 'color': "cyan"},
                                        {'range': [1125, 1125], 'color': "lightblue"},
                                        {'range': [1125, 1125], 'color': "blue"},
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': card2['total_points'].values[0]
                                    }
                                },
                                number={'valueformat': '.0f', 'font': {'size': 24}},
                            )
                        ],
                        'layout': go.Layout(
                            margin={'l': 20, 'r': 30, 'b': 30, 't': 30},
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                    }
                ),
            ]
        )
    )
    return (card1_content,
            card2_content,
            points_card1_content,
            points_card2_content,
            stats_card_content,
            catch_rate_pokemon1_card_content,
            friendship_rate_pokemon2_card_content)


