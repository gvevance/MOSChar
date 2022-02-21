# This program is designed to help the IC designer to choose 
# transistor sizes upon inputting the required device parameters 
# (mainly small signal parameters). Will probably involve some 
# efficient DSA search algorithm and some efficient file handling.

from subprocess import call
import os
import numpy as np

vmin_tolerance = 0.05  #! cannot give voltage as 0. So min tolerance

cir_filename = os.path.join(os.getcwd(),'tmp/temp_nmos_v3.cir')
value_file = os.path.join(os.getcwd(),'tmp/values_nmos_v3.txt')
model_file = os.path.join(os.getcwd(),'Model_files/130nm_bulk.pm')
constraints_file = os.path.join(os.getcwd(),'tmp/constraints_nmos.txt')

width = '100' # in um

def define_constraints():
    ''' Define the constraints to search for after user-input. Writes to a file for the program to read from. 
        Range is to be entered carefully. If you want gm/W > 10, enter the range as "10 10000",
        i.e., 10 and a very large number. '''
    
    print("\nWhat parameters do you have constraints on ? Enter appropriate code (\"0\" when done)...\n")
    print("\"gm_wid\" - gm/W \n\"gds_wid\" - gds/W \n\"gain\" - gm/gds \n\"ft\" - ft \n")
    
    # clear already existing lines in constraints.txt (create it if it doesn' exist)
    c_file = open(constraints_file,'w+')
    c_file.close()

    c_file = open(constraints_file,'a') 
    ret = "start"
    while(ret != '0'):
        ret = input("Enter option : ").strip()
        
        if (ret == "gm_wid") :
            gm_wid_min , gm_wid_max = input("Enter gm/W range : ").split()
            c_file.write("gm/W "+gm_wid_min+" "+gm_wid_max+"\n")

        elif (ret == "gds_wid"):
            gds_wid_min , gds_wid_max = input("Enter gds/W range : ").split()
            c_file.write("gds/W "+gds_wid_min+" "+gds_wid_max+"\n")

        elif (ret == "gain"):
            gain_min , gain_max = input("Enter gain range : ").split()
            c_file.write("gain "+gain_min+" "+gain_max+"\n")

        elif (ret == "ft"):
            ft_min , ft_max = input("Enter ft range : ").split()
            c_file.write("ft "+ft_min+" "+ft_max+"\n")

        elif (ret == "0"):
            print()
            c_file.close()

        else :
            print("Enter valid option. \"0\" if you're done.")
            ret = "invalid code"

    # printing chosen constraints
    
    
