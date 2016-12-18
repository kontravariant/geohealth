import pickle
import pandas as pd
import os
import sqlite3


pickle_check = input("Re-pickle or no? (Y or N)")
if pickle_check == "Y":
    from data_collate import dict_collate, dict_pickler
    dataframes = dict_collate()
    dict_pickler(dataframes)
else:
    pass

#sqlite connection
cwd = '../../data/'
con_path = os.path.join(cwd,'country_data.sqlite')
con = sqlite3.connect(con_path)
#load pickled dictionary of code:table
countryframes = pickle.load(open(os.path.join(cwd,'tables.pkl'),'rb'))

#iterate over dict and write tables named by country code
for code,tbl in countryframes.items():
    print('starting {}'.format(code))
    tbl.to_sql(code,con,index=False,if_exists="replace")
    print('{} done.'.format(code))