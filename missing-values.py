import pandas as pd

# reads df from file
df = pd.read_csv('university_ranking.csv', index_col=0)  

# all rows that are missing some value
null_df = df[df.isnull().any(axis=1)]

# make a new csv file
null_df.to_csv('missing-values.csv')

# what columns are missing data
null_data = null_df.isnull().sum

print(null_data)