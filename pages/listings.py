import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import ast

data = pd.read_csv("assets/listings_amenities.csv", sep="\t")
amenities = ["TV", "Microwave", "Shampoo", "Iron", "Free street parking", "Wifi", "Dishwasher", "Crib", "Rice maker", "Safe", "Board games", "Gym", "Patio or balcony", "Luggage dropoff allowed"]

#convert amenities string to list
for i, row in data.iterrows():
  data["amenities"][i] = ast.literal_eval(row["amenities"])

dash.register_page(__name__)

def layout():
  return html.Div(children=[
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
      amenities, 
      [],
      id="choose-amenity",
      multi=True),
    dcc.RadioItems(
      id='x-axis', 
      options= ['price', 'review_scores_rating'],
      value='review_scores_rating', 
      inline=True
    ),
    dcc.Graph(id="amenities-graph")
])

@callback(
  Output("amenities-graph", "figure"), 
  Input("x-axis", "value"),
  Input("choose-amenity", "value")
)
def generate_chart(xAxis, amenities):

  indices = [] # list of all indices that are not in the subset

  # iterate over all rows of the data and check if all chosen amenities are in the each amenities list
  for index, row in data.iterrows():
    res = all(i in row["amenities"] for i in amenities)
    
    # if not all chosen amenities are in the list, add index to indices list
    if not res:
      indices.append(index)

  # The new dataset is the difference between the whole dataset and the rows with indices from the indices list
  df = data[~data.index.isin(indices)]

  fig = px.histogram(df, x=xAxis)
  return fig
  