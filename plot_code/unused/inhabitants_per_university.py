import pandas as pd
from collections import Counter
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import Panel, ColumnDataSource, HoverTool


def main():

    # reads df from file
    df = pd.read_csv('../../university_ranking.csv', index_col=0)

    # splits data-frame
    df2018 = df.loc[df['year'] == 2018]

    # all continents put into lists
    continents_2018 = df2018['continent'].tolist()

    # all continents counter and put into dictionaries
    count_2018 = dict(Counter(continents_2018))

    # continent order that I wanted
    continents = ['Africa', 'Asia', 'America', 'Europe', 'Oceania']

    # inhabitants of each continent for
    count_20181 = {'Europe': '738.849.000',
                   'America': '1.001.559.000',
                   'Asia': '4.436.224.000',
                   'Africa': '1.216.130.000',
                   'Oceania': '39.901.000'}

    count_20183 = {'Europe': 738849000,
                   'America': 1001559000,
                   'Asia': 4436224000,
                   'Africa': 1216130000,
                   'Oceania': 39901000}

    count_20182 = {'Europe': 738849000/1000000,
                   'America': 1001559000/1000000,
                   'Asia': 4436224000/1000000,
                   'Africa': 1216130000/1000000,
                   'Oceania': 39901000/1000000}

    # lists of counts in corrrect order as outlined above
    list2018 = [count_20181[key] for key in continents]

    # Inhabitants per university in a list
    list20183 = [round(count_20183[key]/count_2018[key]) for key in continents]

    # Inhabitants per university in a list with points =
    # seperating the big numbers
    list2018points = ["{:,}".format(key1).
                      replace(",", ".") for key1 in list20183]

    # Values of the bars in the plot
    list20182 = [count_20182[key]/count_2018[key] for key in continents]

    # lists of amount of inhabitants in corrrect order as outlined above
    listinhabitants = [count_20181[key] for key in continents]

    # lists of amount of universities in corrrect order as outlined above
    listuniversities = [count_2018[key] for key in continents]

    # dictioanry with data for making a figure
    data = {'continents': continents,
            '20182': list20182,
            '20183': list2018points,
            'listinhabitants': listinhabitants,
            'listuniversities': listuniversities}

    source = ColumnDataSource(data=data)

    p = figure(x_range=continents, y_range=(0, 50),
               plot_height=500,
               title="Number of inhabitants per continent per university",
               x_axis_label='Continents',
               y_axis_label='Amount of inhabitants per university (x1m)',
               toolbar_location=None, tools="")

    p.vbar(x=dodge('continents', 0, range=p.x_range),
           top='20182', width=0.2, source=source,
           color="#0000FF")

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None

    hover = HoverTool(tooltips=[('Inhabitants', "@listinhabitants"),
                                ('Amount of universities',
                                 '@listuniversities'),
                                ('Number of inhabitants per university',
                                 '@20183')])

    p.add_tools(hover)

    # disables the scientific notation of numbers
    p.left[0].formatter.use_scientific = False

    output_file('docs/inhabitants_per_university.html')

    show(p)


if __name__ == "__main__":
    main()
