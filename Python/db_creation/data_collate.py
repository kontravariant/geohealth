import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process
import re
from itertools import chain
import pickle

#get WHO (all csv in dir), wdi (all in dir), PWT data (STATA binary) and parse into 'countryframes'
#returns countryframes dict of dataframes
def dict_collate():
    #list of statistic dataframes
    statframes = []
    #dict of country dataframes
    countryframes = {}
    #working directory for data files, save time later
    cwd = '../../data/'
    #health directory to iterate
    hwd = '../../data/Health/WHO'
    #load country map and put MISSING into NA values for usability here (NON-PERMANENT)
    map = pd.read_csv(os.path.join(cwd,"country_info/country_map.csv"),encoding='latin1')
    map = map.fillna('Missing')


    '''
    Dead man trigger
    single test vs all ~200
    '''
    #########
    iso_codes = map['ISO Alpha3'].values.tolist()
    #iso_codes = ['SDN']
    #########

    for datfile in os.listdir(hwd):
        if datfile.endswith(".csv"):
            #read in datfile
            df = pd.read_csv(os.path.join(hwd,datfile),na_values=['.','..','...'],encoding='latin1')
            #create list of countries in current data set
            #WILL country column label change? can we use boolean for column name?
            countries = df['Country'].values.tolist()
            #go through all countries in current data set and get their codes
            codes = []
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
                        #append code to code list
                        codes.append(code)
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
                        #get the index of the maximum match percent
                        maxix = fracs.index(max(fracs))
                        #get the ISO name of the maximum match
                        maxname = match[maxix][0]
                        #use maxname to get the index of ISO name in names vector
                        codeix = names.index(maxname)
                        #get the code in the placecode vector by index of the name
                        code = placecode[codeix]
                        #append code to codes
                        codes.append(code)
                        #go to next country
                        break
                    #if no match move on
                    else:
                        pass

            if len(codes)==len(countries):
                print(len(codes))
                print('checks out for {}'.format(datfile))
                df['Country'] = codes
                statframes.append(df)
            else:
                print('not good @ {}'.format(datfile))

    #all codes in map file (master list of ISO Alpha3)
    for code in iso_codes:
        #initialize dataframe
        df = pd.DataFrame()
        #for each statistic in the statframes dictionary dict of dataframes)
        for frame in statframes:
            #get statistic name from the text in parentheses of column 2, i.e. measles coverage (*MCV*) (%)
            stat = re.search('\((.*?)\)', frame.columns[1]).group(1)
            #get all rows matching current code
            rown = frame.loc[frame['Country'] == code]
            #turn those indices into a list
            vals = rown.values.tolist()
            #unpack/flatten that list and remove first column which is the country name
            vals = list(chain.from_iterable(vals))[1:]

            items = []

            #if there are any hits in the rown list
            if len(rown) > 0:
                #get column names and put into list
                heads = frame.columns.tolist()
                years = []
                #get stat from text in parentheses in column 2
                stat = re.search('\((.*?)\)', heads[1]).group(1)
                #start the data row with the statistic name
                items.append(stat)
                #for each column name, get the 4 digit date
                for i in heads:
                    reyear = re.compile('(\d{4})')
                    year_search = reyear.search(i)
                    #if a year was found append it to the years list
                    if year_search:
                        year = year_search.group(1)
                        years.append(year)
                    else:
                        pass
                #start the column names with 'Statistic'
                cols = []
                cols.append('Statistic')
                #append all years to column name list, as STRINGs
                for item in years:
                    cols.append(str(item))
                #for each value in the row, append to the data row
                for item in vals:
                    items.append(item)
                #create a dataframe from data row (items) and column names (cols)
                appender = pd.DataFrame(data=[items],columns=cols)
                #append current appender to empty data frame with reset indices
                df = df.append(appender, ignore_index=True)
            else:
                #print error if len(rown) = 0
                print("HEALTH: {} ERROR @ {}".format(code,stat))
        #using current code as key, create dictionary pair with data frame
        countryframes[code] = df


    ##################
    '''
    WDI IMPORT
    '''
    ##################

    #set current directory to world development indicators folder
    wdi_dir = '../../data/Health/wdi'
    #iterate over all csv files
    for datfile in os.listdir(wdi_dir):
        if datfile.endswith(".csv"):
            #get statistic from file name, removing file extension
            stat = datfile.replace(".csv","")
            # read in datfile
            df = pd.read_csv(os.path.join(wdi_dir, datfile), na_values=['.', '..', '...'])
            # get country codes
            countries = df['Country Code'].values.tolist()
            heads = df.columns.tolist()
            #start 'years'list/column names and put 'Statistic' first
            years = []
            years.append('Statistic')
            #append all years from data set (col 5 and on) as STRINGs
            for col in heads[5:]:
                year = col[:4]
                years.append(str(year))
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

    ##################
    '''
    PWT IMPORT
    '''
    ##################
    #set working dir, econ working dir, country map file, fill in NAs with string
    #read PWT9.0 stata .dta file
    cwd = '../../data/'
    ewd = '../../data/Econ/'
    map = pd.read_csv(os.path.join(cwd,"country_info/country_map.csv"),encoding='latin1')
    map = map.fillna('Missing')
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
            head.append(str(year))
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
    countryframes['UKR'].to_csv('../../data/ukr.csv',index=False)
    #print confirmation message after PWT parse
    print("{} countries with some amount of data".format(len(countryframes)))
    #data_collate() function returns the dict of {code:data}
    return(countryframes)

#pickle the data dictionary into binary pkl
def dict_pickler(data):
    pickle.dump(data, open("../../data/tables.pkl", "wb"))

#collate data, pass the dataframes dictionary to pickler
dataframes = dict_collate()
dict_pickler(dataframes)