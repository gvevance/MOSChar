# A more functional version of the script with user input. With length sweep.
# Program flow - Enter lengths we want to simulate
# Width is user-input
# Run the code in a for loop and get back the numpy arrays for post-processing

from subprocess import call
import os
import numpy as np
import matplotlib.pyplot as plt

# define constants
 
cir_filename = os.path.join(os.getcwd(),'tmp/temp_pmos_v2.cir')
value_file = os.path.join(os.getcwd(),'tmp/values_pmos_v2.txt')
model_file = os.path.join(os.getcwd(),'Model_files/130nm_bulk.pm')
log_file = os.path.join(os.getcwd(),'tmp/pmos_plotparams.log')

def generate_contents(length,width):
    
    contents = f'''PMOS characterisation

*************************************
* Include model file 
*************************************
.include {model_file}

*************************************
* Defining arameters 
*************************************
.param len = {length}u
.param width = {width}u 
.param lmin = 0.13u

*************************************
* Circuit definition
*************************************
vsg 1 0 dc 0.5
M1 0 0 1 1 pmos l={{len}} w={{width}} as={{2*lmin*width}} ad={{2*lmin*width}} ps={{4*lmin+2*width}} pd={{4*lmin+2*width}}

*************************************
* Control section
*************************************

.control 

save @M1[id], @M1[vdsat], @M1[vth], @M1[cgs], @M1[cgg],
+ @M1[gm], @M1[gds], @M1[gmbs], @M1[vsat]

* DC sweep
dc vsg 0.05 1.3 0.01

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

def prepare_for_post_proc(width):
    
    width_c = float(width) * 1e-6

    with open(value_file) as txtfile :
        temp = np.genfromtxt(txtfile, dtype=float)

    vsg    = temp[1:,0]
    id     = temp[1:,1]
    vdsat  = temp[1:,2]
    cgs    = -temp[1:,3]
    cgg    = temp[1:,4]
    gm     = temp[1:,5]
    gds    = temp[1:,6]
    gmbs   = temp[1:,7]
    vth    = temp[1:,8]

    # custom definitions

    gm_by_id   = gm/id 
    gain       = gm/gds
    ft         = gm/cgg
    gm_by_gmbs = gm/gmbs

    # /width quantities

    id_wid     = id/width_c
    gm_wid     = gm/width_c
    gds_wid    = gds/width_c
    cgg_wid    = cgg/width_c
    cgs_wid    = cgs/width_c
    gmbs_wid   = gmbs/width_c

    return [vsg,gm_by_id,id_wid,vdsat,cgs_wid,cgg_wid,gm_wid,gds_wid,vth,gain,ft,gmbs_wid,gm_by_gmbs]

def plot_figures(sim_values,length,plot_list):

    vsg,gm_by_id,id_wid,vdsat,cgs_wid,cgg_wid,gm_wid,gds_wid,vth,gain,ft,gmbs_wid,gm_by_gmbs = sim_values

    if "gm/id" in plot_list:
        plt.figure(1) # gm/Id vs vsg
        plt.plot( vsg , gm_by_id , label='Len = '+length+'u' )
        plt.ylabel("gm/Id")
        plt.xlabel("Vsg")
        plt.title("Plot of gm/Id vs Vsg")
        plt.grid(True)
        plt.legend()

    if "id/w" in plot_list:
        plt.figure(2) # log10(id/W) vs gm/Id
        plt.semilogy( gm_by_id , id_wid , label='Len = '+length+'u' )
        plt.ylabel("Id/W")
        plt.xlabel("gm/Id")
        plt.title("Plot of Id/W vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "gm/w" in plot_list:
        plt.figure(3) # log10(gm/W) vs gm/Id
        plt.semilogy( gm_by_id , gm_wid , label='Len = '+length+'u' )
        plt.ylabel("gm/W")
        plt.xlabel("gm/Id")
        plt.title("Plot of gm/W vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "gds/w" in plot_list:
        plt.figure(4) # log10(gds/W) vs gm/Id
        plt.semilogy( gm_by_id , gds_wid , label='Len = '+length+'u' )
        plt.ylabel("gds/W")
        plt.xlabel("gm/Id")
        plt.title("Plot of gds/W vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "gain" in plot_list:
        plt.figure(5) # log10(gain/W) vs gm/Id
        plt.semilogy( gm_by_id , gain , label='Len = '+length+'u' )
        plt.ylabel("gain")
        plt.xlabel("gm/Id")
        plt.title("Plot of gain vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "cgg/w" in plot_list:
        plt.figure(6) # log10(cgg/W) vs gm/Id
        plt.semilogy( gm_by_id , cgg_wid , label='Len = '+length+'u' )
        plt.ylabel("cgg/W")
        plt.xlabel("gm/Id")
        plt.title("Plot of cgg/W vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "cgs/w" in plot_list:
        plt.figure(7) # log10(cgs/W) vs gm/Id
        plt.semilogy( gm_by_id , cgs_wid , label='Len = '+length+'u' )
        plt.ylabel("cgs/W")
        plt.xlabel("gm/Id")
        plt.title("Plot of cgs/W vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "ft" in plot_list:
        plt.figure(8) # log10(ft) vs gm/Id
        plt.semilogy( gm_by_id , ft , label='Len = '+length+'u' )
        plt.ylabel("ft")
        plt.xlabel("gm/Id")
        plt.title("Plot of ft vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "vdsat" in plot_list:
        plt.figure(9) # vdsat vs gm/Id
        plt.plot( gm_by_id , vdsat , label='Len = '+length+'u' )
        plt.ylabel("vdsat")
        plt.xlabel("gm/Id")
        plt.title("Plot of vdsat vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "vth" in plot_list:
        plt.figure(10) # vth vs gm/Id
        plt.plot( gm_by_id , vth , label='Len = '+length+'u' )
        plt.ylabel("vth")
        plt.xlabel("gm/Id")
        plt.title("Plot of vth vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "gmbs/w" in plot_list:
        plt.figure(11) # log10(gmbs/W) vs gm/Id
        plt.semilogy( gm_by_id , gmbs_wid , label='Len = '+length+'u' )
        plt.ylabel("gmbs/W")
        plt.xlabel("gm/Id")
        plt.title("Plot of gmbs/W vs gm/Id")
        plt.grid(True)
        plt.legend()

    if "gm/gmbs" in plot_list:
        plt.figure(12) # log10(gm/gmbs) vs gm/Id
        plt.plot( gm_by_id , gm_by_gmbs , label='Len = '+length+'u' )
        plt.ylabel("gm/gmbs")
        plt.xlabel("gm/Id")
        plt.title("Plot of gm/gmbs vs gm/Id")
        plt.grid(True)
        plt.legend()

def pmos_plot_demo_1():
    
    print("\n****** Diode connected PMOS gm/Id curves ******\n")
    print("Minimum length in the 130nm_bulk.pm technology is 0.13u. Minimum width is probably some 200n\n")
    
    print("1 - Default mode (view trends)\n2 - Custom mode\n")
    mode = int(input("Enter mode : "))

    if mode == 1 :
        width = '100'
        len_list = ['0.3']

    elif mode == 2 :
        width = str(input("\nEnter width (in um) : "))
        len_list = str(input("Enter lengths (in um) (space-separated) : ")).split()
    
    else :
        print("Error. Incorrect mode entered. Exiting ...")
        exit()

    print("\nEnter ( space-separated ) : gm/id, vdsat, gm/w, gds/w, id/W, cgs/w, cgg/w, vth, gain, ft, gmbs/w, gm/gmbs \n")
    plot_superlist = ["gm/id", "vdsat", "gm/w", "gds/w", "id/w", "cgs/w", "cgg/w", "vth", "gain", "ft", "gmbs/w", "gm/gmbs"]
    plot_list = input("Enter quantities you want to plot using appropriate codes : ").split()

    while ((set(plot_list).issubset(set(plot_superlist)) == False ) or (len(plot_list) == 0)):
        plot_list = input("Incorrect code entered. Please re-enter : ").split()
    print()

    for length in len_list:
        contents = generate_contents(length,width)
        write_cir(contents)
        call(f"ngspice {cir_filename} > {log_file}",shell=True) 

        sim_values = prepare_for_post_proc(width)

        plot_figures(sim_values,length,plot_list)
        
    plt.show()