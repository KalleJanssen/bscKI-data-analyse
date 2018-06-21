import pandas as pd
import numpy as np
import helper
from statistics import mean
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file, curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import FactorRange, Range1d, Plot
from bokeh.models import Rect, CategoricalAxis, LinearAxis, GlyphRenderer
from bokeh.plotting import figure, gridplot
from bokeh.transform import dodge
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.models.widgets import PreText, Select, Slider


def best_fit_line(xs, ys):

    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))

    b = mean(ys) - m*mean(xs)

    return m, b


def drop_change(atrrname, old, new):

    update_bar_chart()


def update_bar_chart():

    continent = continent_select.value
    data = get_data_bar_chart(continent)
    column_source.data = column_source.from_df(data[['region',
                                                     'list2016',
                                                     'list2017',
                                                     'list2018']])

    # updates table
    update_table(data)

    # updates plot title and x_range
    column_bar_split.title.text = ('Count of universities per region in '
                                   + continent)
    column_bar_split.x_range.factors = data['region'].tolist()


def update_table(data):

    data.columns = ['region', '2016', '2017', '2018', 'mean', 'std']
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
    data['region'] = regions
    data['list2016'] = [count_2016[key] for key in regions]
    data['list2017'] = [count_2017[key] for key in regions]
    data['list2018'] = [count_2018[key] for key in regions]
    data['mean'] = data[['list2016', 'list2017', 'list2018']].mean(axis=1)
    data['std'] = data[['list2016', 'list2017', 'list2018']].std(axis=1)
    data[['mean', 'std']] = data[['mean', 'std']].astype(int)

    return data


def get_data_correlation(variable):

    column_text_dict = {
                        'Pct. intl. students': 'pct_intl_student',
                        'Share of students that are male': 'male',
                        'No. of students': 'no_student',
                        'No. of students per staffmember': 'no_student_p_staff'
                        }
    variable = column_text_dict[variable]

    df = pd.read_csv('../university_ranking.csv')
    years = [2016, 2017, 2018]

    # gets top 800 for every year and puts into list
    dfs = [df.loc[df['year'] == year].head(200) for year in years]
    df = dfs[0].append(dfs[1].append(dfs[2]))

    coi = ['ranking', variable, 'year', 'university_name']
    df = df[coi]
    data = df.copy()
    colormap = {2016: 'red',
                2017: 'green',
                2018: 'blue'}
    colors = [colormap[x] for x in data['year']]

    year_list = []
    for year in years:
        for i in range(200):
            year_list.append(year)
    data['color'] = colors
    data['years'] = year_list
    data.rename(columns={variable: 'variable'}, inplace=True)
    m, b = best_fit_line(data['ranking'], data['variable'])
    x = [i for i in range(200)]
    y = [m * x + b for x in range(len(x))]
    line_data = pd.DataFrame()
    line_data['x'] = x
    line_data['y'] = y

    return data, line_data


def correlation_change(atrrname, old, new):

    update_correlation()


def update_correlation():

    variable = correlation_select.value
    data, line_data = get_data_correlation(variable)
    correlation_source.data = correlation_source.from_df(data[['ranking',
                                                               'variable',
                                                               'years',
                                                               'color',
                                                               'university_name']])
    line_source.data = line_source.from_df(line_data[['x', 'y']])
    correlation.title.text = ('Correlation between ranking and '
                              + variable.lower())

    correlation.yaxis.axis_label = variable


def year_change(attrname, old, new):

    update_pyramid()


def data_pyramid(year, head):

    df = pd.read_csv('../university_ranking.csv', index_col=0)
    df = df.loc[df['year'] == year].head(head)
    coi = ['ranking', 'male', 'female', 'university_name']
    data = df.copy()
    data = data[coi]
    data['midmale'] = data['male']/2
    data['midfemale'] = data['female']/2

    return data


def update_pyramid():

    head = range_slider.value
    year = int(year_select.value)
    data = data_pyramid(year, head)
    coi = ['ranking', 'male', 'female', 'midmale', 'midfemale',
           'university_name']
    pyramid_source.data = pyramid_source.from_df(data[coi])
    # dynamically change height somehow
    pyramid_left_rect.height = 1
    pyramid_right_rect.height = 1


# set up widgets
table = PreText(text='', width=500)
static_table = PreText(text='', width=500)
continent_select = Select(value='America', options=['America', 'Europe',
                                                    'Asia', 'Oceania',
                                                    'Africa'])

correlation_select = Select(value='Pct. intl. students',
                            options=['Pct. intl. students',
                                     'Share of students that are male',
                                     'No. of students',
                                     'No. of students per staffmember'])

year_select = Select(value='2016', options=['2016', '2017', '2018'])
range_slider = Slider(start=1, end=200, step=1, value=1,
                      title='No. of universities')
