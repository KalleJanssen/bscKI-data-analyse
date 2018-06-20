import pandas as pd
import numpy as np
import country_converter as coco
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge


def main():

    output_file('../docs/region_comparision.html')

    df = pd.read_csv('../university_ranking.csv', index_col=0)

    years = [2016, 2017, 2018]

    regions = ['Northern America', 'South America', 'Central America',
               'Northern Europe', 'Western Europe', 'Southern Europe',
               'Eastern Europe', 'South-Eastern Asia', 'Western Asia',
               'Southern Asia', 'Eastern Asia', 'Southern Africa',
               'Eastern Africa', 'Northern Africa', 'Western Africa',
               'Australia and New Zealand']

    regions_abbrv = ['N-AME', 'S-AME', 'C-AME', 'N-EUR', 'W-EUR', 'S-EUR',
                     'E-EUR', 'SE-ASIA', 'W-ASIA', 'S-ASIA', 'E-ASIA',
                     'S-AFR', 'E-AFR', 'N-AFR', 'W-AFR', 'ANZ']

    dfs = [df.loc[df['year'] == year].head(800) for year in years]

    # all continents counter and put into dictionaries
    count_2016 = dict(Counter(dfs[0]['region'].tolist()))
    count_2017 = dict(Counter(dfs[1]['region'].tolist()))
    count_2018 = dict(Counter(dfs[2]['region'].tolist()))
    count_2018['Western Africa'] = 0

    # lists of counts in corrrect order as outlined above
    list2016 = [count_2016[key] for key in regions]
    list2017 = [count_2017[key] for key in regions]
    list2018 = [count_2018[key] for key in regions]

    # dictionary with data for making a figure
    data = {'continents': regions_abbrv,
            '2016': list2016,
            '2017': list2017,
            '2018': list2018}

    source = ColumnDataSource(data=data)
    p = figure(x_range=regions_abbrv, y_range=(0, 400), plot_height=250, 
               plot_width=1000, title="University count per region per year",
               toolbar_location='below', tools="pan,wheel_zoom,box_zoom,reset")

    p.vbar(x=dodge('continents', -0.25, range=p.x_range),
           top='2016', width=0.2, source=source,
           color="#c9d9d3", legend=value("2016"))

    p.vbar(x=dodge('continents',  0.0,  range=p.x_range),
           top='2017', width=0.2, source=source,
           color="#718dbf", legend=value("2017"))

    p.vbar(x=dodge('continents',  0.25, range=p.x_range),
           top='2018', width=0.2, source=source,
           color="#e84d60", legend=value("2018"))

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"

    show(p)


if __name__ == "__main__":
    main()
