import pandas as pd
import os
import re
import shutil

datadir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data/'))

def who_munge():

    outframe = pd.DataFrame()
    cwd = os.path.join(datadir,'raw/who/')
    tgt_dir = os.path.join(datadir,'intermediate/who/')

    for fname in os.listdir(cwd):
        res = re.search("\((.*?)\)",fname)
        df = pd.read_csv(os.path.join(cwd, fname),skiprows=1,encoding='latin1')

        if res:
            stat = res.group(1)
            newname = stat+'.csv'
        else:
            pass
            newname = fname

        df.to_csv(os.path.join(tgt_dir,newname),index=False)
        # shutil.copy(src=os.path.join(cwd, fname), dst=os.path.join(tgt_dir, newname))

if __name__ == "__main__":
    who_munge()