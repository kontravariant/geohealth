import os
import pandas as pd

outframe = pd.DataFrame()
#Load all files in health data originals and match up list of countries in each
cwd = '../data/Health/originals/'
i = 0
for datfile in os.listdir(cwd):
    if datfile.endswith(".csv"):
        df = pd.read_csv(os.path.join(cwd,datfile))
        column = df.ix[:,0].tolist()
        col = pd.DataFrame(column)
        outframe = pd.concat([outframe,col], ignore_index=True,axis=1)
outframe.to_csv("../data/Health/countries.csv",sep=',')
