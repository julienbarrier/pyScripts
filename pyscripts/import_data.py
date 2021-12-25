## import_data.py
## Julien Barrier
## @julienbarrier
##
## Definition of functions to import navigate in files and import some

import glob
import copy
import pandas as pd

def find_dirs(d):
    "list the directories in directory d"
    import os
    return [os.path.join(d,o + '/').replace('\\','/') for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

def find_files(indir, fbase):
    "list the text files in directory indir containing fbase"
    scans = glob.glob(indir+'*'+fbase+'*.txt')
    print('found %s text files'%len(scans))
    return scans

def import_files(indir,fbase):
    "import the text files in directory indir containing fbase"
    list = find_files(indir,fbase);
    list.sort();
    file = [None] * len(list)
    temp = copy.copy(file)
    for filenumber in range(len(list)):
        file[filenumber]= pd.read_csv('%s'%list[filenumber],sep='\s+')
        temp[filenumber] = list[filenumber][len(indir):len(indir)+3]
    del list

    return temp,file
