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
        data = df #Alternatively a Pandas DataFrame can be passed in containing the data.
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
                title="Percentage of population"
                ),
            )
    else:
        fig.update_layout(
            yaxis=dict(
                type='linear',
                title="Proportion of population"
                ),
            )
    return fig #Return the Plotly figure.

#-------------------------------------------------------

def get_sunburst_values(df):
        df["Population"] = (((df["Population_structure"]*df["Total_population"][1]))/100).astype('int64')
        df["Symptomatic"] = (df["p_symptomatic"] * df["Population"]).astype('int64') 
        df["Non_symptomatic"] = df["Population"] - df["Symptomatic"]
        df["Symptomatic_hospitalised"] = ((df["Symptomatic"] * df["Hosp_given_symptomatic"])/100).astype('int64')
        df["Symptomatic_unhospitalised"] = df["Symptomatic"] - df["Symptomatic_hospitalised"]
        df["Symptomatic_critical"] = ((df["Symptomatic_hospitalised"] * df["Critical_given_hospitalised"])/100).astype('int64')
        df["hospitalised_expected_critical"] = df["Rough exp. no. critical"].astype(float).astype('int64')
        df["Symptomatic_hospitalised"] -= df["Symptomatic_critical"] + df["hospitalised_expected_critical"]
        df = df.drop(["Camp", "Rough prob symptomatic case becomes critical (just multiplying)", 
            "Rough exp. no. critical", "Notes:", "Total_population", "Population_structure", "p_symptomatic", 
            "Population", "Symptomatic", "Hosp_given_symptomatic", "Critical_given_hospitalised"], axis=1)
        totals = pd.concat([pd.DataFrame(["Total"]), df.sum(axis=0)[1:]]).rename(index={0: 'Age'}).T
        df = df.append(totals)

        categories = ["Non-Symptomatic", "Symptomatic, Hospitalised", "Symptomatic Unhospitalised", "Symptomatic, Critical", "Hospitalised, Expected To Turn Critical"]
        ages = [f"{10 * i}-{10 * i + 9}" for i in range(7)] + ["70+"]
        labels = categories + [f"{category} ({age})" for age in ages for category in categories]
        parents = ["" for i in range(len(categories))] + [category for age in ages for category in categories]
        values_totals = [df[category][df["Age"] == "Total"][0] for category in df.columns.to_list()[1:]]
        values_ages = [df[category][df["Age"] == age].item() for age in ages for category in df.columns.to_list()[1:]]
        values = values_totals + values_ages

        return labels, parents, values

def generate_sunburst(labels, parents, values):

    sunburst = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
    ))
    sunburst.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    sunburst.update_traces(marker=dict(line=dict(color='#000000', width=1)))
    return sunburst

#------------------------------------------------------------------------------------------------------------------#
# Rate of change of <category> graph using Max's stacked area chart design -Alex ----------------------------------#
def DifferentialGraph(category= None, days = None, showAsPercent = None, df = None, scale = "linear"):
    
    if days == None:
        days = 200 # changed to 200 as expected csv is 200 days
    if showAsPercent == None:
        showAsPercent = True
    if category == None:
        selectedCategory = "Infected (symptomatic)" #If category invalid, choose smptomatically Infected.
    else:
        selectedCategory = category 


    # Blatently stole this from max's stacked area chart code
    categories = ["Susceptible", "Exposed", "Infected (symptomatic)", "Asymptomatically Infected", "Recovered", "Hospitalised", "Critical", "Deaths", "Offsite", "Quarantined", "No ICU Care"]
    ageCategories = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"] # added blank age category (differnt to max's original) to allow for totals removed for debugging
    if (df == None):
        data = pd.read_csv("expected_report.csv") #Read the data from a csv file (model output can be exported as csv).
    else:
        data = df #Alternatively a DataFrame can be passed in containing the data.
    columns = []
    for item in data.columns:
        columns.append(item) #Generate a list of all category names

    dataColumnNames = []
    for i in range(0, len(columns)-1): #Get the names of all the columns which match the selected category in the DataFrame.
        testCategory = columns[i]
        if (testCategory[0:len(selectedCategory)] == selectedCategory):
            dataColumnNames.append(testCategory)

    yDataFrame = data[dataColumnNames].head(days).copy() # head returns only first operand number of terms

    # Will attempt to create an approximation of a differential graph by finding the increase per day
    def create_differential(yData):
        dyData = []
        for i in range(0,days-1):
            try:
                y_previous = 0.0
                y_previous = yData[i-1] # set previous term to previous term
            except IndexError: # uses 0 as previous term when accessing the 0th item in yData
                y_previous = 0.0
        
            y_current = yData[i]
        
            dyData.append((y_current-y_previous))
        return dyData


    fig = go.Figure()
    colours = ["rgb(0, 0, 252)", "rgb(33, 33, 252)", "rgb(66, 66, 252)", "rgb(83, 83, 252)", "rgb(99, 99, 252)", "rgb(132, 132, 252)", "rgb(165, 165, 252)", "rgb(198, 198, 252)", "rgb(211, 211, 252)"] #Colours for each age group.
    
    # Create a scatter diagram line for each age category
    for column in yDataFrame:
        label = "Total " + str(column) #Set the label for the series to the column name if the column name doesn't contain an age range.
        for ageRange in ageCategories:
            if (ageRange in column):
                label = ageRange #Set the label for the series to the age group if the column name does contain an age range.
                
        yData = list(yDataFrame[column])
        dyData=create_differential(yData)
        #multiply values by 100 to get % 
        if showAsPercent:
            for i in range(len(dyData)):
                dyData[i] = 100*dyData[i]
                
        fig.add_trace(go.Scatter(
            name = label,
            x = list(range(1, days + 1)), # set x to be number of days in parameter file
            y = create_differential(yData), # set y to calculated dyData
            mode = "lines",
            line = dict(width=0.5, color=colours.pop()), #Set the line colour and width.
            stackgroup = "one" #Make sure they are all in the same stackgroup so each line stacks on each other.
        ))
    
    if scale == "log":
        logText = "Logarithmic "
    else:
        logText = ""
    #update fig with new graph traces
    fig.update_layout(
            showlegend=True, #Show the list of legends
            title=go.layout.Title(text=(logText +"Rate of Change of " + selectedCategory)), #Set the chart title to selected category
            legend_title_text="Age Groups:",
            plot_bgcolor = "rgb(100, 100, 100)", #Background colour for the chart - may need to be changed.
            xaxis=dict(
                title="Days" #Set the title for the x axis.
                ),
            hovermode = "x" #x unified doesn't work for some reason.
        )
    
    if (showAsPercent):
        if scale == "log":
            titleScale = "Logarithmic Rate of Change of Percentage of population"
        else:
            titleScale = "Rate of Change of Percentage of population"

        fig.update_layout( #Adjust the y axis label and ticksuffix accordingly depending on whether percentages or decimals are chosen in the parameter.
            yaxis=dict(
                type=scale,
                ticksuffix='%',
                title=titleScale
                ),
            )
    else:
        if scale == "log":
            titleScale = "Logarithmic Rate of Change of Proportion of population"
        else:
            titleScale = "Rate of Change of Proportion of population" 

        fig.update_layout(
            yaxis=dict(
                type=scale,
                title=titleScale
                ),
            )

    return fig
