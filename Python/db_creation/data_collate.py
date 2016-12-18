import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process
import re
from itertools import chain
import pickle


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
    map = pd.read_csv(os.path.join(cwd,"country_info/country_map.csv"))
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
            df = pd.read_csv(os.path.join(hwd,datfile),na_values=['.','..','...'])
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


    for code in iso_codes:
        df = pd.DataFrame()
        for frame in statframes:
            stat = re.search('\((.*?)\)', frame.columns[1]).group(1)
            rown = frame.loc[frame['Country'] == code]
            vals = rown.values.tolist()
            vals = list(chain.from_iterable(vals))[1:]

            items = []


            if len(rown) > 0:
                heads = frame.columns.tolist()
                years = []
                stat = re.search('\((.*?)\)', heads[1]).group(1)
                items.append(stat)
                for i in heads:
                    reyear = re.compile('(\d{4})')
                    year_search = reyear.search(i)
                    if year_search:
                        year = year_search.group(1)
                        years.append(year)
                    else:
                        pass
                cols = []
                cols.append('Statistic')
                for item in years:
                    cols.append(str(item))
                for item in vals:
                    items.append(item)

                appender = pd.DataFrame(data=[items],columns=cols)
                df = df.append(appender, ignore_index=True)
            else:
                print("HEALTH: {} ERROR @ {}".format(code,stat))

        countryframes[code] = df


    ##################
    '''
    WDI IMPORT
    '''
    ##################


    wdi_dir = '../../data/Health/wdi'
    for datfile in os.listdir(wdi_dir):
        if datfile.endswith(".csv"):
            stat = datfile.replace(".csv","")
            # read in datfile
            df = pd.read_csv(os.path.join(wdi_dir, datfile), na_values=['.', '..', '...'])
            # get country codes
            countries = df['Country Code'].values.tolist()
            heads = df.columns.tolist()
            years = []
            years.append('Statistic')
            for col in heads[5:]:
                year = col[:4]
                years.append(str(year))
            countries=['SDN']
            for code in iso_codes:
                rown = df[df['Country Code']==code]
                vals = list(chain.from_iterable(rown.values.tolist()))[5:]
                dat = []
                dat.append(stat)
                for item in vals:
                    dat.append(item)
                if len(dat) == len(years):
                    appender = pd.DataFrame(data=[dat], columns=years)
                    countryframes[code] = countryframes[code].append(appender, ignore_index=True)
                else:
                    print("WDI: no good for {} @ {}".format(code, stat))

    print("wdi data DONE")

    ##################
    '''
    PWT IMPORT
    '''
    ##################

    cwd = '../../data/'
    ewd = '../../data/Econ/'
    map = pd.read_csv(os.path.join(cwd,"country_info/country_map.csv"))
    map = map.fillna('Missing')
    pwt = pd.read_stata(os.path.join(ewd,'pwt90.dta'))



    for code in iso_codes:
        print('writing PWT for {}'.format(code))
        code_boolean = pwt.apply(lambda x: code in x['countrycode'], axis=1)
        locate = code_boolean[code_boolean==True]
        indx = locate.index.tolist()
        dat = pwt.iloc[indx,:]
        years = dat['year'].values.tolist()
        head = []
        head.append('Statistic')
        for year in years:
            head.append(str(year))
        dat = dat.iloc[:,3:]
        dat.rename(columns={'year': 'Statistic'}, inplace=True)
        dat = dat.transpose()
        dat.reset_index(level=0, inplace=True)
        dat.columns = head
        dat = dat.iloc[1:,:]
        countryframes[code] = countryframes[code].append(dat, ignore_index=True)

        #sort_list = sorted(countryframes[code].columns, key=lambda x: str(x))
        #countryframes[code] = countryframes[code].reindex_axis(sort_list, axis=1)

    countryframes['UKR'].to_csv('../../data/ukr.csv',index=False)

    print(len(countryframes))
    return(countryframes)


def dict_pickler(data):
    pickle.dump(data, open("../../data/tables.pkl", "wb"))


dataframes = dict_collate()
dict_pickler(dataframes)