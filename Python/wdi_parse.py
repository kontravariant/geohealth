import os
import pandas as pd

outframe = pd.DataFrame()
#Load all files in health data originals and match up list of countries in each
cwd = '../data/'

df = pd.read_csv(os.path.join(cwd,"wdi_tab.csv"),na_values=['.','..','...'])
water = df[df['Series Name'] == 'Improved water source (% of population with access)']
sanit = df[df['Series Name'] == 'Improved sanitation facilities (% of population with access)']
expnd = df[df['Series Name'] == 'Health expenditure per capita, PPP (constant 2011 international $)']

water.to_csv(os.path.join(cwd,"water.csv"))
sanit.to_csv(os.path.join(cwd,"sani.csv"))
expnd.to_csv(os.path.join(cwd,"expend.csv"))

