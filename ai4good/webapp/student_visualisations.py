# Please add your own visualisations to this file.
# Lay them out similarly to how they are in plotter.py so that they are modular and can be used in various places. (Each visualisation has its own subroutine.)
# Also if you could add a comment next to the definition of each subroutine with the names of the people who worked on it, that would be great. -Max
#------------------------------------------------------------------

import pandas as pd     
import plotly.express as px
import plotly.graph_objects as go

#Age breakdown stacked area chart -Max -----------------------------------------------------------------
def AgeBreakdown(category = None, days = 250, showAsPercent = False, df = None):
    categories = ["Susceptible", "Exposed", "Infected (symptomatic)", "Asymptomatically Infected", "Recovered", "Hospitalised", "Critical", "Deaths", "Offsite", "Quarantined", "No ICU Care"]
    ageCategories = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]
    if (df == None):
        data = pd.read_csv("..\\runner\\tests\\expected_report.csv") #Read the data from a csv file (model output can be exported as csv).
    else:
        data = df #Alternatively a DataFrame can be passed in containing the data.
    columns = []
    for item in data.columns:
        columns.append(item) #Generate a list of all category names

    try:
        categories.index(category)
        selectedCategory = category #Detect and check the selected category.
    except ValueError:
        selectedCategory = "Asymptomatically Infected" #If category invalid, choose Asymptomatically Infected.

    dataColumnIndexes = []
    dataColumnIndexesRemoval = []
    selectedCategory = selectedCategory + ":"
    dataColumnNames = []
    for i in range(0, len(columns)-1): #Get the names of all the columns which match the selected category in the DataFrame.
        testCategory = columns[i]
        if (testCategory[0:len(selectedCategory)] == selectedCategory):
            dataColumnNames.append(testCategory)

    dataToPlot = data[dataColumnNames].head(days).copy()
    if (showAsPercent):
        dataToPlot = dataToPlot.multiply(100).copy() #Multiply the decimal values by 100 if they are to be displayed as percentages.

    fig = go.Figure()
    x = dataToPlot.columns
    colours = ["rgb(0, 0, 252)", "rgb(33, 33, 252)", "rgb(66, 66, 252)", "rgb(99, 99, 252)", "rgb(132, 132, 252)", "rgb(165, 165, 252)", "rgb(198, 198, 252)", "rgb(211, 211, 252)"] #Colours for each age group.
    for column in dataToPlot.columns:
        label = str(column) #Set the label for the series to the column name if the column name doesn't contain an age range.
        for ageRange in ageCategories:
            if (ageRange in column):
                label = ageRange #Set the label for the series to the age group if the column name does contain an age range.
                break

        if (len(colours) == 0):
            colours.append("rgb(0, 0, 0)") #If the list of colours has run out, use black as a placeholder.

        fig.add_trace(go.Scatter(
            name = label,
            x = list(range(1, days + 1)), #Set the X data to be the number of days set in the parameter
            y = dataToPlot[column], #Set the Y data to be the data from the DataFrame
            mode = "lines",
            line = dict(width=0.5, color=colours.pop()), #Set the line colour and width.
            stackgroup = "one" #Make sure they are all in the same stackgroup so each line stacks on each other.
            ))

    fig.update_layout(
            showlegend=True, #Show the list of legends
            title=go.layout.Title(text=selectedCategory), #Set the chart title and
            legend_title_text="Age Groups:",
            plot_bgcolor = "rgb(100, 100, 100)", #Background colour for the chart - may need to be changed.
            xaxis=dict(
                title="Days" #Set the title for the x axis.
                ),
            hovermode = "x" #x unified doesn't work for some reason.
        )
    if (showAsPercent):
        fig.update_layout( #Adjust the y axis label and ticksuffix accordingly depending on whether percentages or decimals are chosen in the parameter.
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
    return fig #Return the Plotly figure.

#-------------------------------------------------------