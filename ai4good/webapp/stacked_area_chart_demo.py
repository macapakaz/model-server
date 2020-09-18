import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from student_visualisations import AgeBreakdown

external_stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

categories = ["Susceptible", "Exposed", "Infected (symptomatic)", "Asymptomatically Infected", "Recovered", "Hospitalised", "Critical", "Deaths", "Offsite", "Quarantined", "No ICU Care"]
ageCategories = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]

#Categories:
# Susceptible
# Exposed
# Infected (symptomatic)
# Asymptomatically Infected
# Recovered
# Hospitalised
# Critical
# Deaths
# Offsite
# Quarantined
# No ICU Care

app.layout = html.Div(children=[
    html.H1(children="Stacked area chart demonstration"),

    html.Div(children='''
        The stacked area chart can display the breakdown of the age groups of each category as well as showing the overall trend for the entire population.
    '''),

    dcc.Graph(
        id="age_breakdown_area_chart"
    ),
    html.Div([
        dcc.Dropdown(
                id="input_category",
                options=[{"label": i, "value": i} for i in categories],
                value="Asymptomatically Infected",
            ),
        dcc.RadioItems(
                id="input_percentage",
                options=[{"label": "Percentage", "value": "Percentage"}, {"label": "Decimal", "value": "Decimal"} ],
                value="Percentage",
                labelStyle={"display": "inline-block", 'margin': '5px'}
            ),
        "Days: ",
        dcc.Input(
                id='input_days',
                type='number',
                value=250,
                min=0,
                max=800
            )
        ],
        style={'width': '50%', 'display': 'inline-block'})
])

@app.callback(
    Output("age_breakdown_area_chart", "figure"),
    [Input("input_category", "value"),
     Input("input_percentage", "value"),
     Input("input_days", "value")]
    )
def Update_graph(input_category, input_percentage, input_days):
    if (input_percentage == "Percentage"):
        input_percentage = True
    else:
        input_percentage = False
    return AgeBreakdown(category=input_category, showAsPercent=input_percentage, days=input_days)


if __name__ == "__main__":
    app.run_server(debug=True)