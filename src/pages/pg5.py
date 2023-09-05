import dash
from dash import dcc, html, callback, Output, Input, dash_table, ctx
import plotly.express as px
import pandas as pd
import numpy as np
import dash_daq as daq
import random
import dash_bootstrap_components as dbc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import os
import pathlib
from pathlib import Path

dash.register_page(__name__, name='CREATE')

full_path = os.path.abspath(__file__)
#print(os.path.abspath(__file__))
parent_folder = Path(full_path).parents[2]
#print(parent_folder)
#PATH = pathlib.Path(__file__).parent
#print(PATH)
DATA_PATH = parent_folder.joinpath("src/data").resolve()
IMAGE_PATH= parent_folder.joinpath("src/assets/images").resolve()

df_1 = pd.read_csv(DATA_PATH.joinpath('pokedex.csv'))
df_1=df_1.drop('Unnamed: 0',axis=1)

df_status=df_1.groupby('status').agg({'weight_kg':'mean','height_m':'mean','total_points':'mean','base_experience':'mean','hp':'mean','catch_rate':'mean','generation':'count'})
status_df_stats=pd.DataFrame(df_status)
status_df_stats=status_df_stats.reset_index()
status_df_stats=status_df_stats.rename(columns={'status':'Status', 'weight_kg':'Weight(kg)','height_m':'Height(m)','total_points':'Total Points','base_experience':'Base Expereince','hp':'Hp','catch_rate':'Catch Rate','generation':'Generation'})
status_df_stats['Weight(kg)']=round(status_df_stats['Weight(kg)'],0)
status_df_stats['Height(m)']=round(status_df_stats['Height(m)'],0)
status_df_stats['Total Points']=round(status_df_stats['Total Points'],0)
status_df_stats['Base Expereince']=round(status_df_stats['Base Expereince'],0)
status_df_stats['Hp']=round(status_df_stats['Hp'],0)
status_df_stats['Catch Rate']=round(status_df_stats['Catch Rate'],0)


df_1_rf_subset=df_1[['pokedex_number','name','generation','status','type_1','height_m','weight_kg','ability_1','total_points','hp','attack','defense','sp_attack','sp_defense','speed','catch_rate','base_friendship','base_experience','growth_rate']]
df_1_rf_subset_normal=df_1_rf_subset[df_1_rf_subset['status']=='Normal']
#Undersampling to take care of imbalanced data
df_1_rf_subset_normal=df_1_rf_subset_normal.sample(n=45)
df_1_rf_subset_other=df_1_rf_subset[df_1_rf_subset['status']!='Normal']
#Combining to create the final dataset
df_1_rf_subset_sampled=pd.concat([df_1_rf_subset_other,df_1_rf_subset_normal])

#Creating the dependent variable class
factor = pd.factorize(df_1_rf_subset_sampled['status'])
df_1_rf_subset_sampled.status = factor[0]
definitions = factor[1]

#Filtering only important features
x_set=df_1_rf_subset_sampled.drop(['status','name','pokedex_number','hp','attack','defense','sp_attack','sp_defense','speed'],axis=1)
#Creating dummies for categorical features
x_set_dummies=pd.get_dummies(x_set)
x_set_dummies=x_set_dummies.fillna(0)
x=x_set_dummies.values

y_set=df_1_rf_subset_sampled['status']
y=y_set.values

#Input feature scaling
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

#Training and Fitting the RF model
classifier_full = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 42)
classifier_full.fit(x_scaled, y)

#Feature Importance
importance=classifier_full.feature_importances_
parameters=x_set_dummies.columns.values
df_imp = pd.DataFrame({'parameters':parameters,
                      'importance':importance})
df_imp_sort=df_imp.sort_values(['importance'],ascending=False)
reversefactor = dict(zip(range(4),definitions))

existing_names=list(df_1_rf_subset.name.unique())

df_generation=df_1.groupby('generation').agg({'pokedex_number':'count'})
df_generation=df_generation.reset_index()
df_generation=df_generation.rename(columns={'generation':'Generation','pokedex_number':'Number of Pokemons'})


