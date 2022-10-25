'''
main.py
Program starts from here.  '''

from subprocess import call
import os
# import numpy as np
# import matplotlib.pyplot as plt

# from Demo.nmos_plotparams import nmos_plot_demo_1
from Demo.pmos_plotparams import pmos_plot_demo_1
from Demo.nmos_plotparams2 import nmos_plot_demo_2
from Demo.pmos_plotparams2 import pmos_plot_demo_2

from helper_functions.general import init_setup
from helper_functions.general import write_netlist_to_file

import helper_functions.circuit1 as ckt1
import helper_functions.circuit2 as ckt2
import helper_functions.circuit3 as ckt3
import helper_functions.circuit4 as ckt4

# from Demo.nmos_opsearch import nmos_opsearch_demo_1
# from Demo.pmos_opsearch import pmos_opsearch_demo_1
# from Demo.nmos_opsearch2 import nmos_opsearch_demo_2
# from Demo.pmos_opsearch2 import pmos_opsearch_demo_2


def start_menu() :

    CWD, MODEL_DIR, MODEL_FILE, TMP_DIR, NETLIST_FILE, LOG_FILE, SAVEDATA_FILE, SEARCH_DEFINE_FILE = init_setup()
    print(CWD,MODEL_DIR,MODEL_FILE,TMP_DIR,NETLIST_FILE,LOG_FILE,SAVEDATA_FILE)

    print("\n1. Diode connected NMOS, fixed width and VGS sweep \n2. Diode connected NMOS, fixed Id and width sweep \n\
3. Diode connected PMOS, fixed width and VSG sweep \n4. Diode connected PMOS ,fixed Id and width sweep ")
    circuit = input("\nEnter circuit configuration to simulate : ")

    if circuit == '1' :

        print("\n****** Diode connected NMOS ******\n")
        print("Minimum length in the 130nm_bulk.pm technology is 0.13u. Minimum width is probably some 200n\n")

        lmin = 0.13
        wmin = 0.2

        width = str(input(f"Enter width (in um > {wmin}) : "))
        
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

        print("\nEnter ( space-separated ) : gm/id, vdsat, gm/w, gds/w, id/w, cgs/w, cgg/w, vth, gain, ft, gmbs/w, gm/gmbs \n")
        plot_superlist = ["gm/id", "vdsat", "gm/w", "gds/w", "id/w", "cgs/w", "cgg/w", "vth", "gain", "ft", "gmbs/w", "gm/gmbs"]
        plot_list = input("Enter quantities you want to plot using appropriate codes : ").split()

        while ((set(plot_list).issubset(set(plot_superlist)) == False ) or (len(plot_list) == 0)):
            plot_list = input("Incorrect code entered. Please re-enter : ").split()
        print()

        initial_search = False
        for length in len_list:
            netlist = ckt1.generate_netlist(MODEL_FILE,SAVEDATA_FILE,length,width)
            write_netlist_to_file(TMP_DIR,NETLIST_FILE,netlist)
            call(f"ngspice {NETLIST_FILE} > {LOG_FILE}",shell=True) 
            
            # post processing
            data_dict = ckt1.extract_data(SAVEDATA_FILE,width)
            
            # search for operating point
            if not initial_search :
                search_active = ckt1.define_search_conditions(SEARCH_DEFINE_FILE)     # define search condtions
                initial_search = True
            
            if search_active :
                search_result_bool_vec = ckt1.opsearch(data_dict,SEARCH_DEFINE_FILE)
            else :
                search_result_bool_vec = False

            # plotting
            ckt1.plot_from_data_dict(data_dict,search_active,search_result_bool_vec,length,plot_list)
            
        ckt1.show_plots()


    elif circuit == '2' :
        nmos_plot_demo_2()

    elif circuit == '3' :
        pmos_plot_demo_1()

    elif circuit == '4' :
        pmos_plot_demo_2()
        pass

    else :
        print("Entered incorrect option. Exiting ... ")
        exit()


def main():
    opening_message = "\n****** MOSChar project ******"
    print(opening_message)
    
    start_menu()

if __name__ == "__main__" :
    main()