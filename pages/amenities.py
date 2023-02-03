import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import ast

#data = pd.read_csv("assets/listings_amenities.csv", sep="\t")
amenities = ["TV", "Microwave", "Shampoo", "Iron", "Free street parking", "Wifi", "Dishwasher", "Crib", "Rice maker", "Safe", "Board games", "Gym", "Patio or balcony", "Luggage dropoff allowed"]

dataAM = pd.read_csv("assets/listings_amenities.csv")

#convert amenities string to list
for i, row in dataAM.iterrows():
  dataAM["amenities"][i] = ast.literal_eval(row["amenities"])

dash.register_page(__name__)

def layout():
  return html.Div([
    html.H1("Amenities Analysis"),
    dbc.Row([
      dbc.Label('Available amenities'),
      dbc.Col([
        dcc.Dropdown(
          amenities, 
          [],
          id="choose-amenity",
          multi=True
        ),
      ])
    ]),
    dbc.Row([
      dbc.Label('Amount of bedrooms'),
      dbc.Col([
        dcc.Dropdown(
          ['All', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '13'], # is no actual 10 bedrooms listing but still added value 
          ['All'],
          id='choose-bedrooms'
        )
      ]),
      dbc.Label('Room type'),
      dbc.Col([
        dcc.Dropdown(
          ['All', 'Private room', 'Entire home/apt', 'Hotel room', 'Shared room'], 
          ['All'],
          id='choose-room_type'
        )
      ])
    ]),
    dbc.Row([
      dbc.Label('Exclude outliers?'),
      dbc.Col([
        dbc.RadioItems(
          id= 'exclude-outliers',
          options=[
            {"label": "Yes", "value": "yes"}, 
            {"label": "No", "value": "no"}
          ], 
          value= 'yes',
          inline=True
        )
      ])
    ]),
    dbc.Row([
      dbc.Label('What do you want to inspect?'),
      dbc.Col([
        dbc.RadioItems(
          id='x-axis', 
          options=[
            {"label": "Price", "value": "price"},
            {"label": "Review score", "value": "review_scores_rating"},
            {"label": "Success", "value": "success_metric"}
          ],
          # options= ['price', 'review_scores_rating', 'success_metric'],
          value='review_scores_rating', 
          inline=True
        )
      ])
    ]),
    dcc.Graph(id="amenities-graph"),
    dcc.Graph(id="violin-graph")
])

@callback(
  Output("amenities-graph", "figure"), 
  Output("violin-graph", "figure"), 
  Input("x-axis", "value"),
  Input("choose-amenity", "value"),
  Input("choose-bedrooms", "value"), 
  Input("choose-room_type", "value"), 
  Input('exclude-outliers', 'value')
)
def generate_chart(xAxis, amenities, bedrooms, room_type, exclude_outliers):

  indices = [] # list of all indices that are not in the subset

  # iterate over all rows of the data and check if all chosen amenities are in the each amenities list
  for index, row in dataAM.iterrows():
    res = all(i in row["amenities"] for i in amenities)
    
    # if not all chosen amenities are in the list, add index to indices list
    if not res:
      indices.append(index)

  # The new dataset is the difference between the whole dataset and the rows with indices from the indices list
  df = dataAM[~dataAM.index.isin(indices)]
  if bedrooms != ['All'] and bedrooms != 'All':
    df = df[df['bedrooms'] == int(bedrooms)]

  if room_type != ['All'] and room_type != 'All':
    df = df[df['room_type'] == str(room_type)]

  if exclude_outliers == 'yes' and xAxis == 'price' and np.shape(df)[0] > 10:
    df = df[df['price'] < df.price.quantile(0.95)]
  fig = px.histogram(df, x=xAxis)
  fig2 = px.box(df, x=xAxis)
  return fig, fig2