df_status_num=df_1.groupby('status').agg({'pokedex_number':'count'})
df_status_num=df_status_num.reset_index()
df_status_num=df_status_num.rename(columns={'status':'Status','pokedex_number':'Number of Pokemons'})



fig = px.scatter(status_df_stats,x='Status', y='Weight(kg)',size='Weight(kg)')
#fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',xaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)')
fig.update_yaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)
fig.update_xaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)

fig_1 = px.scatter(status_df_stats,x='Status', y='Height(m)',size='Height(m)')
#fig_1.update_traces(texttemplate='%{text:.2s}', textposition='inside')
fig_1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',xaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)')
fig_1.update_yaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)
fig_1.update_xaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)

fig_3=px.line(df_generation, x='Generation', y='Number of Pokemons')
#fig_3.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_3.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',xaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)')
fig_3.update_yaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)
fig_3.update_xaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)

fig_4=px.pie(df_status_num, values='Number of Pokemons', names='Status')
fig_4.update_layout(
    legend_title_font_color="green"
)

fig_4.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',xaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)',font=dict(color='white'),
        template="plotly_dark")
fig_4.update_yaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)
fig_4.update_xaxes(title_font_color='white', tickfont_color='white',showgrid=True, zeroline=False)

status_weight=dbc.Card([
        dbc.CardBody(
            [
                html.H5("Did you know that Average weight of a Legendary Pokemon is ~5.5 times more than the Average weight of a human being? ", className='text-light'),
                dcc.Graph(
                    id='weight-type-1',
                    figure=fig


                ),

            ],style={"border": "none", "backgroundColor":'#0e2535'}
        )],style={"border": "none", "backgroundColor":'#0e2535'},className='m-0',
    )

status_height=dbc.Card([
        dbc.CardBody(
            [
                html.H5("Cosmoem, a pyshcic type Legendary Pokemon has the least height (0.1m) but the highest weight (999.9 Kg) ", className='text-light'),
                dcc.Graph(
                    id='height-type-1',
                    figure=fig_1


                ),

            ],style={"border": "none", "backgroundColor":'#0e2535'}
        )],style={"border": "none", "backgroundColor":'#0e2535'},className='m-0',
    )

gen_population=dbc.Card([
        dbc.CardBody(
            [
                html.H5("Starting Generation VI, Pokémon series moved to the 3D-era in all of this generation's games onwards. This is one of the reasons why these latter "
                        "generations have less Pokemons.", className='text-light'),
                dcc.Graph(
                    id='gen-type-1',
                    figure=fig_3


                ),

            ],style={"border": "none", "backgroundColor":'#0e2535'}
        )],style={"border": "none", "backgroundColor":'#0e2535'},className='m-0',
    )
tab_population=dbc.Card([
        dbc.CardBody(
            [
                html.H5("Did you know that you are 30 times more likely to encounter a Normal Pokemon as compared to a Mythical Pokemon?", className='text-light'),
                dcc.Graph(
                    id='status-type-1',
                    figure=fig_4


                ),

            ],style={"border": "none", "backgroundColor":'#0e2535'}
        )],style={"border": "none", "backgroundColor":'#0e2535'},className='m-0',
    )


Parametertooltip = html.Div(
    [
        html.H3(
            [
                "Select the following ",
                html.Span(
                    "parameters",
                    id="parameter-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                    className='text-primary'
                ),
                " to build your own Pokemon",
            ]
        ),
        dbc.Tooltip(
            "Please only use the up and down arrows to select numeric inputs "
            ,
            target="parameter-target",placement='bottom'),
    ],className="style-tooltip"
)

def generate_new_pokemon_name(existing_names,num_syllables=2):
    new_name=""
    for i in range(num_syllables):
        random_name=random.choice(existing_names)
        syllables=random_name.lower().split()
        if len(syllables)>1:
            new_name+=random.choice(syllables)
        else:
            new_name+=syllables[0]
    return new_name.capitalize()

