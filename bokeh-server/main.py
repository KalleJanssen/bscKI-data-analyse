import pandas as pd
import numpy as np
from numpy import histogram
import helper
from statistics import mean
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.models import FactorRange, Range1d, Plot
from bokeh.models import Rect, CategoricalAxis, LinearAxis, GlyphRenderer
from bokeh.plotting import figure, gridplot
from bokeh.transform import dodge
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.models.widgets import PreText, Select, Slider, Div, Dropdown


def meansqerror(y, y_pred):

    return np.mean((y - y_pred)**2)


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

    df = pd.read_csv('bokeh-server/static/university_ranking.csv', index_col=0)

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

    input_converter = {
                        'Pct. intl. students': 'pct_intl_student',
                        'Share of students that are male': 'male',
                        'No. of students': 'no_student',
                        'No. of students per staffmember': 'no_student_p_staff'
                        }
    variable = input_converter[variable]

    df = pd.read_csv('bokeh-server/static/university_ranking.csv')
    years = [2016, 2017, 2018]

    # gets top 800 for every year and puts into list
    df_list = [df.loc[df['year'] == year].head(200) for year in years]
    df = df_list[0].append(df_list[1].append(df_list[2]))

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
    if variable == 'pct_intl_student':
        m = round(m, 4)
    else:
        m = round(m, 2)
    b = round(b, 2)
    formulas = ['{0}x + {1}'.format(m, b) for _ in range(len(x))]
    line_data['formula'] = formulas

    return data, line_data


def correlation_change(atrrname, old, new):

    update_correlation()


def update_correlation():

    variable = correlation_select.value
    data, line_data = get_data_correlation(variable)
    correlation_source.data = correlation_source.from_df(data[
                                                         ['ranking',
                                                          'variable',
                                                          'years',
                                                          'color',
                                                          'university_name']])
    bfs_line_source.data = bfs_line_source.from_df(line_data[['x', 'y', 'formula']])
    correlation_hover.tooltips = [('Year', '@years'),
                                  ('Ranking', '@ranking'),
                                  ('university', '@university_name'),
                                  (variable, '@variable')]
    correlation.title.text = ('Correlation between ranking and '
                              + variable.lower())

    correlation.yaxis.axis_label = variable


def get_data_gdp_correlation(variable):

    input_converter = {'Ranking': 'ranking',
                        'Overall score': 'score_overall',
                        'Citation score': 'score_citation',
                        'Industry score': 'score_industry',
                        'Int. outlook score': 'score_int_outlook',
                        'Research score': 'score_research',
                        'Teaching score': 'score_teaching'}
    variable = input_converter[variable]
    df = pd.read_csv('bokeh-server/static/gdp_avg_score.csv')

    coi = ['gdp', variable, 'country']
    data = df.copy()
    data = data[coi]
    data.rename(columns={variable: 'variable'}, inplace=True)
    m, b = best_fit_line(data['gdp'], data['variable'])
    x = [i for i in range(18000)]
    y = [m * x + b for x in range(len(x))]
    line_data = pd.DataFrame()
    line_data['x'] = x
    line_data['y'] = y
    m = round(m, 6)
    b = round(b, 2)
    formulas = ['{0}x + {1}'.format(m, b) for _ in range(len(x))]
    line_data['formula'] = formulas

    return data, line_data


def gdp_correlation_change(attrname, old, new):

    update_gdp_correlation()


def update_gdp_correlation():

    variable = gdp_correlation_select.value
    data, line_data = get_data_gdp_correlation(variable)
    gdp_corr_source.data = gdp_corr_source.from_df(data[['gdp', 'variable',
                                                         'country']])
    gdp_bfs_line_source.data = gdp_bfs_line_source.from_df(line_data[['x', 'y',
                                                             'formula']])
    gdp_correlation.title.text = ('Correlation between gdp (2014) and average ' +
                                  variable.lower())
    gdp_hover.tooltips = [('Country', '@country'),
                          (variable, '@variable'),
                          ('GDP', '@gdp')]
    gdp_correlation.yaxis.axis_label = variable


def year_change(attrname, old, new):

    update_pyramid()


def get_data_pyramid(year, head):

    df = pd.read_csv('bokeh-server/static/university_ranking.csv', index_col=0)
    df = df.loc[df['year'] == year].head(head)
    coi = ['ranking', 'male', 'female', 'university_name']
    data = df.copy()
    data = data[coi]
    data['midmale'] = data['male']/2
    data['midfemale'] = data['female']/2

    return data


