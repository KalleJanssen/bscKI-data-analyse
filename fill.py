import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def male_female_fill(df):
    # columns of interest for predicting male female split
    coi = ['no_student',
           'year',
           'score_teaching',
           'score_research',
           'score_citation',
           'score_int_outlook']

    not_nans = df['male'].notnull()
    # all rows that are not null in male column
    df_not_nans = df[not_nans]

    # split data into features and labels
    x = np.array(df_not_nans[coi])
    y = np.array(df_not_nans['male'])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # the classifier we use
    clf = LinearRegression()
    # trains classifier
    clf.fit(x_train, y_train)

    # test classifier
    print("male: ", clf.score(x_test, y_test))

    # all rows that are null in data-frame
    df_nans = df.loc[~not_nans].copy()

    # predicts values for male and adds to data-frame
    df_nans['male'] = clf.predict(df_nans[coi])
    df.male.fillna(df_nans.male, inplace=True)

    # converts male column to integer type
    df['male'] = df['male'].astype('int64')
    # calculates female percentage of students
    df['female'] = 100 - df['male']

    return df


def score_industry_fill(df):
    coi = ['score_teaching',
           'score_research',
           'score_citation',
           'score_int_outlook',
           ]

    not_nans = df['score_industry'].notnull()
    df_notnans = df[not_nans]

    x = np.array(df_notnans[coi])
    y = np.array(df_notnans['score_industry'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    clf = LinearRegression()
    clf.fit(x_train, y_train)

    print("score_industry: ", clf.score(x_test, y_test))

    df_nans = df.loc[~not_nans].copy()
    df_nans['score_industry'] = clf.predict(df_nans[coi])
    df.score_industry.fillna(df_nans.score_industry, inplace=True)

    return df


def score_overall_fill(df):
    coi = ['score_teaching',
           'score_research',
           'score_citation',
           'score_industry',
           'score_int_outlook',
           ]

    not_nans = df['score_overall'].notnull()
    df_not_nans = df[not_nans]

    x = np.array(df_not_nans[coi])
    y = np.array(df_not_nans['score_overall'])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    clf = LinearRegression()
    clf.fit(x_train, y_train)
    print("score_overall: ", clf.score(x_test, y_test))
    df_nans = df.loc[~not_nans].copy()
    df_nans['score_overall'] = clf.predict(df_nans[coi])
    df.score_overall.fillna(df_nans.score_overall, inplace=True)

    return df
