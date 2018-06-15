import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.layouts import column
from bokeh.io import show, output_file


## globals ##

num_vars = 4

centre = 0.5
theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
theta += np.pi/2

def normalize(df, column):
	# normalizes data in column based on min-max method
	return ((df[column] - df[column].min()) / (df[column].max() - df[column].min()))

def unit_poly_verts(theta, centre ):
    # Return vertices of polygon for subplot axes.
    # This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    x0, y0, r = [centre ] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def radar_patch(r, theta, centre ):
    # Returns the x and y coordinates corresponding to the magnitudes of 
    # each variable displayed in the radar plot
    # offset from centre of circle
    offset = 0.01
    yt = (r*centre + offset) * np.sin(theta) + centre 
    xt = (r*centre + offset) * np.cos(theta) + centre 
    return xt, yt

verts = unit_poly_verts(theta, centre)
x = [v[0] for v in verts] 
y = [v[1] for v in verts] 

def top_5_radar():
	
	p = figure(title="Radar plot of 5 highest ranked universities")
	text = ['No. of Students per staff member', 'Male', '% Int. Students', 'No. of Students', '']
	source = ColumnDataSource({'x':x + [centre ],'y':y + [1],'text':text})

	p.line(x="x", y="y", source=source)

	labels = LabelSet(x="x",y="y",text="text",source=source)

	p.add_layout(labels)

	years = [2016, 2017, 2018]
	coi = ['no_student_p_staff', 'male', 'pct_intl_student', 'no_student']
	df = pd.read_csv('university_ranking.csv', index_col=0)

	# normalizes no_students_p_staff to a value between 0 and 1
	df['no_student_p_staff'] = normalize(df, 'no_student_p_staff')
	df['no_student'] = normalize(df, 'no_student')
	# normalizes data to be between 0 and 1
	df['male'] = df['male'] / 100
	# gets top 5 universities of given year
	df = df.loc[df['year'] == 2016].head(5)
	# gets columns we care about
	df = df[coi]

	flist = np.array(df.values.tolist())
	colors = ['blue','green','red', 'orange','purple']
	for i in range(len(flist)):
	    xt, yt = radar_patch(flist[i], theta, centre)
	    p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color=colors[i])
	return p

def tail_5_radar():
	
	p = figure(title="Radar plot of 5 lowest ranked universities")
	text = ['No. of Students per staff member', 'Male', '% Int. Students', 'No. of Students', '']
	source = ColumnDataSource({'x':x + [centre ],'y':y + [1],'text':text})

	p.line(x="x", y="y", source=source)

	labels = LabelSet(x="x",y="y",text="text",source=source)

	p.add_layout(labels)

	years = [2016, 2017, 2018]
	coi = ['no_student_p_staff', 'male', 'pct_intl_student', 'no_student']
	df = pd.read_csv('university_ranking.csv', index_col=0)

	# normalizes no_students_p_staff to a value between 0 and 1
	df['no_student_p_staff'] = normalize(df, 'no_student_p_staff')
	df['no_student'] = normalize(df, 'no_student')
	# normalizes data to be between 0 and 1
	df['male'] = df['male'] / 100
	# gets top 5 universities of given year
	df = df.loc[df['year'] == 2016].tail(5)
	# gets columns we care about
	df = df[coi]

	flist = np.array(df.values.tolist())
	colors = ['blue','green','red', 'orange','purple']
	for i in range(len(flist)):
	    xt, yt = radar_patch(flist[i], theta, centre)
	    p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color=colors[i])
	return p


def main():

	output_file('docs/radar_plot.html')

	p1 = top_5_radar()
	p2 = tail_5_radar()

	show(column(p1, p2))

if __name__ == "__main__":
	main()