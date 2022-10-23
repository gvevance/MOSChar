# general helper functions

import os

def init_setup() :
    
    CWD = os.getcwd()
    MODEL_DIR = os.path.join(CWD,'Model_files/')
    MODEL_FILE = os.path.join(CWD,'Model_files/130nm_bulk.pm')
    TMP_DIR = os.path.join(CWD,'/tmp/')
    NETLIST_FILE = os.path.join(TMP_DIR,'filename.cir')     # TODO change to appropriate naming convention
    LOG_FILE = os.path.join(TMP_DIR,'filename.log')         # TODO change to appropriate naming convention
    SAVEDATA_FILE = os.path.join(TMP_DIR,'filename.txt')    # TODO change to appropriate naming convention

    return CWD, MODEL_DIR, MODEL_FILE, TMP_DIR, NETLIST_FILE, LOG_FILE, SAVEDATA_FILE


def generate_netlist_circuit_1(MODEL_FILE,SAVEDATA_FILE,length,width):
    contents = f'''NMOS characterisation

*************************************
* Include model file 
*************************************
.include {MODEL_FILE}

*************************************
* Defining arameters 
*************************************
.param len = {length}u
.param width = {width}u 
.param lmin = 0.13u

*************************************
* Circuit definition
*************************************
vgs 1 0 dc 0.5
M1 1 1 0 0 nmos l={{len}} w={{width}} as={{2*lmin*width}} ad={{2*lmin*width}} ps={{4*lmin+2*width}} pd={{4*lmin+2*width}}

*************************************
* Control section
*************************************

.control 

save @M1[id], @M1[vdsat], @M1[vth], @M1[cgs], @M1[cgg],
+ @M1[gm], @M1[gds], @M1[gmbs], @M1[vsat]

* DC sweep
dc vgs 0.05 1.3 0.01

* Run the sim
run

set filetype=ascii
set wr_singlescale
set wr_vecnames

wrdata {SAVEDATA_FILE} @M1[id], @M1[vdsat], @M1[cgs], @M1[cgg] 
+ @M1[gm], @M1[gds], @M1[gmbs], @M1[vth]

* Plot commands
* plot @M1[id]
* plot @M1[gm]
* plot @M1[gmbs]
* plot @M1[gds]
* plot @M1[cgs]
* plot @M1[cgg]
* plot @M1[vdsat]
* plot @M1[vsat]


exit
.endc

*************************************
* End of file
*************************************
.end
'''

    return contents


def write_netlist_to_file(directory,NETLIST_FILE,contents):
    
    if not os.path.exists(directory) :
        os.mkdir(directory)

    with open(NETLIST_FILE,'w+') as file :
        file.write(contents)
