import json
import plotly.express as px
import pandas as pd

def create_choropleth(metric):
    f = open('assets/data/neighbourhoods.geojson') # open geodata json file
    neighbourhoods_geodata = json.load(f) # read geodata json file
    neighbourhood_pd = pd.read_csv('assets/data/sample.csv')
        
    fig = px.choropleth_mapbox(neighbourhood_pd, geojson=neighbourhoods_geodata, color=metric, # use listings_data and neighbourds_geodata as input values, set heatmap to density
        locations="neighbourhood", featureidkey="properties.neighbourhood", # make it so neighbourhoods are the attribute in both inputs
        color_continuous_scale="matter_r",center={"lat": 40.7128, "lon": -73.935242}, # set standard starting location 
        mapbox_style="carto-positron", zoom=9,labels=dict(density="Amount of Airbnb's",average_price="Price ($)",Success_metric="Success metric"))
   
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
    return fig