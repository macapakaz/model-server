import dash             
import dash_core_components as dcc
import dash_html_components as html
from student_visualisations import get_sunburst_values, generate_sunburst
import pandas as pd

df = pd.read_csv("..\\..\\fs\\params\\camp_params.csv")
df = df[df['Camp']=='Moria']

labels, parents, values = get_sunburst_values(df)
graph = generate_sunburst(labels, parents, values)

SunburstChart = dash.Dash()

SunburstChart.layout = html.Div([
    dcc.Graph(figure=graph),
])

if __name__ == '__main__':
    SunburstChart.run_server(debug=True)  # Dash is running on http://127.0.0.1:8050/