#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Huy Nguyen
# Created Date: Tue 7 Sep 2021
# =============================================================================

import requests
import pandas as pd
import plotly.express as px
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from utils import *
from dash.dependencies import Input, Output, State

# Variables
API_ENDPOINTS = "https://api.covid19api.com/summary"
NAVBAR_LOGO = "https://cdn.pixabay.com/photo/2020/04/29/07/54/coronavirus-5107715_1280.png"
NAVBAR_TITLE = "Covid-19 Live Tracker"

######## GET DATA ###########
# Get data from API
response = requests.get(API_ENDPOINTS)
response.raise_for_status()
data = response.json()

######## GET COMPONENTS ###########
# Country
country_df = pd.DataFrame(data["Countries"])
fig = choropleth_plot(dataframe=country_df)

# Navigation bar
navbar = create_navbar(title=NAVBAR_TITLE, logo=NAVBAR_LOGO)

# Data Card
confirmed_card = make_card(data=data, case="Confirmed", title="Confirmed", color="secondary")
recovered_card = make_card(data=data, case="Recovered", title="Recovered", color="success")
deaths_card = make_card(data=data, case="Deaths", title="Deaths", color="danger")

cards = make_card_row(confirmed=confirmed_card, recovered=recovered_card, deaths=deaths_card)

# Heading
heading = html.H2("Covid-19 Worldwide Impact", style={"text-align": "center", "padding-bottom": "30px"})

# Get choropleth graph
choropleth_graph = dcc.Graph(id="choropleth", figure=fig)

# Table
table = create_table(data=data)

# Dropdown
dropdown = dcc.Dropdown(
    id="dropdown",
    options=[{"label": con["Country"], "value": con["CountryCode"]} for con in data["Countries"]] + [
        {"label": "All", "value": "all"}],
    value="all",
    style={"margin-bottom": "20px"}
)

# Graph + Table
graph_table = html.Div([dbc.Row([dbc.Col(choropleth_graph, lg= 6), dbc.Col(html.Div([dropdown, table]), lg= 6)])])

# Bar chart
confirmed_fig = px.bar(country_df.sort_values(by="NewConfirmed", ascending=False).head(20),
                       x="CountryCode",
                       y="NewConfirmed",
                       hover_data=["Country"],
                       title="Top 20 New Confirmed",
                       labels= {"Country": "", "NewConfirmed": ""})
confirmed_graph = dcc.Graph(id="bar_graph", figure=confirmed_fig)

######## WRITE APP ###########
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Covid-19 Live Tracker"
server = app.server

app.layout = html.Div([
    navbar,
    html.Div([cards, heading, graph_table, confirmed_graph], style={"padding": "0px 50px 50px 50px"})
])


@app.callback(Output("table", "data"), [Input("dropdown", "value")])
def update_table(code):
    return get_rows(code, data)


######## RUN APP ###########
if __name__ == '__main__':
    app.run_server()
