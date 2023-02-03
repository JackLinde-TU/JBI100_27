import dash
from dash import dcc, callback, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import date

df = pd.read_csv("assets/host_data.csv", low_memory=False)

dash.register_page(__name__)

# Define app layout
def layout():
  return html.Div([
    html.H1("Host Analysis"),
    dbc.Row([
      dbc.Label('Host since', html_for="date-range", width=3),
      dbc.Col(
        dcc.DatePickerRange(
          id='date-range',
          min_date_allowed = date(2008, 8, 22),
          max_date_allowed = date(2022, 9, 5),
          start_date = date(2010, 1, 1),
          end_date = date(2020, 1, 1),
          initial_visible_month = date(2015, 1, 1)
        )
      )
    ]),
    dbc.Row([
      dbc.Label('Amount of listings', html_for="slider", width=3),
      dbc.Col(
        dcc.RangeSlider(
          id='slider',
          min=1,
          max=200,
          step=1,
          marks={
            1: '1',
            10: '10',
            20: '20',
            30: '30',
            40: '40',
            50: '50',
            100: '100',
            200: '200'
          },
          tooltip={"placement": "bottom", "always_visible": True},
          value=[0,50]
        ),
      )
    ]),
    dbc.Row([
      dbc.Label('Average listing price', html_for="date-rage", width=3),
      dbc.Col(
        dcc.RangeSlider(
          id='slider-price',
          min=0,
          max=2000,
          step=10,
          marks={
            0: '$0',
            100: '$100',
            200: '$200',
            300: '$300',
            400: '$400',
            500: '$500',
            1000: '$1000',
            1500: '$1500',
            2000: '$2000'
          },
          tooltip={"placement": "bottom", "always_visible": True},
          value=[100,500]
        )
      )
    ]),
    dbc.Row([
      dbc.Label('Commercial and/or private hosts', html_for="commericial", width=3),
      dbc.Col(
        dcc.Dropdown(
          id='commercial',
          options=['Commercial Host', 'Private Host'],
          value=['Commercial Host', 'Private Host'],
          multi=True
        )
      )
    ]),

    dbc.Row([
      dbc.Col([
        dbc.Label('Attribute for x-axis', html_for="x-axis"),
        dcc.Dropdown(
          id='x-axis', 
          options={
            'avg_price':'Average Price',
            'avg_rating':'Average Rating',
            'ag_success_metric':'Average Success Metric',
            'avg_cleanliness_rating':'Average Cleanliness Rating',
            'avg_checkin_rating':'Average Checkin Rating',
            'avg_communication_rating':'Average Communication Rating',
            'avg_location_rating':'Average Location Rating',
            'avg_value_rating':'Average Value Rating',
            'calculated_listing_count':'Host Listing Count',
            'response_rate':'Response Rate (%)',
            'acceptance_rate':'Acceptance Rate (%)'
          },
          searchable=False,
          value='response_rate'
        )
      ]),
      dbc.Col([
        dbc.Label('Attribute for y-axis', html_for="y-axis"),
        dcc.Dropdown(
          id='y-axis', 
          options={
            'avg_price':'Average Price',
            'avg_rating':'Average Rating',
            'avg_success_metric':'Average Success Metric',
            'avg_cleanliness_rating':'Average Cleanliness Rating',
            'avg_checkin_rating':'Average Checkin Rating',
            'avg_communication_rating':'Average Communication Rating',
            'avg_location_rating':'Average Location Rating',
            'avg_value_rating':'Average Value Rating',
            'calculated_listing_count':'Host Listing Count',
            'response_rate':'Response Rate (%)',
            'acceptance_rate':'Acceptance Rate (%)'
          },
          value='avg_success_metric'
        )
      ])
    ]),
    dbc.Row([
      dcc.Graph(id="graph"),
    ]),
    dbc.Card([
      dbc.CardHeader(id='click-host-id-3', className="card-title"),
      dbc.CardBody([
        html.P(id='click-host-id'),
        html.P(id='click-host-id-2'),
        # html.P(id='click-host-id-3'),
        html.P(id='click-host-id-4'),
        html.P(id='click-host-id-5'),
        html.P(id='click-host-id-6'),
        html.Blockquote(id='click-host-id-7'),
        html.P(id='click-host-id-8'),
        html.P(id='click-host-id-9')
      ])
    ]) 
  ])

