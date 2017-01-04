import pandas as pd
import os

datadir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data/'))

def wdi_munge():

    src_dir = os.path.join(datadir,'raw/wdi/')
    dat = pd.read_csv(src_dir + "WDI_Data.csv", encoding='latin1')
    water = dat[dat['Indicator Name'] == "Improved water source (% of population with access)"]
    sani = dat[dat['Indicator Name'] == "Improved sanitation facilities (% of population with access)"]
    expend = dat[dat['Indicator Name'] == "Health expenditure per capita, PPP (constant 2011 international $)"]

    dst_dir = os.path.join(datadir,'intermediate/wdi/')
    # remove all except .DS_Store
    # write csv's
    water.to_csv(dst_dir + "water.csv")
    sani.to_csv(dst_dir + "sani.csv")
    expend.to_csv(dst_dir + "expend.csv")

if __name__ == "__main__":
    wdi_munge()