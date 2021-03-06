# A more functional version of the script with user input. With length sweep.
# Program flow - Enter lengths we want to simulate
# Width is user-input
# Run the code in a for loop and get back the numpy arrays for post-processing

from subprocess import call
import os
import numpy as np
import matplotlib.pyplot as plt

# define constants
 
cir_filename = os.path.join(os.getcwd(),'tmp/temp_nmos_v2.cir')
value_file = os.path.join(os.getcwd(),'tmp/values_nmos_v2.txt')
model_file = os.path.join(os.getcwd(),'Model_files/130nm_bulk.pm')
log_file = os.path.join(os.getcwd(),'tmp/nmos_plotparams.log')


def generate_contents(length,width):
    
    contents = f'''NMOS characterisation

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


def plot_figures(params,length,plot_list):

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

    if any([x for x in plot_list if x != "gm/id"]) :
        x = input("Plot versus gm/id or vgs ? : (1/2) ")
        while x not in ['1','2'] :
            x = input("Invalid input entered. Plot versus gm/id or vgs ? : (1/2) ")
        
    if "gm/id" in plot_list:
        plt.figure(1) # gm/Id vs vgs
        plt.plot( vgs , gm_by_id , label='Len = '+length+'u' )
        plt.ylabel("gm/Id")
        plt.xlabel("Vgs")
        plt.grid(True)
        plt.legend()
        plt.title("Plot of gm/Id vs Vgs")

    if "id/w" in plot_list:
        plt.figure(2) # log10(id/W) vs gm/Id
        plt.ylabel("Id/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of Id/W vs gm/Id")
            plt.plot( gm_by_id , id_wid , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of Id/W vs vgs")
            plt.plot( vgs , id_wid , label='Len = '+length+'u' )
            plt.legend()

    if "gm/w" in plot_list:
        plt.figure(3) # log10(gm/W) vs gm/Id
        plt.ylabel("gm/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gm/W vs gm/Id")
            plt.plot( gm_by_id , gm_wid , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of gm/W vs vgs")
            plt.plot( vgs , gm_wid , label='Len = '+length+'u' )
            plt.legend()

    if "gds/w" in plot_list:
        plt.figure(4) # log10(gds/W) vs gm/Id
        plt.ylabel("gds/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gds/W vs gm/Id")
            plt.plot( gm_by_id , gds_wid , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of gds/W vs vgs")
            plt.plot( vgs , gds_wid , label='Len = '+length+'u' )
            plt.legend()

    if "gain" in plot_list:
        plt.figure(5) # log10(gain/W) vs gm/Id
        plt.ylabel("gain")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gain vs gm/Id")
            plt.plot( gm_by_id , gain , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of gain vs vgs")
            plt.plot( vgs , gain , label='Len = '+length+'u' )
            plt.legend()

    if "cgg/w" in plot_list:
        plt.figure(6) # log10(cgg/W) vs gm/Id
        plt.ylabel("cgg/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of cgg/W vs gm/Id")
            plt.plot( gm_by_id , cgg_wid , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of cgg/W vs vgs")
            plt.plot( vgs , cgg_wid , label='Len = '+length+'u' )
            plt.legend()

    if "cgs/w" in plot_list:
        plt.figure(7) # log10(cgs/W) vs gm/Id
        plt.ylabel("cgs/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of cgs/W vs gm/Id")
            plt.plot( gm_by_id , cgs_wid , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of cgs/W vs vgs")
            plt.plot( vgs , cgs_wid , label='Len = '+length+'u' )
            plt.legend()

    if "ft" in plot_list:
        plt.figure(8) # log10(ft) vs gm/Id
        plt.ylabel("ft")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of ft vs gm/Id")
            plt.plot( gm_by_id , ft , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of ft vs vgs")
            plt.plot( vgs , ft , label='Len = '+length+'u' )
            plt.legend()

    if "vdsat" in plot_list:
        plt.figure(9) # vdsat vs gm/Id
        plt.ylabel("vdsat")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of vdsat vs gm/Id")
            plt.plot( gm_by_id , vdsat , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of vdsat vs vgs")
            plt.plot( vgs , vdsat , label='Len = '+length+'u' )
            plt.legend()

    if "vth" in plot_list:
        plt.figure(10) # vth vs gm/Id
        plt.ylabel("vth")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of vth vs gm/Id")
            plt.plot( gm_by_id , vth , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of vth vs vgs")
            plt.plot( vgs , vth , label='Len = '+length+'u' )
            plt.legend()

    if "gmbs/w" in plot_list:
        plt.figure(11) # log10(gmbs/W) vs gm/Id
        plt.ylabel("gmbs/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gmbs/W vs gm/Id")
            plt.plot( gm_by_id , gmbs_wid , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of gmbs/W vs vgs")
            plt.plot( vgs , gmbs_wid , label='Len = '+length+'u' )
            plt.legend()

    if "gm/gmbs" in plot_list:
        plt.figure(12) # log10(gm/gmbs) vs gm/Id
        plt.ylabel("gm/gmbs")
        plt.grid(True)
        
        if x == '1' :
        
            plt.xlabel("gm/Id")
            plt.title("Plot of gm/gmbs vs gm/Id")
            plt.plot( gm_by_id , gm_by_gmbs , label='Len = '+length+'u' )
            plt.legend()
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of gm/gmbs vs vgs")
            plt.plot( vgs , gm_by_gmbs , label='Len = '+length+'u' )
            plt.legend()

def nmos_plot_demo_1():
    
    print("\n****** Diode connected NMOS ******\n")
    print("Minimum length in the 130nm_bulk.pm technology is 0.13u. Minimum width is probably some 200n\n")
    
    print("1 - Default mode (view trends)\n2 - Custom mode\n")
    mode = int(input("Enter mode : "))

    if mode == 1 :
        width = '100'
        len_list = ['0.3']

        print(f"\nwidth = {width}u \nlength = {len_list[0]} \n")

    elif mode == 2 :

        lmin = 0.13
        wmin = 0.2

        width = str(input(f"\nEnter width (in um > {wmin}) : "))
        
        while (True) :
            
            break_ = False
            try :
                if float(width) < wmin :
                    width = str(input(f"Entered width is too small. Enter width (> {wmin}um) : "))
                    
                else :
                    break_ = True
                    
            except :
                width = str(input(f"Improper width entered. Enter width (> {wmin}um) : "))

            if break_ :
                break


        len_list = str(input(f"\nEnter lengths (in um > {lmin}) (space-separated) : ")).split()

        while (True) :
            
            break_ = False
            try :
                if any([(float(length) < lmin) for length in len_list]) :
                    len_list = str(input(f"At least one entered length is too small. Enter lengths (in um > {lmin}) (space-separated) : ")).split()
                else :
                    break_ = True
                    
            except :
                len_list = str(input(f"Improper lengths entered. Enter lengths (in um > {lmin}) (space-separated) : ")).split()

            if break_ :
                break
    
    else :
        print("Error. Incorrect mode entered. Exiting ...")
        exit()

    print("\nEnter ( space-separated ) : gm/id, vdsat, gm/w, gds/w, id/w, cgs/w, cgg/w, vth, gain, ft, gmbs/w, gm/gmbs \n")
    plot_superlist = ["gm/id", "vdsat", "gm/w", "gds/w", "id/w", "cgs/w", "cgg/w", "vth", "gain", "ft", "gmbs/w", "gm/gmbs"]
    plot_list = input("Enter quantities you want to plot using appropriate codes : ").split()

    while ((set(plot_list).issubset(set(plot_superlist)) == False ) or (len(plot_list) == 0)):
        plot_list = input("Incorrect code entered. Please re-enter : ").split()
    print()

    for length in len_list:
        contents = generate_contents(length,width)
        write_cir(contents)
        call(f"ngspice {cir_filename} > {log_file}",shell=True) 
        
        params = prepare_for_post_proc(width)

        plot_figures(params,length,plot_list)
        
    plt.show()