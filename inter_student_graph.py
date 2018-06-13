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
    df2018 = df.loc[df['year'] == 2018].head(200)

    # all international student percantages and ranking put into lists
    int_student_2018 = df2018['pct_intl_student'].tolist()
    ranking2018 = df2018['ranking'].tolist()

    # takes 0.xx to xx
    percent_int_student = [round(key1 * 100) for key1 in int_student_2018]

    data = {'int_student' : percent_int_student,
            'rank' : ranking2018
            }

    source = ColumnDataSource(data=data)

    p = figure(x_range=(0,200), y_range=(0, 100), plot_height=500, plot_width=1000, title="Percentage of international student in top 200 universities in 2018",
               x_axis_label ='Rank', y_axis_label = 'Percentage of international student (in %)', toolbar_location=None, tools="")

    p.vbar(x=dodge('rank', 0, range=p.x_range), top='int_student', width=0.2, source=source,
           color="#0000FF", legend=value("Inhabitants per university"))

    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"

    # makes hover work
    hover = HoverTool(tooltips = [('%  of international students', "@int_student"),
                                 ('University rank', '@rank')])

    p.add_tools(hover)

    output_file('docs/inter_student_graph.html')

    show(p)
if __name__ == "__main__":
    main()
