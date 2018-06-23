import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.layouts import column, gridplot
from bokeh.io import show, output_file

# globals

num_vars = 4

centre = 0.5
theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
theta += np.pi/2


def normalize(df, column):
    # normalizes data in column based on min-max method
    return ((df[column] - df[column].min()) / (df[column].max() - df[column].min()))


def unit_poly_verts(theta, centre):
    # Return vertices of polygon for subplot axes.
    # This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    x0, y0, r = [centre] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def radar_patch(r, theta, centre):
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


def radar_plot(df, year):

    df = df.copy()

    p = figure(title="Radar plot of 5 highest ranked universities in " +
               str(year), x_range=(0, 1.24))
    t = figure(title="Radar plot of 5 lowest ranked universities in " +
               str(year), x_range=(0, 1.24))

    text = ['No. of Students per staff member', 'Male',
            '% Int. Students', 'No. of Students', '']

    source = ColumnDataSource({'x': x + [centre], 'y': y + [1], 'text': text})

    p.line(x="x", y="y", source=source)
    t.line(x="x", y="y", source=source)

    p_labels = LabelSet(x="x", y="y", text="text", source=source)
    t_labels = LabelSet(x="x", y="y", text="text", source=source)

    p.add_layout(p_labels)
    t.add_layout(t_labels)

    coi = ['no_student_p_staff', 'male', 'pct_intl_student', 'no_student']
    df = df[coi]

    # normalizes no_students_p_staff to a value between 0 and 1
    df['no_student_p_staff'] = normalize(df, 'no_student_p_staff')
    df['no_student'] = normalize(df, 'no_student')

    # normalizes data to be between 0 and 1
    df['male'] = df['male'] / 100
    df_head = df.head(5)
    df_tail = df.tail(5)

    flist_head = np.array(df_head.values.tolist())
    flist_tail = np.array(df_tail.values.tolist())

    colors = ['blue', 'green', 'red', 'orange', 'purple']

    for i in range(len(flist_head)):
        xt, yt = radar_patch(flist_head[i], theta, centre)
        p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color=colors[i])

    for i in range(len(flist_tail)):
        xt, yt = radar_patch(flist_tail[i], theta, centre)
        t.patch(x=xt, y=yt, fill_alpha=0.15, fill_color=colors[i])

    return p, t


def radar_plot_avg(df, year):

    df = df.copy()

    p = figure(title="Average radar plot of all ranked universities in " +
               str(year), x_range=(0, 1.24))

    text = ['No. of Students per staff member', 'Male',
            '% Int. Students', 'No. of Students', '']

    source = ColumnDataSource({'x': x + [centre], 'y': y + [1], 'text': text})

    p.line(x="x", y="y", source=source)

    p_labels = LabelSet(x="x", y="y", text="text", source=source)

    p.add_layout(p_labels)

    coi = ['no_student_p_staff', 'male', 'pct_intl_student', 'no_student']
    df = df[coi]

    # normalizes no_students_p_staff to a value between 0 and 1
    df['no_student_p_staff'] = normalize(df, 'no_student_p_staff')
    df['no_student'] = normalize(df, 'no_student')

    # normalizes data to be between 0 and 1
    df['male'] = df['male'] / 100

    no_student_mean = df['no_student_p_staff'].mean()
    male_mean = df['male'].mean()
    pct_intl_student_mean = df['pct_intl_student'].mean()
    no_student_mean = df['no_student'].mean()

    flist = np.array([[no_student_mean, male_mean,
                       pct_intl_student_mean, no_student_mean]])

    for i in range(len(flist)):
        xt, yt = radar_patch(flist[i], theta, centre)
        p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color='blue')

    return p


def main():

    output_file('docs/radar_plot.html')

    df = pd.read_csv('university_ranking.csv')

    years = [2016, 2017, 2018]

    ps = []

    ts = []

    avgs = []

    for year in years:

        new_df = df.loc[df['year'] == year]

        p, t = radar_plot(df, year)
        a = radar_plot_avg(df, year)

        ps.append(p)
        ts.append(t)
        avgs.append(a)

    grid_list = []

    for i in range(len(ps)):

        grid_list.append([ps[i], ts[i], avgs[i]])

    grid = gridplot(grid_list)

    show(grid)


if __name__ == "__main__":
    main()
