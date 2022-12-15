import dash
from dash import html, dcc

dash.register_page(__name__)

def layout():
  return html.Div(children=[
    html.H1(children='This is our Heatmap page'),

    html.Div(children='''
        This is our Archive page content.
    '''),

])