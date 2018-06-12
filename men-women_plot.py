# shows the grades and amount of universities form 2016, 2017 and 2018
from bokeh.plotting import figure, output_file, show
from numpy import histogram
import pandas as pd
import numpy as np
from bokeh.layouts import column, row, widgetbox, WidgetBox, layout
from bokeh.models import Panel, ColumnDataSource, HoverTool
from bokeh.models.widgets import Tabs, CheckboxGroup, Slider
from bokeh.io import output_file, show, curdoc


uniranking = pd.read_csv('university_ranking.csv')

uniranking2018 = uniranking.loc[uniranking['year'] == 2018]

# Designs the histogram

plot2018 = figure(plot_width = 600, plot_height = 600, title ='Amount of universities with certain overall grades 2018',
x_axis_label ='Overall grade', y_axis_label = 'Amount of universities')

continents = ['Africa', 'Asia', 'America', 'Europe', 'Oceania']

# Makes a histogram from range 0 to 100 in steps of 2.
arr_hist2018, edges2018 = np.histogram(uniranking2018['score_overall'],
                               bins = continents,
                               range = [-20, 20])

# Put the information in a dataframe
scores2018 = pd.DataFrame({'score_overall2018': arr_hist2018,
                       'left2018': edges2018[:-1],
                       'right2018': edges2018[1:]})

src2018 = ColumnDataSource(scores2018)

# Designs the histogram
plot2018.quad(source = src2018, bottom=0, top='score_overall2018',
       left='left2018', right='right2018',
       fill_color='red', line_color='black', fill_alpha = 0.75,
       hover_fill_alpha = 1.0, hover_fill_color = 'navy')

# Makes the hover work
hover2018 = HoverTool(tooltips = [('Score', '@left2018 - @right2018'),
                             ('# of universities', '@score_overall2018')])

# Add the hover tool to the graph
plot2018.add_tools(hover2018)

layout = layout([plot2018])

# Show the plot
show(layout)