def generate_contents(len,vgs_min,vgs_max):
    
    if vgs_min == '0' :
        vgs_min = str(vmin_tolerance)
    
    contents = f'''NMOS characterisation

*************************************
* Include model file 
*************************************
.include {model_file}

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

save @M1[id], @M1[vdsat], @M1[vth], @M1[cgs], @M1[cgg],
+ @M1[gm], @M1[gds], @M1[gmbs], @M1[vsat]

* DC sweep
dc vgs {vgs_min} {vgs_max} 0.01

* Run the sim
run

set filetype=ascii
set wr_singlescale
set wr_vecnames

wrdata {value_file} @M1[id], @M1[vdsat], @M1[cgs], @M1[cgg] 
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

def write_cir(contents):
    
    if not os.path.exists(os.path.join(os.getcwd(),"tmp/")) :
        os.mkdir(os.path.join(os.getcwd(),"tmp/"))
        
    with open(cir_filename,'w+') as file :
        file.write(contents)

def extract_params():
    
    width_c = float(width) * 1e-6

    with open(value_file) as txtfile :
        temp = np.genfromtxt(txtfile, dtype=float)

    params = {}

    params["vgs"]    = temp[1:,0]
    params["id"]     = temp[1:,1]
    params["vdsat"]  = temp[1:,2]
    params["cgs"]    = -temp[1:,3]
    params["cgg"]    = temp[1:,4]
    params["gm"]     = temp[1:,5]
    params["gds"]    = temp[1:,6]
    params["gmbs"]   = temp[1:,7]
    params["vth"]    = temp[1:,8]

    # custom definitions

    params["gm_by_id"]   = params["gm"]/params["id"] 
    params["gain"]       = params["gm"]/params["gds"]
    params["ft"]         = params["gm"]/params["cgg"]
    params["gm_by_gmbs"] = params["gm"]/params["gmbs"]

    # /width quantities

    params["id_wid"]     = params["id"]/width_c
    params["gm_wid"]     = params["gm"]/width_c
    params["gds_wid"]    = params["gds"]/width_c
    params["cgg_wid"]    = params["cgg"]/width_c
    params["cgs_wid"]    = params["cgs"]/width_c
    params["gmbs_wid"]   = params["gmbs"]/width_c

    return params

def op_search(params):
    
    vgs = params["vgs"]
    gm_by_id = params["gm_by_id"]
    id_wid = params["id_wid"]
    vdsat = params["vdsat"]
    cgs_wid = params["cgs_wid"]
    cgg_wid = params["cgg_wid"]
    gm_wid = params["gm_wid"]
    gds_wid = params["gds_wid"]
    vth = params["vth"]
    gain = params["gain"]
    ft = params["ft"]
    gmbs_wid = params["gmbs_wid"]
    gm_by_gmbs = params["gm_by_gmbs"]
    
    # print(vgs[(gm_wid <50) & (gm_wid > 30)])

    # initial condition values
    gm_wid_min , gds_wid_min , gain_min , ft_min = 0,0,0,0
    gm_wid_max , gds_wid_max , gain_max , ft_max = 1e16,1e16,1e16,1e16 
    
    # parse constraints.txt
    with open(constraints_file) as c_file :
        c_file_lines = c_file.readlines()
    
    for line in c_file_lines :
        
        name,llim,ulim = line.split()
        llim = float(llim)
        ulim = float(ulim)

        if name == 'gm/W' :
            gm_wid_min , gm_wid_max = llim , ulim 
        elif name == 'gds/W' :
            gds_wid_min , gds_wid_max = llim , ulim
        elif name == 'gain' :
            gain_min , gain_max = llim , ulim
        elif name == 'ft' :
            ft_min , ft_max = llim , ulim
        else :
            print("Error in constraints.txt")
            exit()
    
    bool_vec = (gm_wid<gm_wid_max) & (gm_wid>gm_wid_min) & (gds_wid<gds_wid_max) & (gds_wid>gds_wid_min) & \
               (gain<gain_max) & (gain>gain_min) & (ft<ft_max) & (ft>ft_min)

    if len(vgs[bool_vec] != 0):
        print("\nPossible Vgs values for the selected device param range are : \n")
        
        # printing valid operating points and corresponding device parameters
        for i in range(len(vgs[bool_vec])):
            print(f"Vgs = {vgs[bool_vec][i]:.3f}\tvdsat = {vdsat[bool_vec][i]:.2f}\tgm/Id = {gm_by_id[bool_vec][i]:.2f}\t\
id/W = {id_wid[bool_vec][i]:.2f}\tgm/W = {gm_wid[bool_vec][i]:.2f}\tgain = {gain[bool_vec][i]:.1f}\tft = {ft[bool_vec][i]:.2E}")
        print()  # prints newline

    else :
        print("\nNo valid operating point found. Try another length or voltage range.\n")


def nmos_opsearch_demo_1():

    print("\nSearch for the right bias point for transistors.\n")
    vgs_min , vgs_max = str(input("Enter VGS range (in volts) : ")).split()
    len = str(input("Enter length ( in um ) : "))

    define_constraints()  # does not need any input or output. Writes to a file.
    contents = generate_contents(len,vgs_min,vgs_max)
    write_cir(contents)
    call(['ngspice',cir_filename])

    params = extract_params()
    op_search(params)  # does not need any input. Uses the sim results and constraints file 