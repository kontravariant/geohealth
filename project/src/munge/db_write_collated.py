import pickle
import pandas as pd
import os
import sqlite3

datadir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data/'))

def write_db():

    #sqlite connection
    cwd = os.path.join(datadir,'processed/')
    con_path = os.path.join(cwd,'geohealth.sqlite')
    con = sqlite3.connect(con_path)
    #load pickled dictionary of {code:table}
    countryframes = pickle.load(open(os.path.join(cwd,'countries.pkl'),'rb'))

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

if __name__ == "__main__":
    write_db()