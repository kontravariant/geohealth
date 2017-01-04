import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process
import re
from itertools import chain
import pickle

#get WHO (all csv in dir), wdi (all in dir), PWT data (STATA binary) and parse into 'countryframes'
#returns countryframes dict of dataframes


#dict of country dataframes
countryframes = {}
statframes = {}
#working directory for data files, save time later
datadir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data/'))
#health directory to iterate
hwd = os.path.join(datadir,'intermediate/who/')
wwd = os.path.join(datadir,'intermediate/wdi/')
ewd = os.path.join(datadir,'intermediate/pwt/')
#load country map and put MISSING into NA values for usability here (NON-PERMANENT)
mapfile = os.path.join(datadir,"country_map.csv")
map = pd.read_csv(mapfile,encoding='latin1')
map = map.fillna('Missing')


'''
  Kill switch
  single test vs all ~200
'''
#########
iso_codes = map['ISO Alpha3'].values.tolist()
#iso_codes = ['SDN']
#########

def who_collate():
    for datfile in os.listdir(hwd):
        if datfile.endswith(".csv"):
            #read in datfile
            df = pd.read_csv(os.path.join(hwd,datfile),na_values=['.','..','...'],encoding='latin1')
            #create list of countries in current data set
            countries = df['Country'].values.tolist()
            #go through all countries in current data set and get their codes
            codedict = {}
            for country in countries:
                #search only 'fullname' columns in map
                for col in map.columns[2:5]:
                    #get boolean vector of positive matches for current country
                    test = map.apply(lambda x: country in x[col], axis=1)
                    #filter only rules where match hit
                    trues = test[test==True]
                    #if only 1 hit, simple to get index of the true value
                    #get code in map by index in test vector, get alpha3 value
                    if len(trues) == 1:
                        idxs = test[test==True].index.tolist()
                        code = map.loc[idxs[0],'ISO Alpha3']
                        #append map code to country
                        codedict[country] = code
                        #break out, go to next country
                        break
                    #if more than one match, we must find the best match
                    if len(trues) >= 1:
                        #get same boolean vector
                        idxs = test[test==True].index.tolist()
                        #placeholder vectors for codes and names
                        placecode = []
                        names = []
                        #for each index
                        for i in idxs:
                            #get the ISO names
                            namei = map.loc[i, 'ISO Name']
                            names.append(namei)
                            #get the ISO codes
                            codei = map.loc[i,'ISO Alpha3']
                            placecode.append(codei)
                        #perform fuzzmatch to get scores
                        match = process.extract(country,names)
                        fracs = []
                        #for each match in fuzzymatch vector, get the score
                        for i in match:
                            fracs.append(i[1])
                        #get the code in the placecode vector by index of the name with max match pct%
                        code = placecode[names.index(match[fracs.index(max(fracs))][0])]
                        #map code to country
                        codedict[country] = code
                        #go to next country
                        break
                    #if no match move on
                    else:
                        pass

            # holder of statistic dataframes, [stat_code:table]
            stat = str.replace(datfile,".csv","")
            outframe = pd.DataFrame()
            ###outframe.append()
            for ctry,code in codedict.items():
                datline = df.loc[df['Country'] == ctry]
                datline = datline.reset_index()
                del datline['index']
                datline.set_value(0,'Country',code)
                outframe = outframe.append(datline, ignore_index=True)
            print(stat)
            statframes[stat] = outframe



    #all codes in map file (master list of ISO Alpha3)
    for code in iso_codes:
        #initialize dataframe
        df = pd.DataFrame()
        cframe = pd.DataFrame()
        #iterate through all WHO statistic dataframes, grab the current country row and append to
        #transient cframe to put into countryframes data structure
        for stat,tbl in statframes.items():
            rown = pd.DataFrame(tbl.loc[tbl['Country']==code])
            rown['Statistic'] = stat
            del rown['Country']
            clist = [str(ctry).strip() for ctry in rown.columns]
            rown.columns = clist
            cframe = cframe.append(rown,ignore_index=True)
        countryframes[code] = cframe

    print("Countries missing: \n","--> ",[ctry for ctry in iso_codes if ctry not in list(countryframes.keys())])
    return(countryframes)


