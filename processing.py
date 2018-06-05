import pandas as pd
from collections import Counter
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure

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

