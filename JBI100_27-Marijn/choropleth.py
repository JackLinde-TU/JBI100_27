import json
import plotly.express as px
import numpy as np
import pandas as pd
# from success_metric_neighbourhoods import succes_metric_per_neighbourhood

def create_chroropleth(metric):
    f = open('Data/neighbourhoods.geojson') # open geodata json file
    listings_data = pd.read_csv('Data/listings.csv', low_memory=False) # read listing information from csv file
    neighbourhoods_geodata = json.load(f) # read geodata json file
    neighbourhood_pd = pd.read_csv('Data/sample.csv')

    # column_1 = [] 
    # column_2 = []
    # succes_metric = listings_data['review_scores_rating']*listings_data['number_of_reviews_ltm']
  
    # for i in range(0,len(neighbourhoods_geodata['features'])): # go through the neigbourhoods in the geojson data
    #     column_1.append(neighbourhoods_geodata['features'][i]['properties']['neighbourhood']) # append the neighbourhood from geojson to  column 2
    #     column_2.append((listings_data['neighbourhood_cleansed'] == neighbourhoods_geodata['features'][i]['properties']['neighbourhood']).sum()) # sum of true values where particular neighbourhood in neigbhourhood is equal to neighbourhood in data

    # column_3 = succes_metric_per_neighbourhood()
    # neighbourhood_pd = {'neighbourhood': column_1, 'Succes metric': column_3}    # set it to dictionary
    # neighbourhood_pd = pd.DataFrame(neighbourhood_pd) # make pandas dataframe from dictionary
    fig = px.choropleth_mapbox(neighbourhood_pd, geojson=neighbourhoods_geodata, color=metric, # use listings_data and neighbourds_geodata as input values, set heatmap to density
                                locations="neighbourhood", featureidkey="properties.neighbourhood", # make it so neighbourhoods are the attribute in both inputs
                               color_continuous_scale="matter_r",center={"lat": 40.7128, "lon": -73.935242}, # set standard starting location 
                                mapbox_style="carto-positron", zoom=9)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # fig.show() 
    return fig
        

if __name__ == '__main__':
    figure = create_chroropleth()
    # figure.show()
