import numpy as np
import pandas as pd


def main():

    df_gdp = pd.read_csv('../gdp.csv')
    df_ranking = pd.read_csv('../university_ranking.csv', index_col=0)
    countries = list(set(df_gdp['country'].tolist()))

    rows_list = []
    for country in countries:

        df_ranking_country = df_ranking.loc[df_ranking['country'] == country]
        df_country = df_gdp.loc[df_gdp['country'] == country]

        coi = ['score_overall', 'score_teaching', 'score_research',
               'score_citation', 'score_industry', 'score_int_outlook',
               'ranking']
        score_avgs = []

        for ranking in coi:

            score_avgs.append(df_ranking_country[ranking].mean())

        dict = {'country': country,
                'score_overall': score_avgs[0],
                'score_teaching': score_avgs[1],
                'score_research': score_avgs[2],
                'score_citation': score_avgs[3],
                'score_industry': score_avgs[4],
                'score_int_outlook': score_avgs[5],
                'ranking': score_avgs[6],
                'gdp': df_country.iloc[0]['gdp_billions']}

        rows_list.append(dict)

    df = pd.DataFrame(rows_list)
    df = df.dropna()
    df['avg_score'] = df[coi[:5]].mean(axis=1)
    df['ranking'] = df.ranking.astype(int)
    df = df.round(1)
    df = df.reset_index(drop=True)
    df.to_csv('../gdp_avg_score.csv')


if __name__ == "__main__":
    main()
