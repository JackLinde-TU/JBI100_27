from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LITERA])

#navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
          dbc.NavLink(
            f"{page['name']}", href=page['relative_path']
          )
        )
        for page in dash.page_registry.values() 
    ],
    brand="Airbnb Analyser",
    brand_href="#",
    color="light",
    dark=False,
  )

app.layout = html.Div([
  navbar,
  html.Main(
    children=[
      html.Div(
        children=[dash.page_container],
        className="container",
      )
    ],
  ),
])

if __name__ == '__main__':
	app.run_server(debug=True)