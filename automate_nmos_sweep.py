# A more functional version of the script with user input. With length sweep.
# Program flow - Enter lengths we want to simulate
# Width is fixed (defined as a constant initially)
# Run the code in a for loop and get back the numpy arrays for post-processing

from subprocess import call
import numpy as np
import matplotlib.pyplot as plt

circuit = 'circuit.cir'
value_file = 'values.txt'

def generate_contents(len,width):
    
    contents = f'''NMOS characterisation

    *************************************
    * Include model file 
    *************************************
    .include 130nm_bulk.pm

    *************************************
    * Defining arameters 
    *************************************
    .param len = {len}u
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

    save @M1[id], @M1[vdsat], @M1[vth], @M1[cgs], @M1[cgg], @M1[cds] ,
    + @M1[cdd], @M1[gm], @M1[gds], @M1[gmbs], @M1[vsat]

    * DC sweep
    dc vgs 0.05 1.3 0.01

    * Run the sim
    run

    set filetype=ascii
    set wr_singlescale
    set wr_vecnames

    wrdata {value_file} @M1[id], @M1[vdsat], @M1[cgs], @M1[cgg], @M1[cds] 
    + @M1[cdd], @M1[gm], @M1[gds], @M1[gmbs], @M1[vth]

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

def write_cir(contents):
    with open(circuit,'w') as file :
        file.write(contents)

def prepare_for_post_proc():
    pass

def main():
    
    print("Minimum length in the 130nm_bulk.pm technology is 0.13u. Minimum width is probably some 0.2u")
    width = str(input("Enter width (in um) : "))
    len_vec = str(input("Enter lengths (in um) (space-separated) : "))
    len_list = len_vec.split()
    
    for len in len_list:
        contents = generate_contents(len,width)
        write_cir(contents)
        call(['ngspice',circuit]) 

        prepare_for_post_proc()



if __name__=="__main__":
    main()