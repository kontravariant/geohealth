# -*- coding: utf-8 -*-

"""
Created on Sun Jul 17 08:06:46 2016

@author: tmck
"""
import pandas as pd
import copy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


df = pd.read_csv("../data/country_info/country_lookup.csv")
who_name = df['WHO Country Name']
pwt_name = df['PWT Country Name']
cty_code = df['PWT Country Code']
who_list = who_name.values.tolist()
pwt_list = pwt_name.values.tolist()
code_list = cty_code.values.tolist()
print(who_list)
print(pwt_list)
print(code_list)

map=[]
for country in who_list:
    match = process.extract(country,pwt_list,limit=1)
    match = list(match)
    #print(country,match)
    for i, item in enumerate(match):
        match[i] = list(match[i])
        store = copy.deepcopy(match)
    if (match[0][1] < 75):
        match[0][0] = ''
    map.append([country,match[0][0]])
print(map)

df = pd.DataFrame(map)
df.to_csv('../data/country_info/country_map.csv', sep=',', encoding='utf-8')