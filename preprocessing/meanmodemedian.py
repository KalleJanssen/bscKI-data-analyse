# shows the grades and amount of universities form 2016, 2017 and 2018
from bokeh.plotting import figure, output_file, show
from numpy import histogram
import pandas as pd
import numpy as np
from bokeh.layouts import column, row, widgetbox, WidgetBox, layout
from bokeh.models import Panel, ColumnDataSource, HoverTool
from bokeh.models.widgets import Tabs, CheckboxGroup, Slider
from bokeh.io import output_file, show, curdoc


def main():

    uniranking = pd.read_csv('../../university_ranking.csv')

    uniranking2016 = uniranking.loc[uniranking['year'] == 2016]
    uniranking2017 = uniranking.loc[uniranking['year'] == 2017]
    uniranking2018 = uniranking.loc[uniranking['year'] == 2018]

    print(uniranking2016)


if __name__ == "__main__":
    main()
