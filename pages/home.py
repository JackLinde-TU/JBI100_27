import dash
from dash import Dash, html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from assets.choropleth import create_choropleth

listings_data = pd.read_csv('assets/listings.csv', low_memory=False)
listings_data['success_metric'] = listings_data['review_scores_rating'] * listings_data['reviews_per_month']
success_metric_array = np.array(listings_data['success_metric'])
success_metric_array[np.isnan(success_metric_array)] = 0
listings_data['success_metric'] = success_metric_array
listings_data['price'] = listings_data['price'].replace({'\$':'', ',':''}, regex = True).astype(float)


dash.register_page(__name__, path='/')

def layout():
  return html.Div([
    html.H1("Geographical Analysis"),
    dbc.Row([
      dbc.Label('Choose a metric', html_for="dropdown", width="auto"),
      dbc.Col(
        dcc.Dropdown(
          id = 'dropdown menu 1',
          # first you specify the label which the user sees, then specify the value which you return to the callback. 
          options = [
            {'label': 'Total amount of Airbnb\'s', 'value': 'density'},
            {'label': 'Average price', 'value':'average_price'},
            {'label': 'Average success metric', 'value':'Success_metric'},
          ],
        #value = 'NYC', # Default value  
        )
      )
      # html.Div(id='output-text 1'), # output coming from the callback
    ], className="mb-3"),
    dbc.Row([
      dbc.Col(dcc.Graph(id='choropleth'))
      # html.Div(id='neighborhood222')
    ]),
    dbc.Row([
      dbc.Col(dcc.Graph(id="violin_price", style={'display': 'inline-block'}), width="6"),
      dbc.Col(dcc.Graph(id="violin_success", style={'display': 'inline-block'}), width="6")
    ]),
  ])

@callback(
  Output('choropleth', 'figure'),
  Input('dropdown menu 1', 'value'),
)

def figure(value):
  return create_choropleth(value)

@callback(
  Output('violin_price', 'figure'),
  Output('violin_success', 'figure'),
  Input('choropleth', 'clickData'),)

def figure(clickData):
  selected_location = clickData['points'][0]['location']
  filter_listings_data = listings_data[listings_data.neighbourhood_cleansed == selected_location]

  fig1 = px.violin(filter_listings_data, y='price',labels=dict(price="Price ($)"),title="Violin plot of the price in " + selected_location, )
  fig2 = px.violin(filter_listings_data, y='success_metric', labels=dict(success_metric = "Success metric"),title="Violin plot of the success metric in "+selected_location)

  return fig1, fig2