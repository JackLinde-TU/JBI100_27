from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from choropleth import create_chroropleth

listings_data = pd.read_csv('Data/listings.csv', low_memory=False) 

app = Dash(__name__)

app.layout = html.Div(children=[
html.Div([
    html.Label('Choose a heatmap metric:'),
    dcc.Dropdown(
        id = 'dropdown menu 1',
        # first you specify the label which the user sees, then specify the value which you return to the callback. 
        options = [
            {'label': 'Total amount of Airbnb"s', 'value': 'density'},
            {'label': 'Average price', 'value':'average_price'},
            {'label': 'Average success metric', 'value':'Success_metric'},
            ],
            #value = 'NYC', # Default value
            
        ),
    # html.Div(id='output-text 1'), # output coming from the callback
    ]),

html.Div([   
    html.Div('Choropleth map'), 
    dcc.Graph(
        
        id='choropleth'
    ),
    # html.Div(id='neighborhood222')
    
]),
html.Div([
    html.Div('Box plot'),
    dcc.Graph(
        id='box_plot'
        ),

]),
])  

@app.callback(
    Output('choropleth', 'figure'),
    Input('dropdown menu 1', 'value'),
)

def figure(value):
    return create_chroropleth(value)


@app.callback(
    Output('box_plot', 'figure'),
    Input('choropleth', 'clickData'),)

def figure(clickData):
    selected_location = clickData['points'][0]['location']
    filter_listings_data = listings_data[listings_data.neighbourhood_cleansed == selected_location]
    fig = px.box(filter_listings_data, y = 'price')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


