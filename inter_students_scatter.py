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

    # splits data-frame
    df2018 = df.loc[df['year'] == 2018].head(800)

    # all international student percantages and ranking put into lists
    int_student_2018 = df2018['pct_intl_student'].tolist()
    ranking2018 = df2018['ranking'].tolist()
    uni_names = df2018['university_name'].tolist()

    # takes 0.xx to xx
    percent_int_student = [round(key1 * 100) for key1 in int_student_2018]

    data = {'int_student' : percent_int_student,
            'rank' : ranking2018,
            'uni_names' : uni_names
            }

    source = ColumnDataSource(data=data)

    p = figure(x_range=(0,800), y_range=(0, 100), plot_height=500, plot_width=1000, title="Percentage of international student in top 800 universities in 2018",
               x_axis_label ='Rank', y_axis_label = 'Percentage of international student (in %)', toolbar_location=None, tools="")

    # makes the scatterplot
    p.circle(ranking2018, percent_int_student, size=20, color="navy", alpha=0.5, line_width=1)

    # makes hover work
    hover = HoverTool(tooltips = [('%  of international students', "@int_student"),
                                 ('University rank', '@rank'),
                                 ('University', '@uni_names')
                                 ])

    p.add_tools(hover)

    output_file('docs/inter_student_scatter.html')

    show(p)
if __name__ == "__main__":
    main()
