from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
  )

app.layout = html.Div([
  navbar,
  html.Div(
  ),

dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)