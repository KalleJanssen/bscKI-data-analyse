import plotly.plotly as py
import pandas as pd

import plotly.offline
plotly.tools.set_credentials_file(username='arnitro', api_key='foCkT4Qrj9x1F73nuvBw')

df = pd.read_csv('university_country.csv')
data = [ dict(
        type = 'choropleth',
        locations = df['CODE'],
        z = df['TOTAL'],
        text = df['COUNTRY'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Number of universities'),
      ) ]

layout = dict(
    title = 'Nunber of universities in the ranking per country',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
plotly.offline.plot(fig,validate=False,filename = 'docs/map.html')    