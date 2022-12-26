# general helper functions

from os import getcwd, makedirs
from os.path import exists, join


def init_setup() :
    
    CWD = getcwd()
    MODEL_DIR = join(CWD,'Model_files/')
    MODEL_FILE = join(CWD,'Model_files/130nm_bulk.pm')
    
    DIR = join(CWD,'data/circuit/')

    if not exists(DIR) :
        makedirs(DIR)
        
    NETLIST_FILE = join(DIR,'circuit.cir')
    LOG_FILE = join(DIR,'circuit.log')
    SAVEDATA_FILE_FORMAT = join(DIR,'savedata.txt')
    SEARCH_DEFINE_FILE = join(DIR,'search_definition.txt')

    if not exists(DIR) :
        makedirs(DIR)

    return CWD, MODEL_DIR, MODEL_FILE, DIR, NETLIST_FILE, LOG_FILE, SAVEDATA_FILE_FORMAT, SEARCH_DEFINE_FILE

def write_netlist_to_file(directory,NETLIST_FILE,contents):
    
    if not exists(directory) :
        makedirs(directory)

    with open(NETLIST_FILE,'w+') as file :
        file.write(contents)