def update_pyramid():

    head = pyramid_xaxis_slider.value
    year = int(pyramid_year_select.value)
    data = get_data_pyramid(year, head)
    coi = ['ranking', 'male', 'female', 'midmale', 'midfemale',
           'university_name']
    pyramid_source.data = pyramid_source.from_df(data[coi])
    # dynamically change height somehow
    pyramid_left.y_range.start = 0
    pyramid_left.y_range.end = head
    pyramid_right.y_range.start = 0
    pyramid_right.y_range.end = head
    pyramid_left.xaxis.axis_label = '% of male students'
    pyramid_right.xaxis.axis_label = '% of female students'
    pyramid_left.yaxis.axis_label = 'University rank'


def hist_year_change(attrname, old, new):

    update_histogram()


def update_histogram():

    year = int(histogram_year_select.value)
    arr_hist, edges, mean, median, mode = get_data_histogram(year)
    histogram_mean_median.text = 'Mean: {0}\nMedian: {1}\nMode: {2}'.format(mean,
                                                                            median,
                                                                            mode)
    df = pd.DataFrame({'score_overall': arr_hist,
                       'left': edges[:-1],
                       'right': edges[1:]})
    histogram_source.data = histogram_source.from_df(df)
    histogram_figure.title.text = 'Histogram of scores in ' + str(year)


def get_data_histogram(year):

    df = pd.read_csv('bokeh-server/static/university_ranking.csv', index_col=0)
    df = df.loc[df['year'] == year]
    data = df.copy()
    arr_hist, edges = np.histogram(data['score_overall'],
                                   bins=int(100/2),
                                   range=[0, 100])
    mean = round(data['score_overall'].mean(), 1)
    median = round(data['score_overall'].median(), 1)
    data['score_overall'] = data.score_overall.astype(int)
    mode = data['score_overall'].mode()[0]
    return arr_hist, edges, mean, median, mode


def map_handler(attr, old, new):

    world_map_div.text = new


########################################
# ********** SET UP PLOTS  *********** #
########################################
# # # # # # # # # #
# Column Bar Plot #
# # # # # # # # # #
table = PreText(text='', width=500)
static_table = PreText(text='', width=500)
continent_select = Select(value='America', options=['America', 'Europe',
                                                    'Asia', 'Oceania',
                                                    'Africa'])
column_source = ColumnDataSource(data=dict(region=[], list2016=[],
                                 list2017=[], list2018=[]))