layout = html.Div(
    [
       Parametertooltip,
       dbc.Row([
          dbc.Col([
              html.P('Primary Type'),
              dcc.Dropdown(x_set['type_1'].unique(),id='type-choice', value='Grass',className='fw-bold',style={'color':'black'})
                 ],width=2),
          dbc.Col([
              html.P('Primary Ability'),
              dcc.Dropdown(x_set['ability_1'].unique(),id='ability-choice', value='Pressure',className='fw-bold',style={'color':'black'})
                 ],width=2),
           dbc.Col([
              html.P("Generation (1-8)"),
              dbc.Input(type="number",id='gen-choice',value=1, min=1, max=8, step=1),
                  ],width=2),
           dbc.Col([
              html.P("Total Points(175-1025)"),
              dbc.Input(type="number",id='tp-choice',value=500, min=175, max=1025, step=10),
                  ],width=2),
           dbc.Col([
              html.P("Height (0.1-100m)"),
              dbc.Input(type="number",id='height-choice',value=1.3, min=0.1, max=100, step=0.1),
                  ],width=2)
              ]),
        html.Br(),
       dbc.Row([
            dbc.Col([
              html.P("Weight (0.1-999.9 Kg)"),
              dbc.Input(type="number",id='weight-choice',value=60.0, min=0.1, max=999.9, step=2.5),
                  ],width=2),
          dbc.Col([
              html.P('Growth Rate'),
              dcc.Dropdown(x_set['growth_rate'].unique(),id='growth-choice', value='Slow',className='fw-bold',style={'color':'black'})
                 ],width=2),
          dbc.Col([
              html.P("Experience (36-608)"),
              dbc.Input(type="number",id='exp-choice',value=70, min=36, max=608, step=10),
                  ],width=2),
          dbc.Col([
              html.P("Friendship (0-255)"),
              dbc.Input(type="number",id='fr-choice',value=70, min=0, max=255, step=1),
                  ],width=2),
          dbc.Col([
              html.P("Catch Rate (0-255)"),
              dbc.Input(type="number", id='catch-choice',value=70,min=0, max=255, step=1),
                  ],width=2),
              ]),
          html.Br(),
          html.Div(id='predict-text'),
          dbc.Row([dbc.Col([status_weight],width=6),
                   dbc.Col([status_height],width=6)]),
          dbc.Row([dbc.Col([tab_population],width=6),
                   dbc.Col([gen_population],width=6)])


    ]
)

@callback(
    Output('predict-text','children'),
    Input('type-choice','value'),
    Input('ability-choice','value'),
    Input('gen-choice','value'),
    Input('tp-choice','value'),
    Input('height-choice','value'),
    Input('weight-choice','value'),
    Input('growth-choice','value'),
    Input('exp-choice', 'value'),
    Input('fr-choice', 'value'),
    Input('catch-choice', 'value')
)

def update_values(type,ability,gen,tp,height,weight,growth,exp,fr,catch):
    Generation = int(gen)
    Total_Points = int(tp)
    Height = float(height)
    Weight = float(weight)
    Experience = int(exp)
    Friendship = int(fr)
    Catch_Rate = int(catch)
    #new_data_row = [gen, type, height, weight, ability, tp, catch, fr,
                    #exp, growth]
    new_data_row = [Generation, type, Height, Weight, ability, Total_Points, Catch_Rate, Friendship,
                    Experience, growth]
    x_set = df_1_rf_subset_sampled.drop(['status', 'name', 'pokedex_number', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'], axis=1)
    x_set = x_set.reset_index().drop(['index'], axis=1)
    x_set.loc[len(x_set)] = new_data_row
    x_set_dummies_mod = pd.get_dummies(x_set)
    x_mod = x_set_dummies_mod.values
    new_data = x_mod[len(x_mod) - 1]
    new_data = new_data.reshape(1, -1)
    new_data_scaled = scaler.transform(new_data)
    y_pred_full = classifier_full.predict(new_data_scaled)
    y_pred_full = np.vectorize(reversefactor.get)(y_pred_full)
    new_name=generate_new_pokemon_name(existing_names)
    return html.H4(f"The name of your Pokemon is " + new_name + " and it is of " + y_pred_full[0] + " type",className='text-primary fw-bold')


