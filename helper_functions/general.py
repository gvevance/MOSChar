# general helper functions

import os

def init_setup() :
    
    CWD = os.getcwd()
    MODEL_DIR = os.path.join(CWD,'Model_files/')
    MODEL_FILE = os.path.join(CWD,'Model_files/130nm_bulk.pm')
    TMP_DIR = os.path.join(CWD,'tmp/')
    NETLIST_FILE = os.path.join(TMP_DIR,'filename.cir')     # TODO change to appropriate naming convention
    LOG_FILE = os.path.join(TMP_DIR,'filename.log')         # TODO change to appropriate naming convention
    SAVEDATA_FILE = os.path.join(TMP_DIR,'filename.txt')    # TODO change to appropriate naming convention
    SEARCH_DEFINE_FILE = os.path.join(TMP_DIR,'search_definition.txt')

    return CWD, MODEL_DIR, MODEL_FILE, TMP_DIR, NETLIST_FILE, LOG_FILE, SAVEDATA_FILE, SEARCH_DEFINE_FILE


def write_netlist_to_file(directory,NETLIST_FILE,contents):
    
    if not os.path.exists(directory) :
        os.mkdir(directory)

    with open(NETLIST_FILE,'w+') as file :
        file.write(contents)
