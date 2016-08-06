import os
import pandas as pd
import itertools

df = pd.read_csv('../data/Health/countries_set.csv',header=None)
container = []
for column in df:
    list = df[column].tolist()
    container.append(list)
newlist=[]
for x in itertools.chain.from_iterable(container):
   if (x not in newlist):
      newlist.append(x)

print(newlist)
outframe = pd.DataFrame(data=newlist)
outframe.to_csv('../data/Health/country_union.csv')