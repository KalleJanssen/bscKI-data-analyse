import pandas as pd
import numpy as np
import helper
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file, curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import row, column
from bokeh.models.widgets import PreText, Select


def bar_chart_continent_split():

    # reads df from file
    df = pd.read_csv('../university_ranking.csv', index_col=0)

    # splits data-frame into top 800 data-frames per year
    df2016 = df.loc[df['year'] == 2016].head(800)
    df2017 = df.loc[df['year'] == 2017].head(800)
    df2018 = df.loc[df['year'] == 2018].head(800)

    dfs = [df2016, df2017, df2018]

    # continent order that I wanted
    continents = ['Europe', 'America', 'Asia', 'Oceania', 'Africa']

    list = []

    # all years
    years = ['2016', '2017', '2018']

    # all continents put into lists
    continents_2016 = df2016['continent'].tolist()
    continents_2017 = df2017['continent'].tolist()
    continents_2018 = df2018['continent'].tolist()

    # all continents counter and put into dictionaries
    count_2016 = dict(Counter(continents_2016))
    count_2017 = dict(Counter(continents_2017))
    count_2018 = dict(Counter(continents_2018))

    # lists of counts in corrrect order as outlined above
    list2016 = [count_2016[key] for key in continents]
    list2017 = [count_2017[key] for key in continents]
    list2018 = [count_2018[key] for key in continents]

    # dictionary with data for making a figure
    data = {'continents': continents,
            '2016': list2016,
            '2017': list2017,
            '2018': list2018}

    source = ColumnDataSource(data=data)

    p = figure(x_range=continents, y_range=(0, 450), plot_height=250, plot_width=700, title="University count per continent per year",
               toolbar_location=None, tools="")

    p.vbar(x=dodge('continents', -0.25, range=p.x_range), top='2016', width=0.2, source=source,
           color="#c9d9d3", legend=value("2016"))

    p.vbar(x=dodge('continents',  0.0,  range=p.x_range), top='2017', width=0.2, source=source,
           color="#718dbf", legend=value("2017"))

    p.vbar(x=dodge('continents',  0.25, range=p.x_range), top='2018', width=0.2, source=source,
           color="#e84d60", legend=value("2018"))

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"

    data_frame = pd.DataFrame.from_dict(data)

    data_frame['mean'] = data_frame.mean(axis=1)
    data_frame['std'] = data_frame.std(axis=1)
    data_frame[['mean', 'std']] = data_frame[['mean', 'std']].astype(int)

    return p, data_frame
