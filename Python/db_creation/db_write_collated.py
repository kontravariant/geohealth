import pickle
import pandas as pd
import os
import sqlite3

#ask if data should be repickled before writing SQLite
####DO THIS IF YOU HAVE MADE CHANGES TO SOURCE DATA (csv's) or LOST PICKLE FILE
pickle_check = input("Re-pickle or no? (Y or N)")
#if requested repickle, import data_collate.py and run both functions
if pickle_check == "Y":
    from data_collate import dict_collate, dict_pickler
    dataframes = dict_collate()
    dict_pickler(dataframes)
#if no pickle, continue to sqlite step
else:
    pass

#sqlite connection
cwd = '../../data/'
con_path = os.path.join(cwd,'country_data.sqlite')
con = sqlite3.connect(con_path)
#load pickled dictionary of {code:table}
countryframes = pickle.load(open(os.path.join(cwd,'tables.pkl'),'rb'))

#iterate over dict and write tables named by country code
counter = 0
success = 0
errors = 0
for code,tbl in countryframes.items():
    #print('starting {}'.format(code))
    try:
        tbl.to_sql(code,con,index=False,if_exists="replace")
        #print out each country code as
        #print('{} done.'.format(code))
        success += 1
    except Error as e:
        print('{} resulted in error: {}'.format(code,e))
        error += 1
    counter +=1
print("----{}/{} tables successfully written----".format(success,counter))
print("----{}/{} tables resulted in error----".format(errors,counter))