@callback(
  Output("graph", "figure"),
  Input("slider", "value"),
  Input("x-axis", "value"), 
  Input("y-axis", "value"),
  Input("commercial", "value"),
  Input('date-range', 'start_date'),
  Input('date-range', 'end_date'),
  Input("slider-price", "value")
)
def update_figure(N_listings, x, y, commercial, start_date, end_date, price_range):
  data = df[df['calculated_listing_count'].between(N_listings[0], N_listings[1])]
  data = data[data['host_since'].between(start_date, end_date)]
  data = data[data['avg_price'].between(price_range[0], price_range[1])]

  if commercial == ['Commercial Host']:
      data = data[data['instant_bookable']=='t']
  elif commercial == ['Private Host']:
      data = data[data['instant_bookable']=='f']
  elif commercial == ['Commercial Host', 'Private Host']:
      data = data
  else:
      data = data

  labels={'host_id':'Host ID', 'host_name':'Host Name', 'response_rate':'Response Rate (%)', 'acceptance_rate':'Acceptance Rate (%)',\
          'calculated_listing_count':'Host Listing Count', 'host_url':'Host URL', 'avg_success_metric':'Average Success Metric'}

  if y in ['avg_rating', 'avg_cleanliness_rating', 'avg_checkin_rating',\
      'avg_communication_rating', 'avg_location_rating', 'avg_value_rating']:
      range_y = [3, 5]
  elif y == 'avg_success_metric':
      range_y = [0, 40]
  else:
      range_y = []
  
  if x in ['avg_rating', 'avg_cleanliness_rating', 'avg_checkin_rating',\
  'avg_communication_rating', 'avg_location_rating', 'avg_value_rating']:
      range_x = [3, 5]
  else:
      range_x = []

  fig = px.scatter(data, x=x, y=y, trendline="ols", marginal_x="histogram", marginal_y="histogram",\
                  hover_name='host_id', hover_data=['host_name','calculated_listing_count','host_url'], opacity=0.5, size_max=5,\
                  range_y=range_y, range_x=range_x, trendline_color_override="red",\
                  labels=labels)

  return fig

@callback(
  Output('click-host-id', 'children'),
  Output('click-host-id-2', 'children'),
  Output('click-host-id-3', 'children'),
  Output('click-host-id-4', 'children'),
  Output('click-host-id-5', 'children'),
  Output('click-host-id-6', 'children'),
  Output('click-host-id-7', 'children'),
  Output('click-host-id-8', 'children'),
  Output('click-host-id-9', 'children'),
  Input('graph', 'clickData'))
def update_click_output(clickData):
  host_id = clickData['points'][0]['hovertext']
  host_data = df[df['host_id'] == host_id]
  name = host_data['host_name'].values[0]
  listing_count = host_data['calculated_listing_count'].values[0]
  url = host_data['host_url'].values[0]
  neighbourhood = host_data['host_neighbourhood'].values[0]
  host_since = host_data['host_since'].values[0]
  host_about = host_data['host_about'].values[0]
  avg_price = host_data['avg_price'].values[0]
  response_time = host_data['response_time'].values[0]

  return f'{host_id}', f'URL: {url}', f'{name}', f'Listing Count: {listing_count}',\
      f'Neighbourhood: {neighbourhood}', f'Host Since: {host_since}', f'About: {host_about}',\
      f'Average Listing Price: {avg_price}', f'Response Time: {response_time}'
