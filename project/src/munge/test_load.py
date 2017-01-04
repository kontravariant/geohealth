import pickle, os
datadir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data/'))
cwd = os.path.join(datadir, 'processed/')

countryframes = pickle.load(open(os.path.join(cwd,'countries.pkl'), 'rb'))
print(countryframes['SYC'])