# shows a simple plot to test if bokeh is working properly
from bokeh.plotting import figure, output_file, show
from numpy import histogram
import pandas as pd
import numpy as np
from bokeh.layouts import column, row, widgetbox, WidgetBox, layout
from bokeh.models import Panel, ColumnDataSource, HoverTool
from bokeh.models.widgets import Tabs, CheckboxGroup, Slider
from bokeh.io import output_file, show, curdoc

year = input("Which year do you want to look at? ")

uniranking1 = pd.read_csv('university_ranking.csv')
if year == 'all':
    uniranking = uniranking1
elif '2016' or '2017' or '2018':
    uniranking = uniranking1.loc[uniranking1['year'] == int(year)]
else:
    year = input("Please choose 2016, 2017, 2018 or all.")

p = figure(plot_width = 600, plot_height = 600, title ='University grade and ranking correlation',
x_axis_label ='Overall grade', y_axis_label = 'Amount of universities')

# Makes a histogram from range 0 to 100 in steps of 2.
arr_hist, edges = np.histogram(uniranking['score_overall'],
                               bins = int(100/2),
                               range = [0, 100])


# Put the information in a dataframe
scores = pd.DataFrame({'score_overall': arr_hist,
                       'left': edges[:-1],
                       'right': edges[1:]})

src = ColumnDataSource(scores)

# Designs the histogram
p.quad(source = src, bottom=0, top='score_overall',
       left='left', right='right',
       fill_color='red', line_color='black', fill_alpha = 0.75,
       hover_fill_alpha = 1.0, hover_fill_color = 'navy')

# Makes the hover work
hover = HoverTool(tooltips = [('Score', '@left - @right'),
                             ('Amount of universities', '@score_overall')])


# Add the hover tool to the graph
p.add_tools(hover)

def update(attr, old, new):
    year = slider.value
    new_data = {
        'x'       : uniranking.loc[year].ranking,
        'y'       : uniranking.loc[year].score_overall,
    }
    scores = new_data

slider = Slider(start=2016, end=2018, value=2016, step=1, title="Year")
slider.on_change('value', update)

# Show the plot
layout = layout(widgetbox(slider), p)
curdoc().add_root(layout)

# Show the plot
show(layout)
