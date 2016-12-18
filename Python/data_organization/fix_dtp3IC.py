import pandas as pd
import os
import re

outframe = pd.DataFrame()
cwd = '../data/Health/WHO'
df = pd.read_csv(os.path.join(cwd,'DTP3IC.csv'))
header = list(df.columns.values)
header = header[1:]
years = df.ix[0,1:].tolist()
print(header)
print(years)
heads = []
heads.append('Country')
for i, h_txt in enumerate(header):
    cat = re.sub('(\\.[0-9]{1,2})', '', h_txt)
    yr = str(years[i]).rstrip('0').rstrip('.')
    txt = '{}; {}'.format(cat,yr)
    heads.append(txt)
print(heads)

df.columns = heads
df = df.drop(df.index[0])
df.to_csv('../data/Health/WHO/DTP3IC_fixed.csv',index=False)