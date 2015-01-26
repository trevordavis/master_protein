#!/usr/bin/env python
"""
Put settings here for various files necessary
author:   Tim Tregubov, 12/2014
"""

import os


class Default(object):
    """
    default settings for the server"
    """

    BASEDIR = os.path.dirname(__file__)

    # # # #  edit this section # # # #
    MASTER_PATH = os.path.join(BASEDIR, 'external/master/master')           #
    CREATEPDS_PATH = os.path.join(BASEDIR, 'external/master/createPDS')     #
    EXTRACTPDB_PATH = os.path.join(BASEDIR, 'external/master/extractPDB')   #
    PROCESSING_PATH = os.path.join(BASEDIR, 'processing')                   # directory to hold output files
    CONFIG_PATH = os.path.join(BASEDIR, 'config')                           # config dir for targetlists
    LIBRARY_PATH = os.path.join(BASEDIR, 'bc-30-sc-correct-20141022')       # the database directory
    TARGET_LIST_PATH = os.path.join(CONFIG_PATH, 'ram_targetList')          # this is the name of the targetList file
    # # # #  done edits # # # #

    ALLOWED_EXTENSIONS = frozenset(['pdb', 'pds'])
    ALLOWED_ARGS = frozenset(['bbRMSD', 'dEps', 'ddZScore',
                              'matchInFile', 'matchOutFile', 'phiEps', 'psiEps',
                              'query', 'rmsdCut', 'rmsdMode', 'seqOutFile', 'structOut',
                             'structOutType', 'target', 'targetList', 'topN', 'tune'])