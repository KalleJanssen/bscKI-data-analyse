import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def male_female_fill(df):

    # columns of interest for predicting male female split
    df.loc[df.male.isnull(), 'male'] = df.groupby('country').male.transform('mean')
    df.male = df.male.astype(int)
    df['female'] = 100 - df['male']

    return df

def pct_intl_student_fill(df):

    df['pct_intl_student'] = df['pct_intl_student'].str.replace(r'%', r'.0').astype('float') / 100.0
    df['pct_intl_student'] = df['pct_intl_student'].fillna(0)
    
    return df

def score_industry_fill(df):


    coi = ['ranking',
           'score_overall',
           'score_teaching',
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
