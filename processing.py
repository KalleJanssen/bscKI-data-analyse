import pandas as pd
from collections import Counter
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure


def main():

	df = pd.read_csv('university_ranking.csv', index_col=0)

	# splits data into the three separate years
	columns_2016 = df.loc[df['year'] == 2016]
	columns_2017 = df.loc[df['year'] == 2017]
	columns_2018 = df.loc[df['year'] == 2018]

	# all countries in separate years
	country_list_2016 = columns_2016['country']
	country_list_2017 = columns_2017['country']
	country_list_2018 = columns_2018['country']

	# counts of countries in different years
	country_occurences_2016 = Counter(country_list_2016)
	country_occurences_2017 = Counter(country_list_2017)
	country_occurences_2018 = Counter(country_list_2018)

	# top 10 counts in different years
	ten_highest_2016 = country_occurences_2016.most_common(10)
	ten_highest_2017 = country_occurences_2017.most_common(10)
	ten_highest_2018 = country_occurences_2018.most_common(10)

	countries = []
	count = []
	data = {}
	years = ['2016']

	# goes through ten highest universities in 2016
	for k, v in ten_highest_2016:

		if len(k) > 10:
			initials = ''
			for name in k.split(' '):
			    initials += name[0]
			k = initials

		count.append(v)
		countries.append(k)


	data['countries'] = countries
	data['2016'] = count

	# list of tuples of country, year
	x = [ (country, year) for country in countries for year in years]
	counts = sum(zip(data['2016']), ())

	# creates the html source-file
	source = ColumnDataSource(data=dict(x=x, counts=counts))
	p = figure(x_range=FactorRange(*x), plot_height=250, title="Number of universities in ranking per year per country",
	           toolbar_location=None, tools="")
	p.vbar(x='x', top='counts', width=0.9, source=source)
	p.y_range.start = 0
	p.x_range.range_padding = 0.1
	p.xaxis.major_label_orientation = 1
	p.xgrid.grid_line_color = None
	output_file("bars.html")
	show(p)

if __name__ == "__main__":
	main()