import json
import plotly.express as px
import numpy as np
import pandas as pd
import csv

def succes_metric_per_neighbourhood():
    f = open('Data/neighbourhoods.geojson') # open geodata json file
    listings_data = pd.read_csv('Data/listings.csv', low_memory=False) # read listing information from csv file
    neighbourhoods_geodata = json.load(f) # read geodata json file
    listings_data['price'] = listings_data['price'].replace({'\$':'', ',':''}, regex = True).astype(float)
    listings_data['success_metric'] = listings_data['review_scores_rating'] * listings_data['reviews_per_month']
    success_metric_array = np.array(listings_data['success_metric'])
    success_metric_array[np.isnan(success_metric_array)] = 0
    column_1 = [] 
    prices_neighbourhoods = np.zeros(len(neighbourhoods_geodata['features']))
    success_metric = np.zeros(len(neighbourhoods_geodata['features']))
    density = []
    
    for i in range(0,len(neighbourhoods_geodata['features'])): # go through the neigbourhoods in the geojson data
        density.append((listings_data['neighbourhood_cleansed'] == neighbourhoods_geodata['features'][i]['properties']['neighbourhood']).sum())
        column_1.append(neighbourhoods_geodata['features'][i]['properties']['neighbourhood']) # append the neighbourhood from geojson to  column 1
        k = 0
        for j in range(0,len(listings_data['neighbourhood_cleansed'])):
            if neighbourhoods_geodata['features'][i]['properties']['neighbourhood'] == listings_data['neighbourhood_cleansed'][j]:
                success_metric[i] += success_metric_array[j]
                prices_neighbourhoods[i] += listings_data['price'][j]
                k += 1
        # print(k)
        if k != 0:
            prices_neighbourhoods[i] = prices_neighbourhoods[i]/density[i]
            success_metric[i] = success_metric[i]/density[i]
        # if succes_metric[i]


    neighbourhood_pd = {'neighbourhood': column_1, 'density': density, 'average_price':prices_neighbourhoods, 'Success_metric': success_metric}

    neighbourhood_pd = pd.DataFrame(neighbourhood_pd)
    # print(neighbourhood_pd.head())
    # neighbourhood_pd.to_csv('sample.csv')  

succes_metric_per_neighbourhood()