# Please add your own visualisations to this file.
# Lay them out similarly to how they are in plotter.py so that they are modular and can be used in various places. (Each visualisation has its own subroutine.)
# Also if you could add a comment next to the definition of each subroutine with the names of the people who worked on it, that would be great. -Max
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

