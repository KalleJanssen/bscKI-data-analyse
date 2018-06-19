import pandas as pd
import numpy as np
import helper
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file, curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import PreText, Select


def drop_change(atrrname, old, new):

	update_bar_chart()

def update_bar_chart():

	data = get_data_bar_chart(selection.value)
	source.data = source.from_df(data[['region', 'list2016', 'list2017', 'list2018']])
	
	# updates table
	update_table(data)

	# updates plot title and x_range
	column_bar_split.title.text = 'Count of universities per region in %s' % (continent)
	column_bar_split.x_range.factors = data['region'].tolist()


def update_table(data):

	table.text = str(data[['region', '2016', '2017', '2018', 'mean', 'std']])


def get_data_bar_chart(continent):

	df = pd.read_csv('../university_ranking.csv', index_col=0)

	df = df.loc[df['continent'] == continent]

	regions = list(set(df['region'].tolist()))

	years = [2016, 2017, 2018]

	dfs = [df.loc[df['year'] == year] for year in years]
	
	# all continents counter and put into dictionaries
	count_2016 = dict(Counter(dfs[0]['region'].tolist()))
	count_2017 = dict(Counter(dfs[1]['region'].tolist()))
	count_2018 = dict(Counter(dfs[2]['region'].tolist()))
	# fills in missing datapoint
	if continent == 'Africa':

		count_2018['Western Africa'] = 0

	# lists of counts in corrrect order as outlined above
	data = pd.DataFrame()
	data['region']   = regions
	data['list2016'] = [count_2016[key] for key in regions]
	data['list2017'] = [count_2017[key] for key in regions]
	data['list2018'] = [count_2018[key] for key in regions]
	data['mean'] = data[['list2016', 'list2017', 'list2018']].mean(axis=1)
	data['std']  = data[['list2016', 'list2017', 'list2018']].std(axis=1)
	data[['mean', 'std']] = data[['mean', 'std']].astype(int)

	return data 

# set up widgets
table = PreText(text='', width=500)
static_table = PreText(text='', width=500)
selection = Select(value='America', options=['America', 'Europe', 'Asia', 'Oceania', 'Africa'] )

# set up hover
hover = HoverTool(
            tooltips=[('No. of Universities', '@list2016')])

# set up plots
source = ColumnDataSource(data=dict(region=[], list2016=[], list2017=[], list2018=[]))
column_bar_split = figure(y_range=(0, 400), x_range=[],
		   plot_height=250, plot_width=700, tools=[])
column_bar_split.vbar(x=dodge('region', -0.25, range=column_bar_split.x_range), top='list2016', width=0.2, source=source,
   color="#c9d9d3", legend=value("2016"))
column_bar_split.vbar(x=dodge('region',  0.0,  range=column_bar_split.x_range), top='list2017', width=0.2, source=source,
   color="#718dbf", legend=value("2017"))
column_bar_split.vbar(x=dodge('region',  0.25, range=column_bar_split.x_range), top='list2018', width=0.2, source=source,
   color="#e84d60", legend=value("2018"))
column_bar_split.legend.location = 'top_right'
column_bar_split.legend.orientation = 'horizontal'

# on change switch values
selection.on_change('value', drop_change)

# gets static plot and table string from helper.py
static_col, static_table_data = helper.bar_chart_continent_split()
static_table.text = str(static_table_data)

# lays out the widgets and columns
widgets = column(selection, table)
main_row = row(column_bar_split, widgets)
secondary_row = row(static_col, static_table)
layout = column(main_row, secondary_row)

# initial update
update_bar_chart()

curdoc().add_root(layout)
curdoc().title = 'Region Split'