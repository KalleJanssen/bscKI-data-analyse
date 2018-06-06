import pandas as pd
import fill
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import country_converter as coco

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
        time.sleep(3)
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
        time.sleep(3)
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

    df[['female', 'male']] = df.pop('fem_mal_ratio').str.split(' : ', expand=True)
    df['no_student'] = df['no_student'].str.strip('" ').str.replace(',', '').astype(int)
    cols = ['score_overall',
            'score_teaching',
            'score_research',
            'score_citation',
            'score_industry',
            'score_int_outlook']
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    # saves data-frame as a comma separated values file
    df.to_csv('../university_ranking_unf.csv')


def main():

    # if university_ranking_unf.csv is empty, use this.
    # retrieve_data()

    # reads df from file
    df = pd.read_csv('../university_ranking_unf.csv', index_col=0)
    
    # fills missing data with proper data using ml and means
    df = fill.male_female_fill(df)
    df = fill.pct_intl_student_fill(df)
    df = fill.score_overall_fill(df)
    df = fill.score_industry_fill(df)
    
    # adds continent column
    country_list = df['country'].tolist()
    converter = coco.CountryConverter()
    continents = converter.convert(names=country_list, to='continent')
    df['continents'] = continents
    
    print(df.info())
    
    df.to_csv('../university_ranking.csv')
    df.to_json('../university_ranking.json')

if __name__ == "__main__":
    main()
