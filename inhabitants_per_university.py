import pandas as pd
import numpy as np
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import Panel, ColumnDataSource, HoverTool

def main():

    # reads df from file
    df = pd.read_csv('university_ranking.csv', index_col=0)

    output_file('docs/inhabitants-per-university.html')

    # splits data-frame
    df2018 = df.loc[df['year'] == 2018]

    # 2018
    years = ['2018']

    # all continents put into lists
    continents_2018 = df2018['continents'].tolist()

    # all continents counter and put into dictionaries
    count_2018 = dict(Counter(continents_2018))

    # continent order that I wanted
    continents = ['Africa', 'Asia', 'America', 'Europe', 'Oceania']

    # inhabitants of each continent
    count_20181 = {'Europe': 738849000, 'America': 1001559000, 'Asia': 4436224000, 'Africa' : 1216130000, 'Oceania' : 39901000}

    # lists of counts in corrrect order as outlined above
    list2018 = [count_20181[key]/count_2018[key] for key in continents]

    # lists of amount of inhabitants in corrrect order as outlined above
    listinhabitants = [count_20181[key] for key in continents]

    # lists of amount of universities in corrrect order as outlined above
    listuniversities = [count_2018[key] for key in continents]

    # dictioanry with data for making a figure
    data = {'continents' : continents,
            '2018' : list2018,
            'listinhabitants' : listinhabitants,
            'listuniversities': listuniversities}

    source = ColumnDataSource(data=data)

    p = figure(x_range=continents, y_range=(0, 50000000), plot_height=500, title="Number of inhabitants per continent per university",
               x_axis_label ='Continents', y_axis_label = 'Amount of inhabitants per university', toolbar_location=None, tools="")

    p.vbar(x=dodge('continents', 0, range=p.x_range), top='2018', width=0.2, source=source,
           color="#0000FF", legend=value("Inhabitants per university"))

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"

    hover = HoverTool(tooltips = [('Inhabitants', "@listinhabitants"),
                                 ('Amount of universities', '@listuniversities'),
                                 ('Number of inhabitants per university', '@2018{int}')])

    p.add_tools(hover)

    # disables the scientific notation of numbers
    p.left[0].formatter.use_scientific = False

    output_file('docs/inhabitants_per_university.html')
    
    show(p)

if __name__ == "__main__":
    main()
