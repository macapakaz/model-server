# Not the modular code
# Initial code for running visualisation locally with plotly and plotly dash
# Will be added to student_visualisation.py after refactoring

import pandas as pd     
import plotly.express as px
import plotly.graph_objects as go
import dash             
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

CampParams = dash.Dash(__name__)

#--------------------------------------------------------------------------------------
df_o = pd.read_csv("expected_report.csv")
df = pd.read_excel("camp_params.xlsx")
df_i = pd.read_excel("contact_matrix_params.xlsx")
df = df[df['Camp']=='Moria']                #Select the camp 'Moria' or 'Haman-al-Alil'

#-------------------------------Contact Matrix Graph--------------------------------
idn =df_i[:]['idx']     

fig_i = go.Figure(data=[
    go.Line(name='Age 0-10', x=idn, y=df_i[:8]['Age 0-10']),
    go.Line(name='Age 10-20', x=idn, y=df_i[:8]['Age 10-20']),
    go.Line(name='Age 20-30', x=idn, y=df_i[:8]['Age 20-30']),
    go.Line(name='Age 30-40', x=idn, y=df_i[:8]['Age 30-40'])
    ])
fig_i.update_layout(
    width = 1000,
    height = 600,
    
    title = "Contact Parameters",yaxis=dict(
                title='Total Population'),xaxis=dict(
                title='Time, Days',
                )
)
fig_i.update_layout(hovermode='closest')
#------------------------------Line graph for Disease Progression- Ages: 0-9-------------------------------------------------
idx =df_o[:]['idx_er']

fig = go.Figure(data=[
    go.Line(name='Susceptible: 0-9', x=idx, y=df_o[:]['Susceptible: 0-9']  ),
    go.Line(name='No ICU Care: 0-9', x=idx, y=df_o[:]['No ICU Care: 0-9']  ),
    go.Line(name='Recovered: 0-9', x=idx, y=df_o[:]['Recovered: 0-9']  ),
    go.Line(name='Quarantined: 0-9', x=idx, y=df_o[:]['Quarantined: 0-9']  ),
    go.Line(name='Critical: 0-9', x=idx, y=df_o[:]['Critical: 0-9']  ),
    go.Line(name='Deaths: 0-9', x=idx, y=df_o[:]['Deaths: 0-9']  ),
    go.Line(name='Exposed: 0-9', x=idx, y=df_o[:]['Exposed: 0-9']  ),
    go.Line(name='Infected (symptomatic): 0-9', x=idx, y=df_o[:]['Infected (symptomatic): 0-9']),
    go.Line(name='Asymptomatically Infected: 0-9', x=idx, y=df_o[:]['Asymptomatically Infected: 0-9'])
    ])
fig.update_layout(
    width = 1200,
    height = 600,
    
    title = "Parameters for Age Group: 0-9 (from expected result file)",yaxis=dict(
                title='Total Population (Age: 0-9)'),xaxis=dict(
                title='Time, Days',
                )
)
fig.update_layout(hovermode='closest')

#--------------------------------Line graph for Disease Progression- Ages: 0-9-------------------------------------------------------
fig2 = go.Figure(data=[
    go.Scatter(name='Susceptible: 10-19', x=idx, y=df_o[:]['Susceptible: 10-19']  ),
    go.Scatter(name='No ICU Care: 10-19', x=idx, y=df_o[:]['No ICU Care: 10-19']  ),
    go.Scatter(name='Recovered: 10-19', x=idx, y=df_o[:]['Recovered: 10-19']  ),
    go.Scatter(name='Quarantined: 10-19', x=idx, y=df_o[:]['Quarantined: 10-19']  ),
    go.Scatter(name='Critical: 10-19', x=idx, y=df_o[:]['Critical: 10-19']  ),
    go.Scatter(name='Deaths: 10-19', x=idx, y=df_o[:]['Deaths: 10-19']  ),
    go.Scatter(name='Exposed: 10-19', x=idx, y=df_o[:]['Exposed: 10-19']  ),
    go.Scatter(name='Infected (symptomatic): 10-19', x=idx, y=df_o[:]['Infected (symptomatic): 10-19']),
    go.Scatter(name='Asymptomatically Infected: 10-19', x=idx, y=df_o[:]['Asymptomatically Infected: 10-19'])
    ])
fig2.update_layout(
    width = 1200,
    height = 600,
    
    title = "Parameters for Age Group: 10-19 ",yaxis=dict(
                title='Total Population (Age: 10-19)'),xaxis=dict(
                title='Time, Days',
                )
)

#---------------------------------Graphs based on Camp Input Parameters-------------------------------------------------
CampParams.layout = html.Div([
    html.Div([
        dcc.Dropdown(id='piedropdown',
            options=[
                     {'label': 'Symptomatic', 'value': 'p_symptomatic'},
                     {'label': 'Hospitalized Symptomatic', 'value': 'Hosp_given_symptomatic'},
                     {'label':'Critical Hospitalized', 'value':'Critical_given_hospitalised'},
                     {'label':'Population Stucture', 'value':'Population_structure'},
                     {'label':'Chances of Symptomatic Cases becoming Critical', 'value':'Rough prob symptomatic case becomes critical'},
                     {'label':'Expected Critical Cases', 'value':'Rough exp. no. critical'}
            ],
            value='Population_structure',
            multi=False,
            clearable=False
        ),
        ]),
        html.Div([
            dcc.Graph(id='piechart'),
        ]),
      
       
        html.Div([
            dcc.Dropdown(id='linedropdown',
                options=[
                          {'label': 'Symptomatic', 'value': 'p_symptomatic'},
                     {'label': 'Hospitalized Symptomatic', 'value': 'Hosp_given_symptomatic'},
                     {'label':'Critical Hospitalized', 'value':'Critical_given_hospitalised'},
                     {'label':'Population Stucture', 'value':'Population_structure'},
                     {'label':'Chances of Symptomatic Cases becoming Critical', 'value':'Rough prob symptomatic case becomes critical'},
                     {'label':'Expected Critical Cases', 'value':'Rough exp. no. critical'}
                ],
                value='Population_structure',
                multi=False,
                clearable=False
            )
            ]),
       
  
     
        html.Div([
            dcc.Graph(id='linechart'),
        ]),
        
        
        html.Div([
            dcc.Graph(figure=fig_i),
        ]),
         html.Div([
            dcc.Graph(figure=fig),
        ]),
        
        html.Div([
            dcc.Graph(figure=fig2)
        ])
])

#-----------------------------------------------------------------------------------------------------------------
@CampParams.callback(
   [ Output('piechart', 'figure'),
     Output('linechart', 'figure')],
     [Input('piedropdown', 'value'),Input('linedropdown', 'value')],   
)
def update_graphs(piedropdown, linedropdown):
    dff=df
    pie_chart=px.pie(
            data_frame=dff,
            names='Age',
            values=piedropdown,
            hover_name='Age',
            hole=.25,
            title='Plotting Input Camp Parameters', 
            hover_data=['Camp'],
            width=800,
            height=600
             )
    pie_chart.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    
   line_chart = px.bar(
            data_frame=dff,
            x='Age',
            y=linedropdown,
            color='Age',
            title='Bar Graph: Input Camp Parameters', 
            )
    line_chart.update_layout( width = 900, height= 600, uirevision='foo')
   
    return (pie_chart, line_chart)
    
#-----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    CampParams.run_server(debug=True)
