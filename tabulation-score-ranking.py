import plotly.plotly as py
import pandas as pd
import plotly.offline
import plotly.graph_objs as go
from math import sqrt
from collections import Counter


plotly.tools.set_credentials_file(username='arnitro', api_key='foCkT4Qrj9x1F73nuvBw')


def mean_sd(list):
	num_items = len(list)
	mean = sum(list) / num_items
	differences = [x - mean for x in list]
	sq_differences = [d ** 2 for d in differences]
	ssd = sum(sq_differences)

	variance = ssd / num_items

	sd = sqrt(variance)

	return mean, sd

def main():

	df = pd.read_csv('university_ranking.csv', index_col=0)

	continents = ['Europe', 'America', 'Asia', 'Oceania', 'Africa']      

	df2016 = df.loc[df['year'] == 2016]
	df2017 = df.loc[df['year'] == 2017]
	df2018 = df.loc[df['year'] == 2018]

	# all continents put into lists
	continents_2016 = df2016['continents'].tolist()
	continents_2017 = df2017['continents'].tolist()
	continents_2018 = df2018['continents'].tolist()

	# all continents counter and put into dictionaries
	count_2016 = dict(Counter(continents_2016))
	count_2017 = dict(Counter(continents_2017))
	count_2018 = dict(Counter(continents_2018))

	# lists of counts in corrrect order as outlined above
	list2016 = [count_2016[key] for key in continents]
	list2017 = [count_2017[key] for key in continents]
	list2018 = [count_2018[key] for key in continents]

	data = {}

	# append required data for mean and sd to dictionary
	for i, continent in enumerate(continents):
		data[continent] = [list2016[i], list2017[i], list2018[i]]

	means = []
	sds = []

	# calculates mean and sd between years for every given continent
	for country in data:
		mean, sd = mean_sd(data[country])
		mean = round(mean, 2)
		sd = round(sd, 2)
		means.append(mean)
		sds.append(sd)

	mean_ranking = []
	sd_ranking = []
			

	trace = go.Table(
			header=dict(values=['Continent', '2016', '2017', '2018', 'mean', 'sd'],
			line = dict(color='#000000'),
			fill = dict(color='#B5DBE8')),
			cells=dict(values=[continents, list2016, list2017, list2018, means, sds],
				fill = dict(color='#EDEDED')))

	layout = dict(width=500, height=500)
	data = [trace]
	fig = dict(data=data, layout=layout)
	plotly.offline.plot(fig, filename = 'docs/styled_table.html')

if __name__ == "__main__":
	main()  