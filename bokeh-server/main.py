import pandas as pd
import numpy as np
import helper
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file, curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import PreText, Select



def get_data(continent):

	df = pd.read_csv('../university_ranking.csv', index_col=0)

	df = df.loc[df['continent'] == continent]

	regions = list(set(df['region'].tolist()))

	years = [2016, 2017, 2018]
	dfs = [df.loc[df['year'] == year] for year in years]
	
	# all continents counter and put into dictionaries
	count_2016 = dict(Counter(dfs[0]['region'].tolist()))
	count_2017 = dict(Counter(dfs[1]['region'].tolist()))
	count_2018 = dict(Counter(dfs[2]['region'].tolist()))
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

# continent order that I wanted
continents = ['America', 'Europe', 'Asia', 'Oceania', 'Africa']      

# set up widgets
stats = PreText(text='', width=500)
r_stats = PreText(text='', width=500)
selection = Select(value='America', options=continents)

# set up plots

source = ColumnDataSource(data=dict(region=[], list2016=[], list2017=[], list2018=[]))

regions = continents

p = figure(y_range=(0, 400), x_range=regions,
		   plot_height=250, plot_width=700, tools=[])

p.vbar(x=dodge('region', -0.25, range=p.x_range), top='list2016', width=0.2, source=source,
   color="#c9d9d3", legend=value("2016"))
p.vbar(x=dodge('region',  0.0,  range=p.x_range), top='list2017', width=0.2, source=source,
   color="#718dbf", legend=value("2017"))
p.vbar(x=dodge('region',  0.25, range=p.x_range), top='list2018', width=0.2, source=source,
   color="#e84d60", legend=value("2018"))

p.legend.location = 'top_right'
p.legend.orientation = 'horizontal'


def drop_change(atrrname, old, new):
	update()


def update(selected=None):

	continent = selection.value
	data = get_data(continent)
	source.data = source.from_df(data[['region', 'list2016', 'list2017', 'list2018']])
	
	update_stats(data)

	p.title.text = 'Count of universities per region in %s' % (continent)
	p.x_range.factors = data['region'].tolist()

selection.on_change('value', drop_change)

def update_stats(data):


	data2 = data.copy()
	data2.columns = ['region', '2016', '2017', '2018', 'mean', 'std']

	stats.text = str(data2)

def selection_change(attrname, old, new):
	continent = selection.value
	data = get_data(continent)
	selected = source.selected.indices
	if selected:
		data = data.iloc[selected, :]
	update_stats(data)

source.on_change('selected', selection_change)

r, r_data = helper.bar_chart_continent_split()

r_stats.text = str(r_data)


widgets = column(selection, stats)
main_row = row(p, widgets)
secondary_row = row(r, r_stats)
layout = column(main_row, secondary_row)

update()

curdoc().add_root(layout)
curdoc().title = 'Region Split'