#!/usr/bin/python

import sys, getopt, os
from gui import *
from constants import *
'''
script for showing sequence logo GUI.
Running in a separate process.
'''

def run(search_id, flag):
    root = Tk()
    seqs = []
    path = 'cache/'+str(search_id)

    lineNum = 0
    query = 'default'
    with open(path, 'r') as f:
        for line in f:
            if lineNum == 0:
                query = line.strip()
            elif lineNum >= 2:
                seqs.append(line.strip())
            lineNum += 1
    logo = LogoGUI(search_id, query, seqs, 20, flag, root)
    size = str(LOGO_GUI_WIDTH)+'x'+str(LOGO_GUI_HEIGHT)
    root.geometry(size)
    root.mainloop()

def main(search_id, flag):
    # make tmp directory for each serach
    if not os.path.exists(CACHE_PATH+str(search_id)):
        os.makedirs(CACHE_PATH+str(search_id))
    run(search_id, flag)

if __name__ == "__main__":
    '''
    argv[1]: search_id
    argv[2]: flag for logo type: sequence logo or frequency logo
    '''
    main(sys.argv[1], sys.argv[2])
