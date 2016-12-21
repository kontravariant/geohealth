import os
import pandas as pd
from pandas.io import sql
import numpy as np
import re
from itertools import chain
''''''
import sqlite3

cwd = '../../data/'
con_path = os.path.join(cwd,'country_data.sqlite')
con = sqlite3.connect(con_path)
dat_read = pd.read_sql("select * from GBR", con)
print(dat_read)
