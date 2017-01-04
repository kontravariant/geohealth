
#no munging yet just copying
import os
import shutil

dat_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data/'))

def pwt_munge():

    raw_dir = os.path.join(dat_dir,'raw/pwt/')
    int_dir = os.path.join(dat_dir,'intermediate/pwt/')
    for fname in os.listdir(raw_dir):
        shutil.copy(src=raw_dir+fname, dst=int_dir+fname)

if __name__ == "__main__":
    pwt_munge()