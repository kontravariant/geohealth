import pandas as pd
import os
import re
import shutil

def who_munge():

    outframe = pd.DataFrame()
    cwd = '../../data/raw/who'
    tgt_dir = '../../data/intermediate/who'

    for fname in os.listdir(cwd):
        res = re.search("\((.*?)\)",fname)
        df = pd.read_csv(os.path.join(cwd, fname),skiprows=1)

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