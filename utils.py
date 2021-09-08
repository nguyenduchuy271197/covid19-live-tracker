import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dash_table

# Country
def choropleth_plot(dataframe):
    """
    Return choropleth graph for covid19
    """
    fig = px.choropleth(data_frame=dataframe,
                        locations="Country",
                        locationmode="country names",
                        color="TotalConfirmed",
                        projection="orthographic",
                        hover_data=["NewConfirmed", "NewDeaths"],
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def make_card(data, case, title, color):
    """
    case: ['Confirmed', 'Deaths', 'Recovered']
    color: ["primary", "secondary", "success", "danger"]
    """
    total_case = f"Total{case}"
    new_case = f"New{case}"

    total = data["Global"][total_case]
    new = data["Global"][new_case]

    card = dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(
                [
                    html.H4(total, className="card-title"),
                    html.P(f"+{new}", className="card-text"),
                ]
            )
        ],
        style={"text-align": "center", "color": "white"}, color=color
    )
    return card


def create_navbar(title, logo):
    """
    Create navigation bar with logo and title
    """
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logo, height="80px")),
                        dbc.Col(dbc.NavbarBrand(title, className="ml-2",
                                                style={"padding-left": "20px", "font-size": "30px"})),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="#",
            )
        ],
        color="dark",
        dark=True,
    )

    return navbar


def make_card_row(confirmed, recovered, deaths):
    """
    Make card row from given data cards
    """
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(confirmed, md=4),
                    dbc.Col(recovered, md=4),
                    dbc.Col(deaths, md=4),
                ],
                className="mb-4",
            )
        ], style={"padding": "1rem"}
    )

    return cards


def create_table(data):
    """
    Create table to show all countries info
    """
    display_data = [
        {"Country": con["Country"], "TotalConfirmed": con["TotalConfirmed"], "TotalRecovered": con["TotalRecovered"],
         "TotalDeaths": con["TotalDeaths"]} for con in data['Countries']]

    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in display_data[0].keys()],
        data=display_data,
        style_cell={'textAlign': 'center', 'whiteSpace': 'normal'},
        style_table={'height': '500px', 'overflowY': 'auto'}
    )

    return table


def get_rows(code, data):
    """
    Update table
    """
    if code == "all":
        display_data = [
            {"Country": con["Country"], "TotalConfirmed": con["TotalConfirmed"],
             "TotalRecovered": con["TotalRecovered"],
             "TotalDeaths": con["TotalDeaths"]} for con in data['Countries']]
    else:
        display_data = [
            {"Country": con["Country"], "TotalConfirmed": con["TotalConfirmed"],
             "TotalRecovered": con["TotalRecovered"],
             "TotalDeaths": con["TotalDeaths"]} for con in data['Countries'] if con["CountryCode"] == code]

    return display_data
