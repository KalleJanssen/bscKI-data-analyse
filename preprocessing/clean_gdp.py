import csv
with open('../gdp_unf.csv', 'r') as f:
    with open('../gdp.csv', 'w') as w:
        for i, line in enumerate(f):
            newline = line.replace(';', ',')
            if ',,,,' in newline:
                newline = newline.replace(',,,,', '')
            if i == 0:
                newline = newline.lower()
            if 'gdp (billions)' in newline:
                newline = newline.replace('gdp (billions)', 'gdp_billions')
            w.write(newline)