# A more functional version of the script with user input. With length sweep.
# Program flow - Enter lengths we want to simulate
# Width is user-input
# Run the code in a for loop and get back the numpy arrays for post-processing

from subprocess import call
import numpy as np
import matplotlib.pyplot as plt

# define constants
 
cir_filename = 'temp_nmos_v2_b.cir'
value_file = 'values_nmos_v2_b.txt'
model_file = '130nm_bulk.pm'

def generate_contents(length,wmin,wmax,i0,vds):
    
    contents = f'''NMOS characterisation

*************************************
* Include model file 
*************************************
.include {model_file}

*************************************
* Defining arameters 
*************************************
.param len = {length}u
.param width = {wmax}u 
.param lmin = 0.13u

*************************************
* Circuit definition
*************************************
vdd 1 0 dc 1.3
i0 2 1 dc {i0}
vds_ref 4 0 dc {vds}
e_amp 3 0 2 4 1e4
M1 2 3 0 0 nmos l={{len}} w={{width}} as={{2*lmin*width}} ad={{2*lmin*width}} ps={{4*lmin+2*width}} pd={{4*lmin+2*width}}


*************************************
* Control section
*************************************

.control 

save @M1[vdsat], @M1[vth], @M1[cgs], @M1[cgg],
+ @M1[gm], @M1[gds], @M1[gmbs], @M1[vsat]

* parameter sweep of width

let wmin = {wmin}u
let wmax = {wmax}u
let delta_w = 5u
let w = wmin

set filetype=ascii
set wr_singlescale
*set wr_vecnames

* loop
while w le wmax
    alter width w
    op
    wrdata {value_file} w, @M1[vdsat], @M1[cgs], @M1[cgg] 
    + @M1[gm], @M1[gds], @M1[gmbs], @M1[vth], @M1[vgs]
    set appendwrite
    let w = w + delta_w
end

* Run the sim
run

*wrdata {value_file} @M1[vdsat], @M1[cgs], @M1[cgg] 
*+ @M1[gm], @M1[gds], @M1[gmbs], @M1[vth], @M1[vgs]

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
    with open(cir_filename,'w') as file :
        file.write(contents)


def prepare_for_post_proc(i0):
    
    with open(value_file) as txtfile :
        temp = np.genfromtxt(txtfile, dtype=float)

    params = {}

    params["width"]    = temp[1:,0]
    params["vdsat"]    = temp[1:,1]
    params["cgs"]      = -temp[1:,2]
    params["cgg"]      = temp[1:,3]
    params["gm"]       = temp[1:,4]
    params["gds"]      = temp[1:,5]
    params["gmbs"]     = temp[1:,6]
    params["vth"]      = temp[1:,7]
    params["vgs"]      = temp[1:,8] 
    params["id"]       = float(i0)*1e-6
    
    # custom definitions

    params["gm_by_id"]   = params["gm"]/params["id"] 
    params["gain"]       = params["gm"]/params["gds"]
    params["ft"]         = params["gm"]/params["cgg"]
    params["gm_by_gmbs"] = params["gm"]/params["gmbs"]

    return params


def plot_figures(params,length,plot_list):

    width = params["width"]
    vgs = params["vgs"]
    gm = params["gm"]
    gmbs = params["gmbs"]
    gds = params["gds"]
    gm_by_id = params["gm_by_id"]
    cgg = params["cgg"]
    cgs = params["cgs"]
    vdsat = params["vdsat"]
    vth = params["vth"]
    gain = params["gain"]
    ft = params["ft"]
    gm_by_gmbs = params["gm_by_gmbs"]

    if "vgs" in plot_list:
        plt.figure(1) # gm/Id vs width
        plt.plot( width , vgs , label='Len = '+length+'u' )
        plt.ylabel("vgs")
        plt.xlabel("width")
        plt.title("Plot of vgs vs width")
        plt.grid(True)
        plt.legend()

    if "gm/id" in plot_list:
        plt.figure(1) # gm/Id vs width
        plt.plot( width , gm_by_id , label='Len = '+length+'u' )
        plt.ylabel("gm/Id")
        plt.xlabel("width")
        plt.title("Plot of gm/Id vs width")
        plt.grid(True)
        plt.legend()

    if "gm" in plot_list:
        plt.figure(3) # log10(gm/W) vs gm/Id
        plt.semilogy( width , gm , label='Len = '+length+'u' )
        plt.ylabel("gm")
        plt.xlabel("width")
        plt.title("Plot of gm vs width")
        plt.grid(True)
        plt.legend()

    if "gds" in plot_list:
        plt.figure(4) # log10(gds) vs width
        plt.semilogy( width , gds , label='Len = '+length+'u' )
        plt.ylabel("gds")
        plt.xlabel("width")
        plt.title("Plot of gds vs width")
        plt.grid(True)
        plt.legend()

    if "gain" in plot_list:
        plt.figure(5) # log10(gain) vs width
        plt.semilogy( width , gain , label='Len = '+length+'u' )
        plt.ylabel("gain")
        plt.xlabel("width")
        plt.title("Plot of gain vs width")
        plt.grid(True)
        plt.legend()

    if "cgg/w" in plot_list:
        plt.figure(6) # log10(cgg) vs width
        plt.semilogy( width, cgg , label='Len = '+length+'u' )
        plt.ylabel("cgg")
        plt.xlabel("width")
        plt.title("Plot of cgg vs width")
        plt.grid(True)
        plt.legend()

    if "cgs/w" in plot_list:
        plt.figure(7) # log10(cgs) vs width
        plt.semilogy( width , cgs , label='Len = '+length+'u' )
        plt.ylabel("cgs")
        plt.xlabel("width")
        plt.title("Plot of cgs vs width")
        plt.grid(True)
        plt.legend()

    if "ft" in plot_list:
        plt.figure(8) # log10(ft) vs width
        plt.semilogy( width , ft , label='Len = '+length+'u' )
        plt.ylabel("ft")
        plt.xlabel("width")
        plt.title("Plot of ft vs width")
        plt.grid(True)
        plt.legend()

    if "vdsat" in plot_list:
        plt.figure(9) # vdsat vs width
        plt.plot( width , vdsat , label='Len = '+length+'u' )
        plt.ylabel("vdsat")
        plt.xlabel("width")
        plt.title("Plot of vdsat vs width")
        plt.grid(True)
        plt.legend()

    if "vth" in plot_list:
        plt.figure(10) # vth vs width
        plt.plot( gm_by_id , vth , label='Len = '+length+'u' )
        plt.ylabel("vth")
        plt.xlabel("width")
        plt.title("Plot of vth vs width")
        plt.grid(True)
        plt.legend()

    if "gmbs/w" in plot_list:
        plt.figure(11) # log10(gmbs/W) vs width
        plt.semilogy( width , gmbs , label='Len = '+length+'u' )
        plt.ylabel("gmbs/W")
        plt.xlabel("width")
        plt.title("Plot of gmbs vs width")
        plt.grid(True)
        plt.legend()

    if "gm/gmbs" in plot_list:
        plt.figure(12) # log10(gm/gmbs) vs width
        plt.plot( width , gm_by_gmbs , label='Len = '+length+'u' )
        plt.ylabel("gm/gmbs")
        plt.xlabel("width")
        plt.title("Plot of gm/gmbs vs width")
        plt.grid(True)
        plt.legend()


def main():
    
    print("\nAutomated gm/id curve extracting ...")
    print("Minimum length in the 130nm_bulk.pm technology is 0.13u. Minimum width is probably some 200n\n")
    
    print("1 - Default mode (view trends)\n2 - Custom mode\n")
    mode = int(input("Enter mode : "))

    if mode == 1 :
        wmin = '10'
        wmax = '100'
        i0 = '100'
        vds = 0.2
        len_list = ['0.3']

        print(f"\nwmin = {wmin}u \nwmax = {wmax}u \nlength = {len_list[0]}")
        print(f"i0 = {i0}uA \nvds = {vds}V \n")


    elif mode == 2 :
        i0 = str(input("\nEnter current (in uA) : "))
        vds = str(input("\nEnter VDS (in V) : "))
        wmin,wmax = str(input("Enter width range (in um) : ")).split()
        len_list = str(input("Enter lengths (in um) (space-separated) : ")).split()
    
    else :
        print("Error. Incorrect mode entered. Exiting ...")
        exit()

    print("\nCodes : gm/id, vdsat, gm, gds, cgs, cgg, vth, gain, ft, gmbs, gm/gmbs \n")
    plot_superlist = ["gm/id", "vdsat", "gm", "gds", "cgs", "cgg", "vth", "gain", "ft", "gmbs", "gm/gmbs"]
    plot_list = input("Enter quantities you want to plot using appropriate codes : ").split()

    while ((set(plot_list).issubset(set(plot_superlist)) == False ) or (len(plot_list) == 0)):
        plot_list = input("Incorrect code entered. Please re-enter : ").split()
    print()

    for length in len_list:
        contents = generate_contents(length,wmin,wmax,i0,vds)
        write_cir(contents)
        call(['ngspice',cir_filename]) 

        params = prepare_for_post_proc(i0)

        plot_figures(params,length,plot_list)
        
    plt.show()

if __name__=="__main__":
    main()