def wdi_collate(countryframes):
    ##################
    '''
    WDI IMPORT
    '''
    ##################

    #iterate over all csv files
    for datfile in os.listdir(wwd):
        if datfile.endswith(".csv"):
            #get statistic from file name, removing file extension
            stat = datfile.replace(".csv","")
            # read in datfile
            df = pd.read_csv(os.path.join(wwd, datfile), na_values=['.', '..', '...'])
            # get country codes
            countries = df['Country Code'].values.tolist()
            heads = df.columns.tolist()
            #start 'years'list/column names and put 'Statistic' first
            years = []
            years.append('Statistic')
            #append all years from data set (col 5 and on) as STRINGs
            for col in heads[5:]:
                year = col[:4]
                years.append(str(year).strip())
            #for all countries in master ISO Alpha3 list
            for code in iso_codes:
                #data rows that match the current code
                rown = df[df['Country Code']==code]
                #start from column 5, flatten data rows into list
                vals = list(chain.from_iterable(rown.values.tolist()))[5:]
                #start data row with the statistic name
                dat = []
                dat.append(stat)
                #append all values into data row (dat)
                for item in vals:
                    dat.append(item)
                #ensure data row and header row have the same length
                if len(dat) == len(years):
                    #create appender data frame and append to existing dataframe in dictionary
                    appender = pd.DataFrame(data=[dat], columns=years)
                    countryframes[code] = countryframes[code].append(appender, ignore_index=True)
                else:
                    #if data and headers do not match, return error
                    print("WDI: no good for {} @ {}".format(code, stat))

    #print confirmation of completed WDI parse
    print("wdi data DONE")
    return(countryframes)

def pwt_collate(countryframes):

    ##################
    '''
    PWT IMPORT
    '''
    ##################
    #read PWT9.0 stata .dta file
    pwt = pd.read_stata(os.path.join(ewd,'pwt90.dta'))


    #for code in master ISO Alpha3 list
    for code in iso_codes:
        #print message showing current country
        print('writing PWT for {}'.format(code))
        #get boolean vector with TRUE rows matching current country code
        code_boolean = pwt.apply(lambda x: code in x['countrycode'], axis=1)
        #pare down boolean vector to only rows that are TRUE
        locate = code_boolean[code_boolean==True]
        #get the indices in the locate vector as list
        indx = locate.index.tolist()
        #get data rows by index list in PWT master dataframe
        dat = pwt.iloc[indx,:]
        #data is LONG format (tall), so get year column into list
        years = dat['year'].values.tolist()
        #start header row and append 'Statistic' as first column
        head = []
        head.append('Statistic')
        #append all year names as strings into header row
        for year in years:
            head.append(str(year).strip())
        #data starts at column 3
        dat = dat.iloc[:,3:]
        #rename column year to Statistic and transpose
        dat.rename(columns={'year': 'Statistic'}, inplace=True)
        dat = dat.transpose()
        #reset index since it does not matter
        dat.reset_index(level=0, inplace=True)
        #rename data columns using header list
        dat.columns = head
        #drop obsolete first row (was index row before transpose)
        dat = dat.iloc[1:,:]
        #append current dataframe to current country data frame (WHO + WDI) in dict
        countryframes[code] = countryframes[code].append(dat, ignore_index=True)
        #BELOW: tried to sort column names to put statistic first, ended up duplicating columns
        #sort_list = sorted(countryframes[code].columns, key=lambda x: str(x))
        #countryframes[code] = countryframes[code].reindex_axis(sort_list, axis=1)
    #export UKR to csv as example
    countryframes['USA'].to_csv(os.path.join(datadir+'/processed/usa.csv'),index=False)
    #print confirmation message after PWT parse
    print("{} countries with some amount of data".format(len(countryframes)))
    #data_collate() function returns the dict of {code:data}
    return(countryframes)

def dict_pickler(data):
    # pickle the data dictionary into binary pkl
    pickle.dump(data, open(os.path.join(datadir,"processed/countries.pkl"), "wb"))


def collate_and_pickle():
    #collate data, pass the dataframes dictionary to pickler
    #collate
    whoframes = who_collate()
    wdiframes = wdi_collate(whoframes)
    fullframes = pwt_collate(wdiframes)
    #and pickle
    dict_pickler(fullframes)

if __name__ == "__main__":
    collate_and_pickle()
