import dash
from dash import dcc, html

dash.register_page(__name__, name='CONCLUSION')

layout = html.Div(
    [
        dcc.Markdown('Congratulations, you have finally become a trainer')
    ]
)
