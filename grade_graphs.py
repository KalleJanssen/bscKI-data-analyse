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
year2016 = 2016
uniranking2016 = uniranking.loc[uniranking['year'] == int(year2016)]

p2016 = figure(plot_width = 600, plot_height = 600, title ='Amount of universities with certain overall grades 2016',
x_axis_label ='Overall grade', y_axis_label = 'Amount of universities')

# Makes a histogram from range 0 to 100 in steps of 2.
arr_hist2016, edges2016 = np.histogram(uniranking2016['score_overall'],
                               bins = int(100/2),
                               range = [0, 100])


# Put the information in a dataframe
scores2016 = pd.DataFrame({'score_overall2016': arr_hist2016,
                       'left2016': edges2016[:-1],
                       'right2016': edges2016[1:]})

src2016 = ColumnDataSource(scores2016)

# Designs the histogram
p2016.quad(source = src2016, bottom=0, top='score_overall2016',
       left='left2016', right='right2016',
       fill_color='red', line_color='black', fill_alpha = 0.75,
       hover_fill_alpha = 1.0, hover_fill_color = 'navy')

# Makes the hover work
hover = HoverTool(tooltips = [('Score', '@left2016 - @right2016'),
                             ('Amount of universities', '@score_overall2016')])

# Add the hover tool to the graph
p2016.add_tools(hover)


#2017
year2017 = 2017
uniranking2017 = uniranking.loc[uniranking['year'] == int(year2017)]

p2017 = figure(plot_width = 600, plot_height = 600, title ='Amount of universities with certain overall grades 2017',
x_axis_label ='Overall grade', y_axis_label = 'Amount of universities')

# Makes a histogram from range 0 to 100 in steps of 2.
arr_hist2017, edges2017 = np.histogram(uniranking2017['score_overall'],
                               bins = int(100/2),
                               range = [0, 100])


# Put the information in a dataframe
scores2017 = pd.DataFrame({'score_overall2017': arr_hist2017,
                       'left2017': edges2017[:-1],
                       'right2017': edges2017[1:]})

src2017 = ColumnDataSource(scores2017)

# Designs the histogram
p2017.quad(source = src2017, bottom=0, top='score_overall2017',
       left='left2017', right='right2017',
       fill_color='red', line_color='black', fill_alpha = 0.75,
       hover_fill_alpha = 1.0, hover_fill_color = 'navy')

# Makes the hover work
hover = HoverTool(tooltips = [('Score', '@left2017 - @right2017'),
                             ('Amount of universities', '@score_overall2017')])

# Add the hover tool to the graph
p2017.add_tools(hover)



#2018
year2018 = 2018
uniranking2018 = uniranking.loc[uniranking['year'] == int(year2018)]

p2018 = figure(plot_width = 600, plot_height = 600, title ='Amount of universities with certain overall grades 2018',
x_axis_label ='Overall grade', y_axis_label = 'Amount of universities')

# Makes a histogram from range 0 to 100 in steps of 2.
arr_hist2018, edges2018 = np.histogram(uniranking2018['score_overall'],
                               bins = int(100/2),
                               range = [0, 100])


# Put the information in a dataframe
scores2018 = pd.DataFrame({'score_overall2018': arr_hist2018,
                       'left2018': edges2018[:-1],
                       'right2018': edges2018[1:]})

src2018 = ColumnDataSource(scores2018)

# Designs the histogram
p2018.quad(source = src2018, bottom=0, top='score_overall2018',
       left='left2018', right='right2018',
       fill_color='red', line_color='black', fill_alpha = 0.75,
       hover_fill_alpha = 1.0, hover_fill_color = 'navy')

# Makes the hover work
hover = HoverTool(tooltips = [('Score', '@left2018 - @right2018'),
                             ('Amount of universities', '@score_overall2018')])

# Add the hover tool to the graph
p2018.add_tools(hover)


layout = layout([p2016, p2017, p2018])

# Show the plot
show(layout)