########################################
# ********** SET UP PLOTS  *********** #
########################################
# # # # # # # # # #
# Column Bar Plot #
# # # # # # # # # #
column_source = ColumnDataSource(data=dict(region=[], list2016=[],
                                 list2017=[], list2018=[]))
column_bar_split = figure(y_range=(0, 400), x_range=[],
                          plot_height=250, plot_width=700, tools='hover',
                          tooltips='No. of universities: @$name')
column_bar_split.vbar(x=dodge('region', -0.25, range=column_bar_split.x_range),
                      top='list2016', width=0.2, source=column_source,
                      color="#c9d9d3", legend=value("2016"), name='list2016')
column_bar_split.vbar(x=dodge('region',  0.0,  range=column_bar_split.x_range),
                      top='list2017', width=0.2, source=column_source,
                      color="#718dbf", legend=value("2017"), name='list2017')
column_bar_split.vbar(x=dodge('region',  0.25, range=column_bar_split.x_range),
                      top='list2018', width=0.2, source=column_source,
                      color="#e84d60", legend=value("2018"), name='list2018')
column_bar_split.legend.location = 'top_right'
column_bar_split.legend.orientation = 'horizontal'

# # # # # # # # # # # #  # # # # # #  # # # # # ##
# Correlation Between Ranking and Selected Value #
# # # # # # # # # # # # # # # # # # # # # # # # ##
correlation_source = ColumnDataSource(data=dict(ranking=[], variable=[],
                                      color=[], years=[], university_name=[]))
line_source = ColumnDataSource(data=dict(x=[], y=[]))

# hover for scatterplot
hover = HoverTool(
            tooltips=[('Year', '@years'),
                      ('Ranking', '@ranking'),
                      ('university', '@university_name'),
                      ('Variable', '@variable')],
            names=['scatter'])

# scatterplot + best fit line for correlation between variable and ranking
correlation = figure(tools=[hover], title='', plot_width=600, plot_height=600)
correlation.xaxis.axis_label = "International Ranking"
correlation.yaxis.axis_label = ""
correlation.scatter('ranking', 'variable', source=correlation_source,
                    color='color', name='scatter', legend='years')
correlation.line('x', 'y', line_width=2, color='black',
                 source=line_source)

# # # # # # # # # # # # # # # # #
# Pyramid chart men-women split #
# # # # # # # # # # # # # # # # #
pyramid_source = ColumnDataSource(data=dict(ranking=[], male=[], female=[],
                                  university_name=[], midfemale=[],
                                  midmale=[]))
pyramid_hover = HoverTool(tooltips=[('Ranking', '@ranking'),
                                    ('% male students', '@male%'),
                                    ('% female students', '@female%'),
                                    ('University', '@university_name')])
pyramid_left = figure(tools=[pyramid_hover], title='male',
                      x_range=Range1d(100, 0),
                      y_range=Range1d(0, 200), plot_height=400, plot_width=200)
pyramid_right = figure(tools=[pyramid_hover], title='female',
                       x_range=Range1d(0, 100),
                       y_range=Range1d(0, 200), plot_height=400,
                       plot_width=200)

pyramid_right.yaxis.visible = False

pyramid_left_rect = Rect(y='ranking',
                         x='midmale',
                         width='male',
                         height=0.8,
                         fill_color='#b3cde3',
                         line_color=None)
pyramid_right_rect = Rect(y='ranking',
                          x='midfemale',
                          width='female',
                          height=0.8,
                          fill_color='#fbb4ae',
                          line_color=None)
left_glyph = GlyphRenderer(data_source=pyramid_source, glyph=pyramid_left_rect)
right_glyph = GlyphRenderer(data_source=pyramid_source, glyph=pyramid_right_rect)

pyramid_left.renderers.extend([left_glyph])
pyramid_right.renderers.extend([right_glyph])

pyramid_left.min_border_right = 0
pyramid_right.min_border_left = 0

# on change switch values
continent_select.on_change('value', drop_change)
correlation_select.on_change('value', correlation_change)
year_select.on_change('value', year_change)
range_slider.on_change('value', year_change)

# gets static plot and table string from helper.py
static_col, static_table_data = helper.bar_chart_continent_split()
static_table.text = str(static_table_data)

# lays out the widgets and columns
correlation_column = column(correlation_select, correlation)
non_static_row = row(column_bar_split, table)
static_row = row(static_col, static_table)
main_column = column(continent_select, non_static_row, static_row)
pyramid_plot = gridplot([[pyramid_left, pyramid_right]], border_space=0)
pyramid_widget_box = widgetbox(year_select, range_slider)
pyramid_column = column(pyramid_widget_box, pyramid_plot)
main_row = row(main_column, correlation_column)
secondary_row = row(pyramid_column)
layout = column(main_row, secondary_row)

# initial update
update_bar_chart()
update_correlation()
update_pyramid()

curdoc().add_root(layout)
curdoc().title = 'Region Split'