column_bar_split = figure(y_range=(0, 400), x_range=[],
                          plot_height=250, plot_width=700,
                          tools=['hover', 'save'],
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
bfs_line_source = ColumnDataSource(data=dict(x=[], y=[], formula=[]))
correlation_select = Select(value='Pct. intl. students',
                            options=['Pct. intl. students',
                                     'Share of students that are male',
                                     'No. of students',
                                     'No. of students per staffmember'])
# hover for scatterplot
correlation_hover = HoverTool(
            tooltips=[('Year', '@years'),
                      ('Ranking', '@ranking'),
                      ('university', '@university_name'),
                      ('Variable', '@variable')],
            names=['scatter'])

# scatterplot + best fit line for correlation between variable and ranking
correlation = figure(tools=[correlation_hover, 'save'],
                     title='',
                     plot_width=600,
                     plot_height=500,
                     toolbar_location='above')
correlation.xaxis.axis_label = "International Ranking"
correlation.yaxis.axis_label = ""
correlation.scatter('ranking', 'variable', source=correlation_source,
                    color='color', name='scatter', legend='years')
correlation.line('x', 'y', line_width=2, color='black',
                 legend='formula',
                 source=bfs_line_source)

# # # # # # # # # # # #  # # # # # #  #
# Correlation Between Ranking and gdp #
# # # # # # # # # # # # # # # # # # # #
gdp_corr_source = ColumnDataSource(data=dict(gdp=[], variable=[], country=[]))
gdp_bfs_line_source = ColumnDataSource(data=dict(x=[], y=[], formula=[]))
gdp_correlation_select = Select(value='Ranking',
                                options=['Ranking', 'Overall score',
                                         'Citation score', 'Industry score',
                                         'Int. outlook score',
                                         'Research score', 'Teaching score'])
# hover for scatter-plot
gdp_hover = HoverTool(
            tooltips=[('Country', '@country'),
                      ('Variable', '@variable'),
                      ('GDP', '@gdp')],
            names=['scatter_gdp'])
gdp_correlation = figure(tools=[gdp_hover, 'save'],
                         title='',
                         plot_width=500,
                         plot_height=486,
                         toolbar_location='above')
gdp_correlation.xaxis.axis_label = 'GDP in billions'
gdp_correlation.yaxis.axis_label = ''
gdp_correlation.scatter('gdp', 'variable', source=gdp_corr_source,
                        name='scatter_gdp')
gdp_correlation.line('x', 'y', line_width=2, color='black',
                     legend='formula', source=gdp_bfs_line_source)

# # # # # # # # # # # # # # # # #
# Pyramid chart men-women split #
# # # # # # # # # # # # # # # # #
pyramid_year_select = Select(value='2016', options=['2016', '2017', '2018'])
pyramid_xaxis_slider = Slider(start=20, end=200, step=1, value=20,
                              title='No. of universities', orientation='vertical',
                              height=400)
pyramid_source = ColumnDataSource(data=dict(ranking=[], male=[], female=[],
                                  university_name=[], midfemale=[],
                                  midmale=[]))
pyramid_hover = HoverTool(tooltips=[('Ranking', '@ranking'),
                                    ('% male students', '@male%'),
                                    ('% female students', '@female%'),
                                    ('University', '@university_name')])
pyramid_left = figure(title='male',
                      x_range=(100, 0), tools=[pyramid_hover, 'save'],
                      y_range=(0, 200), plot_height=470, plot_width=200)
pyramid_right = figure(title='female',
                       x_range=(0, 100), tools=[pyramid_hover, 'save'],
                       y_range=(0, 200), plot_height=470,
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
left_glyph = GlyphRenderer(data_source=pyramid_source,
                           glyph=pyramid_left_rect)
right_glyph = GlyphRenderer(data_source=pyramid_source,
                            glyph=pyramid_right_rect)

pyramid_left.renderers.extend([left_glyph])
pyramid_right.renderers.extend([right_glyph])

pyramid_left.min_border_right = 0
pyramid_right.min_border_left = 0

# # # # # # # # # ##
# Grade Histograms #
# # # # # # # # # ##
histogram_year_select = Slider(start=2016, end=2018, step=1, value=2016,
                               title='Year:')
histogram_mean_median = PreText(text='')
histogram_source = ColumnDataSource(data=dict(score_overall=[],
                                              left=[],
                                              right=[]))
histogram_hover = HoverTool(tooltips=[('Score', '@left - @right'),
                                      ('# of universities', '@score_overall')])
histogram_figure = figure(plot_width=500, plot_height=500,
                          x_axis_label='Overall grade',
                          y_axis_label='Amount of Universities',
                          tools=[histogram_hover, 'save'])

histogram_figure.quad(source=histogram_source, bottom=0, fill_alpha=0.75,
                      top='score_overall', left='left', right='right',
                      fill_color='red', line_color='black',
                      hover_fill_alpha=1.0, hover_fill_color='navy')
histogram_figure.add_tools(histogram_hover)

# # # # # # #
# world map #
# # # # # # #
world_map_div = Div(text="<img src='/bokeh-server/static/map2016.png'>")
menu = [("2016", "<img src='/bokeh-server/static/map2016.png'>"),
        ("2017", "<img src='/bokeh-server/static/map2017.png'>"),
        ("2018", "<img src='/bokeh-server/static/map2018.png'>")]
map_dropdown = Dropdown(label='Select a year:', menu=menu)

# on change switch values
continent_select.on_change('value', drop_change)
correlation_select.on_change('value', correlation_change)
pyramid_year_select.on_change('value', year_change)
pyramid_xaxis_slider.on_change('value', year_change)
histogram_year_select.on_change('value', hist_year_change)
map_dropdown.on_change('value', map_handler)
gdp_correlation_select.on_change('value', gdp_correlation_change)

# gets static plot and table string from helper.py
static_col, static_table_data = helper.bar_chart_continent_split()
static_table.text = str(static_table_data)

# lays out the widgets and columss
non_static_row = row(column_bar_split, table)
static_row = row(static_col, static_table)
map_column = column(map_dropdown, world_map_div)


correlation_column = column(correlation_select, correlation)
main_column = column(continent_select, non_static_row, static_row)
pyramid_plot = gridplot([[pyramid_left, pyramid_right]],
                        border_space=0)
pyramid_plot_slider = row(pyramid_plot, pyramid_xaxis_slider)
pyramid_column = column(pyramid_year_select, pyramid_plot_slider)
pyramid_row = row(pyramid_column)
correlations_200 = row(correlation_column, pyramid_row)

histogram_figure_mean_median = row(histogram_figure, histogram_mean_median)
hist_column = column(histogram_year_select, histogram_figure)
gdp_column = column(gdp_correlation_select, gdp_correlation)
further_row = row(hist_column, gdp_column)

rest_column = column(correlations_200, further_row)
regions_column = column(main_column, map_column)

layout = row(regions_column, rest_column)

# initial update
update_bar_chart()
update_correlation()
update_pyramid()
update_histogram()
update_gdp_correlation()

curdoc().add_root(layout)
curdoc().title = 'Interactive Data Visualisation'
