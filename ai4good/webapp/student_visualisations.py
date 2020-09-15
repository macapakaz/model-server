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

#Age breakdown stacked area chart -Max -----------------------------------------------------------------
def AgeBreakdown(category = None, days = 250, showAsPercent = False, df = None):
    if (df == None):
        data = pd.read_csv("expected_report.csv")
    else:
        data = df
    columns = []
    for item in data.columns:
        #print(item)
        columns.append(item)

    try:
        categories.index(category)
        selectedCategory = category
    except ValueError:
        selectedCategory = "Asymptomatically Infected"

    #selectedCategory = "Asymptomatically Infected"
    dataColumnIndexes = []
    dataColumnIndexesRemoval = []
    selectedCategory = selectedCategory + ":"
    dataColumnNames = []
    for i in range(0, len(columns)-1):
        testCategory = columns[i]
        if (testCategory[0:len(selectedCategory)] == selectedCategory):
            dataColumnIndexes.append(i)
            dataColumnNames.append(testCategory)
        else:
            dataColumnIndexesRemoval.append(i)

    print(dataColumnNames)
    #print(data[dataColumnNames].copy())
    #input()
    #print(data[dataColumnNames].head(250).copy())
    dataToPlot = data[dataColumnNames].head(days).copy()
    if (showAsPercent):
        dataToPlot = dataToPlot.multiply(100).copy()

    fig = go.Figure()
    x = dataToPlot.columns
    colours = ["rgb(0, 0, 252)", "rgb(33, 33, 252)", "rgb(66, 66, 252)", "rgb(99, 99, 252)", "rgb(132, 132, 252)", "rgb(165, 165, 252)", "rgb(198, 198, 252)", "rgb(211, 211, 252)"]
    for column in dataToPlot.columns:

        label = str(column)
        for ageRange in ageCategories:
            if (ageRange in column):
                label = ageRange
                break

        if (len(colours) == 0):
            colours.append("rgb(0, 0, 0)")

        fig.add_trace(go.Scatter(
            name = label,
            x = list(range(1, days + 1)),
            y = dataToPlot[column],
            mode = "lines",
            line = dict(width=0.5, color=colours.pop()),
            #hoverinfo = "x+y+name",
            #hoverlabel=dict(bgcolor="rgb(255, 255, 255)"),
            stackgroup = "one"
            ))

    fig.update_layout(
            showlegend=True,
            title=go.layout.Title(text=selectedCategory),
            legend_title_text="Age Groups:",
            plot_bgcolor = "rgb(100, 100, 100)",
            xaxis=dict(
                title="Days"
                ),
            hovermode = "x"
        )
    if (showAsPercent):
        fig.update_layout(
            yaxis=dict(
                type='linear',
                ticksuffix='%',
                title="Percentage of population."
                ),
            )
    else:
        fig.update_layout(
            yaxis=dict(
                type='linear',
                title="Proportion of population."
                ),
            )
    return fig

if __name__ == '__main__':
    PieChart_CampParams.run_server(debug=True)      # Dash is running on http://127.0.0.1:8050/
