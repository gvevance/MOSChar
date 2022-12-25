'''
main.py
Program starts from here.  '''

from subprocess import call
import os
from helper_functions.general import init_setup
from helper_functions.general import write_netlist_to_file
import helper_functions.circuit as ckt


def start_menu() :

    print("\n Diode connected NMOS, fixed width and VGS sweep")    
    CWD, MODEL_DIR, MODEL_FILE, DIR, NETLIST_FILE, LOG_FILE, SAVEDATA_FILE_FORMAT, SEARCH_DEFINE_FILE = init_setup()

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

        SAVEDATA_FILE = SAVEDATA_FILE_FORMAT.split(".txt")[0]+'_W_'+width+'_L_'+length+'.txt'

        regen = 'y'
        if os.path.exists(SAVEDATA_FILE) :
            regen = input(f"Save data exists for the configuration W={width}u L={length}u. Re-simulate ? [y/N] : ")

        if regen in ['y','Y'] :
            netlist = ckt.generate_netlist(MODEL_FILE,SAVEDATA_FILE,length,width)
            write_netlist_to_file(DIR,NETLIST_FILE,netlist)
            call(f"ngspice {NETLIST_FILE} > {LOG_FILE}",shell=True) 
        
        # post processing
        data_dict = ckt.extract_data(SAVEDATA_FILE,width)
        
        # search for operating point
        if not initial_search :
            search_active = ckt.define_search_conditions(SEARCH_DEFINE_FILE)     # define search condtions
            initial_search = True                                                 # don't prompt search for each length
        
        if search_active :
            search_result_bool_vec = ckt.opsearch(data_dict,SEARCH_DEFINE_FILE)
        else :
            search_result_bool_vec = False

        # plotting
        ckt.plot_from_data_dict(data_dict,search_active,search_result_bool_vec,length,plot_list)
        
    ckt.show_plots()


def main():
    opening_message = "\n****** MOSChar project ******"
    print(opening_message)
    
    start_menu()


if __name__ == "__main__" :
    main()