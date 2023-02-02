import json
import plotly.express as px
import numpy as np
import pandas as pd
# from success_metric_neighbourhoods import succes_metric_per_neighbourhood
listings_data = pd.read_csv('Data/listings.csv', low_memory=False) 
selected_location = 'Williamsburg'
filter_listings_data = listings_data[listings_data.neighbourhood_cleansed == selected_location]
fig = px.box(filter_listings_data, y = 'price')
fig.show()