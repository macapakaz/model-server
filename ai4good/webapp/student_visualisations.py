# Please add your own visualisations to this file.
# Lay them out similarly to how they are in plotter.py so that they are modular and can be used in various places. (Each visualisation has its own subroutine.)
# Also if you could add a comment next to the definition of each subroutine with the names of the people who worked on it, that would be great. -Max

import pandas as pd     
import plotly.express as px
import dash             
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

PieChart_CampParams = dash.Dash(__name__)     #initializing dash

#---------------------------- DataFrame---------------------------------------------------------

df = pd.read_excel("camp_params.xlsx")        # this code uses the parameters copied from fs/params/camp_params.csv (from column camp to Population_structure)
df = df[df['Camp']=='Haman-al-Alil']          # Select the camp 'Moria' or 'Haman-al-Alil'

#------------------------------Layout------------------------------------------------------------
PieChart_CampParams.layout = html.Div([       # designing the layout of the page 
    html.Div([
        html.Div([
        dcc.Dropdown(id='piedropdown',        # choosing dropdown component and adding the parameters
            options=[
                     {'label': 'Symptomatic', 'value': 'p_symptomatic'},        # label is the name displayed in the drop down, value is the parameter name in excel sheet
                     {'label': 'Hospitalized Symptomatic', 'value': 'Hosp_given_symptomatic'},
                     {'label':'Critical Hospitalized', 'value':'Critical_given_hospitalised'},
                     {'label':'Population Stucture', 'value':'Population_structure'},
                     {'label':'Chances of Symptomatic Cases becoming Critical', 'value':'Rough prob symptomatic case becomes critical'},
                     {'label':'Expected Critical Cases', 'value':'Rough exp. no. critical'}
            ],
            value='Population_structure',     # intial parameter that is plotted when the webpage loads
            multi=False,                      # 'multi': for choosing multiple values in the dropdown 
            clearable=False
        ),
        ],className='six columns'),
    ],className='row'),                       # one row assigned to dropdown

   html.Div([
       html.Div([
            dcc.Graph(id='piechart'),        # choosing the Graph dash component 
        ],className='six columns'),

    ],className='row'),                      # next row assigned to pie-chart
])

#-----------------------------PieChart----------------------------------------------------------------
@PieChart_CampParams.callback(              # adding interactive element to the page
    Output('piechart', 'figure'),           # output that will be obtained
     [Input('piedropdown', 'value')],       # input list to the graph from dropdrown
     
)
def update_graphs(piedropdown):             # function to call the input values (argument) 
    dff=df                                  # creating a copy of the global dataframe df
    pie_chart=px.pie(                       # calling pie interface from plotly express
            data_frame=dff,
            names='Age',                    # the column name according to which data will be classified into different pie sectors
            values=piedropdown,             # the paramters which will be visulatised
            hover_name='Age',               # age will be shown in bold in hover text
            hole=.25,                       # donut chart
            title='Camp Parameters',        
            hover_data=['Camp'],            # exta data to be shown in hover text
             width=800,                     # figure width in pixels
             height=600,  
            )
    pie_chart.update_traces(marker=dict(line=dict(color='#000000', width=2)))   # adding design and extended features to pie chart 

   return (pie_chart)                       # function returns pie_chart figure
#------------------------------------------------------------------

if __name__ == '__main__':
    PieChart_CampParams.run_server(debug=True)      # Dash is running on http://127.0.0.1:8050/
