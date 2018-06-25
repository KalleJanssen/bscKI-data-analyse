import pandas as pd
import numpy as np
import country_converter as coco
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge



# def best_fit_line(xs, ys):

#     m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
#          ((mean(xs)*mean(xs)) - mean(xs*xs)))

#     b = mean(ys) - m*mean(xs)

#     return m, b


def main():

    # file where .html should be saved
    output_file('docs/GDP_scatter.html',
                title='Scatterplot: GDP x Ranking')

    # reads df from file
    df = pd.read_csv('university_ranking.csv', index_col=0)
    df_gdp = pd.read_csv('GDP.csv', index_col=0)

    colormap = {2016: 'red',
                2017: 'green',
                2018: 'blue'}

    years = [2016, 2017, 2018]

    # country_list = df['country'].tolist()
   


    # gets top 800 for every year and puts into list

    # for country in country_list:
    df2016 = df.loc[df['year']==2016].head(20)

    countries = set(df2016['country'].tolist())
    # print(countries)

    
    print(df2016['country'],df2016['ranking'])

    # rank=0
    # i=0
    # for country in countries:
    #     lol = df2016.loc[df2016['country']]
    #     print(lol)
        # rank += df2016['ranking']
        # print(country)
        # print(rank)

        # if country == df2016['country']:
        #     print(df2016['ranking'])

 
    

 

    # df = dfs[0].append(dfs[1].append(dfs[2]))

    # count_2016 = dict(Counter(df2016['country'].tolist()))
    # print(count_2016)





    




    # print(df2016['country'])
    # for country in country_list:
    #     for df2016['country']

    #     rank_2016 = dict(Counter(df2016['ranking'].tolist()))
    #     print(country)
    #     print(rank_2016)

    # # # changes float to integer for more correct scatterplot
    # df['pct_intl_student'] = df['pct_intl_student'] * 100
    # df.pct_intl_student = df.pct_intl_student.astype(int)

    # # creates all data we need
    # year_list = []

    # # creates list of years for every datapoint
    # for year in years:
    #     for i in range(800):
    #         year_list.append(year)

    # # creates list of colors for every datapoint
    # colors = [colormap[x] for x in df['year']]

    # # all data collected in a dictionary
    # data = {
    #         'ranking': df['ranking'],
    #         'pct_intl_student': df['pct_intl_student'],
    #         'years': year_list,
 

if __name__ == "__main__":
    main()
