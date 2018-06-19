from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import show, output_file

output_file('docs/male-female-example.html')

# create data
products = ['python', 'pypy', 'jython']
customers = ['Cust 1', 'Cust 2']
colours = ['red', 'blue']
data = {
    'products': products,
    'Cust 1': [200, 850, 400],
    'Cust 2': [600, 620, 550]
}


source = ColumnDataSource(data)

p = figure(y_range=products)

p.hbar_stack(customers, y='products', height=0.5, source=source, color=colours)

show(p)
output_file("stacked.html")
