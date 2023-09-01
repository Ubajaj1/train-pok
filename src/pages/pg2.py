import dash
from dash import dcc, html, callback, Output, Input, dash_table, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import os
import pathlib
from pathlib import Path

dash.register_page(__name__, name='CATCH')

# page 2 data
full_path = os.path.abspath(__file__)
#print(os.path.abspath(__file__))
parent_folder = Path(full_path).parents[2]
#PATH = pathlib.Path(__file__).parent
#print(PATH)
DATA_PATH = parent_folder.joinpath("src/data").resolve()
IMAGE_PATH= parent_folder.joinpath("src").resolve()



#dfg = pd.read_csv(DATA_PATH.joinpath("opsales.csv"))


df_1 = pd.read_csv(DATA_PATH.joinpath('pokedex.csv'))

df_1=df_1.drop('Unnamed: 0',axis=1)

df_images=pd.read_excel(DATA_PATH.joinpath('pokedex_images_subset.xlsx'))
df_images=df_images.drop('Unnamed: 0',axis=1)

df_location=pd.read_excel(DATA_PATH.joinpath('pokemon-locations-data.xlsx'))

df_1=pd.merge(df_1,df_location,on=['pokedex_number','name'],how='left')
df_1=pd.merge(df_1,df_images,on=['pokedex_number','name'],how='left')
#calculating the catch parameters
df_1['catch_parameters']=(df_1['total_points']*(1/3)+df_1['catch_rate']*(1/3)+df_1['base_friendship']*(1/3))
#sorting the values
df_1_sort=df_1.sort_values(by=['type_1','catch_parameters'], ascending=[True,False])
df_1_sort_type=pd.DataFrame()
for t in df_1_sort['type_1'].unique():
    type_df = df_1_sort[df_1_sort['type_1']==t]
    top_names = type_df.head(4)
    df_1_sort_type = pd.concat([df_1_sort_type, top_names])

df_1_sort_type = df_1_sort_type.rename(columns={'type_1':'Primary Type','type_2':'Secondary Type','pokedex_number':'Pokedex Number','name':'Name','status':'Status','generation':'Generation','species':'Species',
                              'total_points':'Total Points','hp':'Hp','catch_rate':'Catch Rate','base_friendship':'Base Friendship','catch_parameters':'Catch Parameters','base_experience':'Base Experience','growth_rate':'Growth Rate','percentage_male':'Male (%)'})

df_1_sort_type=df_1_sort_type.reset_index().drop(['index'],axis=1)
df_1_sort_type_subset=df_1_sort_type[['Name','Primary Type','Secondary Type','Base Experience','Growth Rate','Male (%)', 'Location','Region']]

dict_poke=df_1_sort_type.to_dict('records')

