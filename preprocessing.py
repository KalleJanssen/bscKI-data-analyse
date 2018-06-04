from bs4 import BeautifulSoup
import requests
import urllib.request
import ast
import time
import pandas as pd
import numpy as np
from selenium import webdriver


def main():

    datapoints = []
    browser = webdriver.Chrome(executable_path='chromedriver.exe')

    for j in range(6, 9):
        url = ('https://www.timeshighereducation.com/world-university-rankings/201'
         + str(j) + '/world-ranking#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/stats')
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        table = soup.find('table', id='datatable-1')


        i = 1
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
                datapoints.append((university, 
                                country, 
                                ranking,
                                no_student, 
                                no_student_p_staff,
                                pct_intl_student, 
                                fem_mal_ratio,
                                '201' + str(j)))

    df = pd.DataFrame(datapoints, columns=['university_name', 
        'country',
        'ranking', 
        'no_student',
        'no_student_p_staff',
        'pct_intl_student',
        'fem_mal_ratio',
        'year'])

    df.to_csv('university_ranking.csv')



if __name__ == "__main__":
    main()