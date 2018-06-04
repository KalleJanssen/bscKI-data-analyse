import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
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

    # all rows that are not null in male column
    not_nans = df['male'].notnull()
    df_not_nans = df[not_nans]

    # split data into features and labels
    x = df_not_nans[coi]
    y = df_not_nans['male']
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

    x = df_notnans[coi]
    y = df_notnans['score_industry']
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

    x = df_not_nans[coi]
    y = df_not_nans['score_overall']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    clf = LinearRegression()
    clf.fit(x_train, y_train)
    print("score_overall: ", clf.score(x_test, y_test))
    df_nans = df.loc[~not_nans].copy()
    df_nans['score_overall'] = clf.predict(df_nans[coi])
    df.score_overall.fillna(df_nans.score_overall, inplace=True)

    return df


def retrieve_data():
    stats = []
    scores = []

    browser = webdriver.Chrome()

    # loop through relevant years
    for j in range(6, 9):

        # creates url to be used
        url = ('https://www.timeshighereducation.com/world-university-rankings/201'
               + str(j) + '/world-ranking#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/stats')
        browser.get(url)
        # converts html file into soup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        # find relevant table
        table = soup.find('table', id='datatable-1')

        i = 1
        # loops through rows and columns for relevant data
        for table_row in table.select('tr'):
            cells = table_row.findAll('td')
            if len(cells) > 0:
                ranking = i

                name_country = cells[1]
                name_country = name_country.select('a')
                university = name_country[0].text.strip()
                country = name_country[1].text.strip()
                no_student = cells[2].text.strip()
                no_student_p_staff = cells[3].text.strip()
                pct_intl_student = cells[4].text.strip()
                fem_mal_ratio = cells[5].text.strip()
                i += 1
                stats.append((university,
                              country,
                              ranking,
                              no_student,
                              no_student_p_staff,
                              pct_intl_student,
                              fem_mal_ratio,
                              '201' + str(j)))

    # same as above, had to separate into 2 for loops because it didn't work otherwise
    for j in range(6, 9):

        url = ('https://www.timeshighereducation.com/world-university-rankings/201' +
               str(j) + '/world-ranking#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/scores')
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        table = soup.find('table', id='datatable-1')
        for table_row in table.select('tr'):
            cells = table_row.findAll('td')

            if len(cells) > 0:
                name_country = cells[1]
                name_country = name_country.select('a')
                university = name_country[0].text.strip()
                country = name_country[1].text.strip()
                score_overall = cells[2].text.strip()
                score_teaching = cells[3].text.strip()
                score_research = cells[4].text.strip()
                score_citation = cells[5].text.strip()
                score_industry = cells[6].text.strip()
                score_int_outlook = cells[7].text.strip()

                scores.append((university,
                               country,
                               score_overall,
                               score_teaching,
                               score_research,
                               score_citation,
                               score_industry,
                               score_int_outlook,
                               '201' + str(j)))

    # creates 2 data-frames to be merged
    ranking_df = pd.DataFrame(stats, columns=['university_name',
                                              'country',
                                              'ranking',
                                              'no_student',
                                              'no_student_p_staff',
                                              'pct_intl_student',
                                              'fem_mal_ratio',
                                              'year'])

    score_df = pd.DataFrame(scores, columns=['university_name',
                                             'country',
                                             'score_overall',
                                             'score_teaching',
                                             'score_research',
                                             'score_citation',
                                             'score_industry',
                                             'score_int_outlook',
                                             'year'])
    # merges 2 data-frames based on university name, country and year into one data-frame
    df = ranking_df.merge(score_df, on=['university_name', 'country', 'year'])

    df[['male', 'female']] = df.pop('fem_mal_ratio').str.split(' : ', expand=True)
    df['no_student'] = df['no_student'].str.strip('" ').str.replace(',', '').astype(int)
    cols = ['score_overall',
            'score_teaching',
            'score_research',
            'score_citation',
            'score_industry',
            'score_int_outlook']
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    # saves data-frame as a comma separated values file
    df.to_csv('university_ranking.csv')


def main():
    retrieve_data()

    # reads df from file
    df = pd.read_csv('university_ranking.csv', index_col=0)

    df = male_female_fill(df)
    df = score_industry_fill(df)
    df = score_overall_fill(df)

    df.to_csv('university_ranking.csv')


if __name__ == "__main__":
    main()