tooltip = html.Div(
    [
        html.P(
            [
                "I wonder what ",
                html.Span(
                    "floccinaucinihilipilification",
                    id="tooltip-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                ),
                " means?",
            ]
        ),
        dbc.Tooltip(
            "Noun: rare, "
            "the action or habit of estimating something as worthless.",
            target="tooltip-target",
        ),
    ]
)


os.chdir(IMAGE_PATH)
def make_card(dict_poke):
    poke_name=dict_poke['Name']
    return dbc.Card([

                        dbc.CardBody(
                                [   dbc.CardImg(id='img-output',src='assets/images/'+dict_poke['name_split']+ ".png", top=True),
                        dbc.CardBody(
                                 [
                                     html.H5(poke_name, className="card-title"),
                                     html.P("Pokedex ID : " + str(dict_poke['Pokedex Number']),className="card-text"
                                            ),
                                     html.P("Status : " + dict_poke['Status'],
                                     className="card-text"
                                                    ),
                                     html.P("Species : " + dict_poke['Species'],
                                            className="card-text"
                                            ),
                                     html.P("Generation : " + str(dict_poke['Generation']),
                                            className="card-text"
                                            ),
                                     html.P("Friendship : " + str(int(dict_poke['Base Friendship'])),
                                            className="card-text"
                                            ),
                                     html.P("Catch Rate : " + str(int(dict_poke['Catch Rate'])),
                                            className="card-text"
                                            ),
                                     html.P("Total Points : " + str(int(dict_poke['Total Points'])),
                                            className = "card-text"
                                             ),



                                 ]
                                    ),
                                ]   )
                    ],
                    style={"width": "18rem", "backgroundColor":'#0e2535'})
cards=html.Div()
buttons=html.Div()

layout = html.Div(
    [  dbc.Row([
            dbc.Col(
                [   html.P('Select the primary type of Pokemon that you want to catch', className='fix_label',  style={'color': 'white'}),
                    dcc.Dropdown(df_1_sort_type_subset['Primary Type'].unique(),id='type-choice', value='Grass',className='fw-bold',style={'color':'black'})
                ], width=6
            )
        ]),

        html.Br(),
        html.P(['These are the Top 4 Pokemons based on your selection'], className='fix_label',  style={'color': '#ffcb05'}),
        tooltip,
        dbc.Container([cards]),
        html.P('Out of these Pokemons, select the one that you want to catch -', className='fix_label',  style={'color': 'white'}),
        html.Div(
                [
            dbc.RadioItems(
                    id="radios",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=df_1_sort_type_subset['Name'].unique(),
                    value='No',
                        ),
            html.Div(id="radio-output"),
                ],
            className="radio-group",
                ),
        html.Br(),

        dbc.Row([dbc.Col(
                [
                    dash_table.DataTable(id='table-output',
                                         virtualization=True,
                                         style_cell={'textAlign': 'center',
                                                     'min-width': '150px',
                                                     'backgroundColor': '#0e2535',
                                                     'color': '#FEFEFE',
                                                     'border-bottom': '0.10rem solid #313841',
                                                     'font': 'Alilato'

                                                     },
                                         style_as_list_view=True,
                                         style_header={
                                            'textAlign': 'center',
                                             'backgroundColor': '#0e2535',
                                             #'fontWeight': 'bold',
                                              'font': 'Alilato',
                                             'color': 'white',
                                             'border': '#010915',
                                             'border-bottom': '0.10rem solid #313841'
                                         },

                                         style_data={'textOverflow': 'hidden', 'color': 'white'},
                                         fixed_rows={'headers': True}
                                         )
                ], width=6
            )
        ])
    ]
)

@callback(
    Output(cards,'children'),
    Input('type-choice', 'value')

)

def update_cards(selected_value):
    dff_img = df_1_sort_type[df_1_sort_type['Primary Type'] == selected_value]
    dff_img=dff_img.reset_index().drop(['index'],axis=1)
    dict_poke = dff_img.to_dict('records')
    #make a list of cards
    poke_cards =[]
    for poke in dict_poke:
        poke_cards.append(make_card(poke))

    card_layout = [
        dbc.Row([
        dbc.Col([dbc.Card(card, color="#0e2535", outline=True) for card in poke_cards[0:1]], width=3),
        dbc.Col([dbc.Card(card, color="#0e2535", outline=True) for card in poke_cards[1:2]], width=3)
                ], className="m-auto"),

        dbc.Row([
        dbc.Col([dbc.Card(card, color="#0e2535", outline=True) for card in poke_cards[2:3]], width=3),
        dbc.Col([dbc.Card(card, color="#0e2535", outline=True) for card in poke_cards[3:4]], width=3)
        ], className="m-auto")
    ]
    return card_layout

@callback(
    Output('radios', 'options'),
    Input('type-choice', 'value')
)

def update_radio(selected_value):
    dff_1 = df_1_sort_type_subset[df_1_sort_type_subset['Primary Type'] == selected_value]
    return dff_1['Name']

@callback(
    Output('radio-output', 'children'),
    Input('radios', 'value')
)

def update_radio_selection(value):
    if value=="None":
        return "You have not caught a Pokemon yet"
    else:
        return f"You have caught {value} Pokemon, here are some more details on it-"


@callback(
    Output('table-output', 'data'),
    Input('radios', 'value')
)


def update_table(value):
    dff = df_1_sort_type_subset[df_1_sort_type_subset['Name']==value]
    return dff.to_dict('records')