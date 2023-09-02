import dash
from dash import dcc, html, callback, Output, Input, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import os
import pathlib
from pathlib import Path

dash.register_page(__name__, name='EVOLVE')

full_path = os.path.abspath(__file__)
#print(os.path.abspath(__file__))
parent_folder = Path(full_path).parents[2]
#print(parent_folder)
#PATH = pathlib.Path(__file__).parent
#print(PATH)
DATA_PATH = parent_folder.joinpath("src/data").resolve()
IMAGE_PATH= parent_folder.joinpath("src").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath('pokedex.csv'))
df_images = pd.read_excel(DATA_PATH.joinpath('pokedex_images_subset.xlsx'))
df_evolve = pd.read_excel(DATA_PATH.joinpath('Evolution_data_transposed.xlsx'))

# Merge data
newdf = pd.merge(df, df_evolve, how='left', left_on='name', right_on='Pokemon_name')
newdf = pd.merge(newdf, df_images, on=['pokedex_number', 'name'], how='left')

# Rename columns and fill missing values
newdf.rename(columns={'type_1': 'Primary Type', 'type_2': 'Secondary Type', 'pokedex_number': 'Pokedex Number', 'name': 'name',
                      'status': 'Status', 'generation': 'Generation', 'species': 'Species', 'total_points': 'Total Points',
                      'hp': 'Hp', 'catch_rate': 'Catch Rate', 'base_friendship': 'Base Friendship', 'catch_parameters': 'Catch Parameters',
                      'base_experience': 'Base Experience', 'growth_rate': 'Growth Rate', 'percentage_male': 'Male (%)'}, inplace=True)
newdf['link'] = newdf['link'].fillna(newdf['name'])
newdf['Pokemon_name'] = newdf['Pokemon_name'].fillna(newdf['name'])
newdf['Stage'] = newdf['Stage'].fillna('Stage_1')
newdf['rank'] = newdf['rank'].fillna(1)

newdf.sort_values(by=['link', 'rank'], ascending=[True, True], inplace=True)
newdf['Catch Rate'] = newdf['Catch Rate'].fillna(-1)
newdf['Base Friendship'] = newdf['Base Friendship'].fillna(-1)

# Layout
layout = html.Div([
    html.H3("Select a Pokemon to see its evolution"),
    dbc.Col([dcc.Dropdown(
        id='pokemon-dropdown',
        options=[{'label': name, 'value': name} for name in newdf['name'].unique()],
        value=newdf['name'].unique()[0],
        multi=False,
        style={'color': 'black'}
    )],width=6),
    html.Div(id='evolution-output'),
])

os.chdir(IMAGE_PATH)

# Define the callback to update the evolution output
@callback(
    Output('evolution-output', 'children'),
    Input('pokemon-dropdown', 'value')
)

def update_evolution_output(selected_pokemon):
    output = []

    pokemon_list = newdf[newdf['Pokemon_name'] == selected_pokemon]['link'].tolist()

    for i in pokemon_list:
        sample = newdf[newdf['link'] == i]  # Define sample DataFrame within the loop
        link_container = html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.P(f"Evolution Chain: {i}",className='text-primary fw-bold fs-2 text'),
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.CardImg(id='img-output', src='assets/images/' + sample.iloc[s]['name_split'] + ".png", top=True),
                                dbc.CardBody([
                                    html.H5(sample.iloc[s]['name'], className="card-title fw-bold text-warning", style={'font-size': '20px'}),
                                    html.P("Pokedex ID : " + str(sample.iloc[s]['Pokedex Number']), className="card-text fw-bold", style={'font-size': '16px'}),
                                    html.P("Status : " + sample.iloc[s]['Status'], className="card-text fw-bold",
                                           style={'font-size': '16px'}),
                                    html.P("Generation : " + str(sample.iloc[s]['Generation']), className="card-text fw-bold",
                                           style={'font-size': '16px'}),

                                ])
                            ])
                        ], style={"width": "18rem", "backgroundColor": '#0e2535', "font_size": "5px"})
                        for s in range(len(sample))
                    ], style={'display': 'flex'})
                ])
            ], style={'width': '900px', 'height': '500px', 'margin': '10px', 'background-color': '#0e2535'})
        ])
        output.append(link_container)

    return output
