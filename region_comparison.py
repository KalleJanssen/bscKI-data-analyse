import pandas as pd
import country_converter as coco

df = pd.read_csv('university_ranking.csv')

converter = coco.CountryConverter()

country_list = df['country'].tolist()
df['region'] = converter.convert(names=country_list, to='UNregion')
