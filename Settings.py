#!/usr/bin/env python

import os


class Default(object):

    CELERY_BROKER_URL = 'amqp://guest@127.0.0.1//'
    CELERY_BACKEND = 'amqp'

    ALLOWED_EXTENSIONS = frozenset(['pdb', 'pds'])
    ALLOWED_ARGS = frozenset(['bbRMSD', 'dEps', 'ddZScore',
                              'matchInFile', 'matchOutFile', 'phiEps', 'psiEps',
                              'query', 'rmsdCut', 'rmsdMode', 'seqOutFile', 'structOut',
                              'structOutType', 'target', 'targetList', 'topN', 'tune'])
    BASEDIR = os.path.dirname(__file__)
    MASTER_PATH = os.path.join(BASEDIR, 'external/master/master')
    CREATEPDS_PATH = os.path.join(BASEDIR, 'external/master/createPDS')
    EXTRACTPDB_PATH = os.path.join(BASEDIR, 'external/master/extractPDB')
    PROCESSING_PATH = os.path.join(BASEDIR, 'processing')
    CONFIG_PATH = os.path.join(BASEDIR, 'config')
    LIBRARY_PATH = os.path.join(BASEDIR, 'bc-30-sc-correct-20141022')
    TARGET_LIST_PATH = os.path.join(CONFIG_PATH, 'ram_targetList')