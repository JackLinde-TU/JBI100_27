from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

dash.register_page(__name__)

def layout():
  return html.Div(children=[
    html.H1(children='This is our Heatmap page'),

    html.Div(children='''
        This is our Archive page content.
    '''),

])