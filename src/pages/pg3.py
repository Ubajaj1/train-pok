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
    html.H1("Select the Pokemons that you want to compare"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pokemon1',
                className="fw-bold text-dark",
                options=[{'label': name, 'value': name} for name in pokemon_data['name']],
                value=pokemon_data['name'][0]  # Default value
            ),
            dbc.Card(id='pokemon1-card', className="mt-4", style={'width': '30rem',"backgroundColor":'#0e2535'})
        ], width=5),  # First column for the first dropdown and image

        dbc.Col([
            dcc.Dropdown(
                id='pokemon2',
                className="fw-bold text-dark",
                options=[{'label': name, 'value': name} for name in pokemon_data['name']],
                value=pokemon_data['name'][1]  # Default value
            ),
            dbc.Card(id='pokemon2-card', className="mt-4", style={'width': '30rem',"backgroundColor":'#0e2535'}),
        ], width=5),  # Second column for the second dropdown and image
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                id='points-card-1',
                className="mt-4",
                style={"border": "none",'width': '18rem', "backgroundColor":'#0e2535'}
            )
        ], width=3),
        dbc.Col([
            dbc.Card(
                id='catch-rate-pokemon1-card',
                className="mt-4",
                style={'width': '12rem',"backgroundColor":'#0e2535'}
            )
        ], width=2),
        dbc.Col([
            dbc.Card(
                id='points-card-2',
                className="mt-4",
                style={'width': '18rem',"backgroundColor":'#0e2535'}
            )
        ], width=3),
        dbc.Col([
            dbc.Card(
                id='friendship-rate-pokemon2-card',
                className="mt-4",
                style={'width': '12rem',"backgroundColor":'#0e2535'}
            )
        ], width=2),

    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                id='speed-stats-card',
                className="mt-4",
                style={'width': '60rem',"backgroundColor":'#0e2535'}
            )
        ], style={"backgroundColor":'#0e2535'}),

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
    height_style = {'color': 'white'}
    weight_style = {'color': 'white'}

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
                                html.P(f"{card1['name'].values[0]}", className = 'text-primary', style=height_style),
                                html.P("HEIGHT (m):  " + f"{card1['height_m'].values[0]}", className='card-title', style=height_style),
                                html.P("WEIGHT (kg): "+ f"{card1['weight_kg'].values[0]}", style=weight_style),
                            ]
                        ),
                    ),
                ],
            )
        ], style={"backgroundColor":'#0e2535'}
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
                                html.P(f"{card2['name'].values[0]}", className = 'text-primary', style=height_style),
                                html.P("HEIGHT (m): "+f"{card2['height_m'].values[0]}", style=height_style),
                                html.P("WEIGHT (kg): "+f"{card2['weight_kg'].values[0]}", style=weight_style),
                            ]
                        ),
                    ),
                ],
            )
        ],style={"backgroundColor":'#0e2535'}
    )
    points_card1_content = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Total Points", className='text-warning'),
                dcc.Graph(
                    id='points-gauge-1',
                    config={'displayModeBar': False},
                    style={'height': '200px', "border": "none"},
                    figure={
                        'data': [
                            go.Indicator(
                                mode="number+gauge",
                                value=card1['total_points'].values[0],
                                domain={'x': [0, 1], 'y': [0, 1]},
                                gauge={
                                    'axis': {
                                        'visible': True,
                                        'range': [0, 1125],
                                        'dtick': 225,
                                        'tickfont': {"color":'white'}
                                    },
                                    'bar': {'color': "blue"},
                                    'steps': [
                                        {'range': [0, 1125], 'color': "white"},
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': card1['total_points'].values[0]
                                    }
                                },
                                number={'valueformat': '.0f', 'font': {'size': 24, 'color':'white'}},
                            )
                        ],
                        'layout': go.Layout(
                            margin={'l': 20, 'r': 30, 'b': 30, 't': 30},
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                    }
                ),
            ],style={"border": "none", "backgroundColor":'#0e2535'}
        )
    )

    catch_rate_pokemon1 = card1['catch_rate'].values[0]
    catch_rate_pokemon2 = card2['catch_rate'].values[0]

    friendship_rate_pokemon1 = card1['base_friendship'].values[0]
    friendship_rate_pokemon2 = card2['base_friendship'].values[0]

    catch_rate_pokemon1_card_content = dbc.Card(
        dbc.CardBody(
            [
                html.P("HP - "+ str(int(card1['hp'].values[0])), style={'color': 'white'}),
                html.P("Attack - " + str(int(card1['attack'].values[0])), style={'color': 'white'}),
                html.P("Defense - " + str(int(card1['defense'].values[0])), style={'color': 'white'}),
                html.P("Special Attack - " + str(int(card1['sp_attack'].values[0])), style={'color': 'white'}),
                html.P("Special Defense - " + str(int(card1['sp_defense'].values[0])), style={'color': 'white'}),
                html.P("Speed - " + str(int(card1['speed'].values[0])), style={'color': 'white'})
            ],style={"backgroundColor":'#0e2535','height': '262px'}
        )
    )

    friendship_rate_pokemon2_card_content = dbc.Card(
        dbc.CardBody(
            [
                html.P("HP - " + str(int(card2['hp'].values[0])), style={'color': 'white'}),
                html.P("Attack - " + str(int(card2['attack'].values[0])), style={'color': 'white'}),
                html.P("Defense - " + str(int(card2['defense'].values[0])), style={'color': 'white'}),
                html.P("Special Attack - " + str(int(card2['sp_attack'].values[0])), style={'color': 'white'}),
                html.P("Special Defense - " + str(int(card2['sp_defense'].values[0])), style={'color': 'white'}),
                html.P("Speed - " + str(int(card2['speed'].values[0])), style={'color': 'white'})
            ], style={"backgroundColor":'#0e2535','height': '262px'}
        )
    )

    stats_labels = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    stats_pokemon1 = [card1[label].values[0] for label in stats_labels]
    stats_pokemon2 = [card2[label].values[0] for label in stats_labels]
    radar_chart_data = [
       go.Scatterpolar(
        r=stats_pokemon1,
        theta=stats_labels,
        fill = 'toself',
        name=selected_pokemon1,
        textfont={'color': 'white'},
        #marker=dict(color='white')
        texttemplate="plotly_dark"
        ),
       go.Scatterpolar(
        r=stats_pokemon2,
        theta=stats_labels,
        fill='toself',
        name=selected_pokemon2,
        textfont={'color': 'white'},
        #marker=dict(color='white')
        texttemplate="plotly_dark"
    ),]
    radar_chart_layout = go.Layout(
        polar=dict(
            radialaxis=dict(visible=True)
            #bgcolor = 'white'
        ),
        showlegend=True,
        title='Stats Comparison',
        paper_bgcolor='#0e2535',
        font=dict(color='white'),
        template="plotly_dark"

        #template="plotly_dark"
        #textfont=dict(color='white')
    )
    stats_card_content = dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id='stats-radar-chart-pokemon',
                    config={'displayModeBar': False},
                    style={"backgroundColor":'#0e2535'},
                    #style={'backgroundColor':'#0e2535'},
                    figure={'data': radar_chart_data, 'layout': radar_chart_layout},
                ),
            ], style={"border": "none",'backgroundColor':'#0e2535'}
        )
    )
    points_card2_content = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Total Points", className='text-warning'),
                dcc.Graph(
                    id='points-gauge-1',
                    config={'displayModeBar': False},
                    style={'height': '200px',"backgroundColor":'#0e2535'},
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
                                        'dtick': 225,
                                        'tickfont': {"color": 'white'}
                                        # Specify the tick interval
                                    },
                                    'bar': {'color': "blue"},
                                    'steps': [
                                        {'range': [0, 1125], 'color': "white"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': card2['total_points'].values[0]
                                    }
                                },
                                number={'valueformat': '.0f', 'font': {'size': 24, 'color':'white'}},
                            )
                        ],
                        'layout': go.Layout(
                            margin={'l': 20, 'r': 30, 'b': 30, 't': 30},
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                    }
                ),
            ],style={"backgroundColor":'#0e2535'}
        )
    )
    return (card1_content,
            card2_content,
            points_card1_content,
            points_card2_content,
            stats_card_content,
            catch_rate_pokemon1_card_content,
            friendship_rate_pokemon2_card_content)