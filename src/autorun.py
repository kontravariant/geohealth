from data import data_get
from munge import munge
import subprocess,os

'''
        Get all data in python,
        munge all data into countryframe database

        Create panel data in R and add income codes
'''

#run get all data
data_get.get_all()
#run munge all data
munge.munge_all()

#run R script to reshape and code incomes
curdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),))
r_reshape_fname = os.path.join(curdir,'munge','db_reshape.R')
cmd = ['Rscript',r_reshape_fname]
print(cmd)
subprocess.run(cmd)
