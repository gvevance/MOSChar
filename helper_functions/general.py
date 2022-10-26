# general helper functions

import os

def init_setup(circuit) :
    
    CWD = os.getcwd()
    MODEL_DIR = os.path.join(CWD,'Model_files/')
    MODEL_FILE = os.path.join(CWD,'Model_files/130nm_bulk.pm')
    
    if circuit == '1' :
        DIR = os.path.join(CWD,'data/circuit1/')
    elif circuit == '2' :
        DIR = os.path.join(CWD,'data/circuit2/')
    elif circuit == '3' :
        DIR = os.path.join(CWD,'data/circuit3/')
    elif circuit == '4' :
        DIR = os.path.join(CWD,'data/circuit4/')
    else :          
        exit()

    if not os.path.exists(DIR) :
        os.makedirs(DIR)
        
    NETLIST_FILE = os.path.join(DIR,'circuit1.cir')
    LOG_FILE = os.path.join(DIR,'circuit1.log')
    SAVEDATA_FILE_FORMAT = os.path.join(DIR,'savedata.txt')
    SEARCH_DEFINE_FILE = os.path.join(DIR,'search_definition.txt')

    if not os.path.exists(DIR) :
        os.makedirs(DIR)

    return CWD, MODEL_DIR, MODEL_FILE, DIR, NETLIST_FILE, LOG_FILE, SAVEDATA_FILE_FORMAT, SEARCH_DEFINE_FILE


def write_netlist_to_file(directory,NETLIST_FILE,contents):
    
    if not os.path.exists(directory) :
        os.mkdir(directory)

    with open(NETLIST_FILE,'w+') as file :
        file.write(contents)
