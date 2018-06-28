import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def male_female_fill(df):

    # converts all missing datapoints in column male into
    # mean of same country
    df.loc[df.male.isnull(), 'male'] = (df.groupby('country')
                                        .male.transform('mean'))
    # converts type to integer
    df.male = df.male.astype(int)
    # calculates female percentage based on male percentage
    df['female'] = 100 - df['male']

    return df


def pct_intl_student_fill(df):

    # converts string representation to float representation
    df['pct_intl_student'] = (df['pct_intl_student'].str.replace(r'%', r'.0')
                              .astype('float') / 100.0)
    # fills missing data points with 0 value
    df['pct_intl_student'] = df['pct_intl_student'].fillna(0)

    return df


def score_industry_fill(df):

    # columns we will use for predicting score_industry
    coi = ['ranking',
           'score_overall',
           'score_teaching',
           'score_research',
           'score_citation',
           'score_int_outlook',
           ]

    # get all rows that do not miss any value in any column
    not_nans = df['score_industry'].notnull()
    df_notnans = df[not_nans]

    # features
    x = np.array(df_notnans[coi])
    # labels
    y = np.array(df_notnans['score_industry'])

    # splits rows into testing and training data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # classifier that we use, Multiple Linear Regression
    clf = LinearRegression()
    # trains classifier on trainig data
    clf.fit(x_train, y_train)

    # prints amount of predicted values that are correct
    # compares with the testing data
    print("score_industry: ", clf.score(x_test, y_test))

    # fills in missing values with classifier predicted values
    df_nans = df.loc[~not_nans].copy()
    df_nans['score_industry'] = clf.predict(df_nans[coi])
    df.score_industry.fillna(df_nans.score_industry, inplace=True)
    df['score_industry'] = round(df['score_industry'], 2)

    return df


def score_overall_fill(df):

    # columns we will se for predicting score_overall
    coi = ['score_teaching',
           'score_research',
           'score_citation',
           'score_int_outlook',
           ]

    # gets all rows that are not missing any value in any column
    not_nans = df['score_overall'].notnull()
    df_not_nans = df[not_nans]

    # features
    x = np.array(df_not_nans[coi])
    # labels
    y = np.array(df_not_nans['score_overall'])
    # splits non empty rows into training and testing data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # classifier that we use, Multiple Linear Regression
    clf = LinearRegression()
    # 
    clf.fit(x_train, y_train)
    print("score_overall: ", clf.score(x_test, y_test))
    df_nans = df.loc[~not_nans].copy()
    df_nans['score_overall'] = clf.predict(df_nans[coi])
    df.score_overall.fillna(df_nans.score_overall, inplace=True)
    df['score_overall'] = round(df['score_overall'], 2)

    return df
