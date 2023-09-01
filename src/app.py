import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.SUPERHERO])
server=app.server
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="display-4 fw-bold",style={'fontSize':20}),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-primary bg-gradient fw-bold",
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Img(src='assets/pokemon-logo.png',style={'height':'90%', 'width':'20%'}), width=10),

        dbc.Col(
            html.Img(src='assets/pokeball.png',style={'height':'80%', 'width':'100%'}), width=2),

            #html.Div("Pokemon",
                         #style={'fontSize':50, 'textAlign':'left',}))
    ], justify='start',className='h-5'),

    dbc.Row(
            html.P("POKEMON TRAINER GUIDE",className="fw-bold h-5", style={'fontSize':35,'fontColor':'black', 'textAlign':'center'})
            ),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ],className='h-90')
], fluid=True,style={"height": "100vh"})


if __name__ == "__main__":
    app.run(debug=True,port=8053)

