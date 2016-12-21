#######
#Data boiler from pwt_collate_boiler
#######

import os
import pandas as pd
from pandas.io import sql
import numpy as np
import re
from itertools import chain
''''''
import sqlite3

cwd = '../../data/'
ewd = '../../data/Econ/'
map = pd.read_csv(os.path.join(cwd,"country_info/country_map.csv"))
map = map.fillna('Missing')
iso_codes = map['ISO Alpha3'].values.tolist()
pwt = pd.read_stata(os.path.join(ewd,'pwt90.dta'))
dat = 1
iso_codes=['USA']
for code in iso_codes:
    code_boolean = pwt.apply(lambda x: code in x['countrycode'], axis=1)
    locate = code_boolean[code_boolean==True]
    indx = locate.index.tolist()
    dat = pwt.iloc[indx,:]
    years = dat['year'].values.tolist()
    head = []
    head.append('Statistic')
    for year in years:
        head.append(year)
    print(head)

    dat = dat.iloc[:,3:]
    dat.rename(columns={'year': 'Statistic'}, inplace=True)
    dat = dat.transpose()
    dat.reset_index(level=0, inplace=True)
    dat.columns = dat.loc[0].values.tolist()
    dat = dat.iloc[1:,:]

output = dat.itertuples()
print(tuple(output))


####
#TO LOOP THROUGH ALL CODE DATAFRAMES
####
con_path = os.path.join(cwd,'test_db.sqlite')
con = sqlite3.connect(con_path)
dat.to_sql("USA",con,index=False,if_exists='replace')

#cur = con.cursor()

