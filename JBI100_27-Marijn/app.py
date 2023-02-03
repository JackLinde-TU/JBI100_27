from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from choropleth import create_choropleth
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

listings_data = pd.read_csv('Data/listings.csv', low_memory=False) 
listings_data['success_metric'] = listings_data['review_scores_rating'] * listings_data['reviews_per_month']
success_metric_array = np.array(listings_data['success_metric'])
success_metric_array[np.isnan(success_metric_array)] = 0
listings_data['success_metric'] = success_metric_array
listings_data['price'] = listings_data['price'].replace({'\$':'', ',':''}, regex = True).astype(float)

app = Dash(__name__)

app.layout = html.Div(children=[
html.H1('Geographical analysis tool'),
html.Div([
    html.Label('Choose a heatmap metric:'),
    dcc.Dropdown(
        id = 'dropdown menu 1',
        # first you specify the label which the user sees, then specify the value which you return to the callback. 
        options = [
            {'label': "Total amount of Airbnb's", 'value': 'density'},
            {'label': 'Average price', 'value':'average_price'},
            {'label': 'Average success metric', 'value':'Success_metric'},
            ],
            
        ),
    ]),

html.Div([    
    dcc.Graph(
        
        id='choropleth'
    ),
    
]),

html.Div(children=[
        dcc.Graph(id="violin_price", style={'display': 'inline-block'}),
        dcc.Graph(id="violin_success", style={'display': 'inline-block'}),

])
])  

@app.callback(
    Output('choropleth', 'figure'),
    Input('dropdown menu 1', 'value'),
)

def figure(value):
    return create_choropleth(value)


@app.callback(
    Output('violin_price', 'figure'),
    Output('violin_success', 'figure'),
    Input('choropleth', 'clickData'),)

def figure(clickData):
    selected_location = clickData['points'][0]['location']
    filter_listings_data = listings_data[listings_data.neighbourhood_cleansed == selected_location]

    fig1 = px.violin(filter_listings_data, y='price',labels=dict(price="Price ($)"),title="Violin plot of the price in " + selected_location)
    fig2 = px.violin(filter_listings_data, y='success_metric', labels=dict(success_metric = "Success metric"),title="Violin plot of the success metric in "+selected_location)

    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)


