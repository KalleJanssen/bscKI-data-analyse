import plotly.plotly as py
import pandas as pd
import plotly.offline
import country_converter as coco
from collections import Counter


codes = ['AFG', 'ALB', 'DZA', 'ASM', 'AND', 'AGO', 'AIA', 'ATG', 'ARG', 'ARM', 'ABW', 
         'AUS', 'AUT', 'AZE', 'BHM', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN', 
         'BMU', 'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'VGB', 'BRN', 'BGR', 'BFA', 'MMR', 
         'BDI', 'CPV', 'KHM', 'CMR', 'CAN', 'CYM', 'CAF', 'TCD', 'CHL', 'CHN', 'COL', 
         'COM', 'COD', 'COG', 'COK', 'CRI', 'CIV', 'HRV', 'CUB', 'CUW', 'CYP', 'CZE', 
         'DNK', 'DJI', 'DMA', 'DOM', 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'ETH', 
         'FLK', 'FRO', 'FJI', 'FIN', 'FRA', 'PYF', 'GAB', 'GMB', 'GEO', 'DEU', 'GHA', 
         'GIB', 'GRC', 'GRL', 'GRD', 'GUM', 'GTM', 'GGY', 'GNB', 'GIN', 'GUY', 'HTI', 
         'HND', 'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRN', 'IRQ', 'IRL', 'IMN', 'ISR', 
         'ITA', 'JAM', 'JPN', 'JEY', 'JOR', 'KAZ', 'KEN', 'KIR', 'PRK', 'KOR', 'KSV', 
         'KWT', 'KGZ', 'LAO', 'LVA', 'LBN', 'LSO', 'LBR', 'LBY', 'LIE', 'LTU', 'LUX', 
         'MAC', 'MKD', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI', 'MLT', 'MHL', 'MRT', 'MUS', 
         'MEX', 'FSM', 'MDA', 'MCO', 'MNG', 'MNE', 'MAR', 'MOZ', 'NAM', 'NPL', 'NLD', 
         'NCL', 'NZL', 'NIC', 'NGA', 'NER', 'NIU', 'MNP', 'NOR', 'OMN', 'PAK', 'PLW', 
         'PAN', 'PNG', 'PRY', 'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'ROU', 'RUS', 
         'RWA', 'KNA', 'LCA', 'MAF', 'SPM', 'VCT', 'WSM', 'SMR', 'STP', 'SAU', 'SEN', 
         'SRB', 'SYC', 'SLE', 'SGP', 'SXM', 'SVK', 'SVN', 'SLB', 'SOM', 'ZAF', 'SSD', 
         'ESP', 'LKA', 'SDN', 'SUR', 'SWZ', 'SWE', 'CHE', 'SYR', 'TWN', 'TJK', 'TZA', 
         'THA', 'TLS', 'TGO', 'TON', 'TTO', 'TUN', 'TUR', 'TKM', 'TUV', 'UGA', 'UKR', 
         'ARE', 'GBR', 'USA', 'URY', 'UZB', 'VUT', 'VEN', 'VNM', 'VGB', 'WBG', 'YEM', 
         'ZMB', 'ZWE']
converter = coco.CountryConverter()
plotly.tools.set_credentials_file(username='arnitro', api_key='foCkT4Qrj9x1F73nuvBw')
 
df = pd.read_csv('university_ranking.csv', index_col=0)
df2016 = df.loc[df['year'] == 2016].head(800)
df2017 = df.loc[df['year'] == 2017].head(800)
df2018 = df.loc[df['year'] == 2018].head(800)

dfs = [df2016, df2017, df2018]

i = 2016


for df in dfs:

    country_list = df['country'].tolist()
    df['country_code'] = converter.convert(names=country_list, to='ISO3')

    country_code = df['country_code'].tolist()

    counter = dict(Counter(country_code))

    for con_code in codes:

        if con_code not in counter:
            counter[con_code] = 0
        else:
            pass

    code = [key for key in counter]
    count = [counter[key] for key in counter]

    data = [dict(
            type='choropleth',
            locations=code,
            z=count,
            colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"],
                        [0.5, "rgb(70, 100, 245)"], [0.6, "rgb(90, 120, 245)"],
                        [0.7, "rgb(106, 137, 247)"],
                        [1, "rgb(220, 220, 220)"]],
            autocolorscale=False,
            reversescale=True,
            marker=dict(
                line=dict(
                    color='rgb(180,180,180)',
                    width=0.5
                )),
            colorbar=dict(
                autotick=False,
                title='Number of universities'))]

    layout = dict(
        title='Number of universities in top 800 per country per year - ' + str(i),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection=dict(
                type='Mercator'
            )
        )
    )

    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, validate=False,
                        filename='docs/map' + str(i) + '.html')
    i += 1
