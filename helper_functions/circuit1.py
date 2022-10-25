import numpy as np
import matplotlib.pyplot as plt

def generate_netlist(MODEL_FILE,SAVEDATA_FILE,length,width):
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


def extract_data(SAVEDATA_FILE,width) :
    
    width_c = float(width) * 1e-6

    with open(SAVEDATA_FILE) as txtfile :
        temp = np.genfromtxt(txtfile, dtype=float)

    data_dict = {}

    data_dict["vgs"]    = temp[1:,0]
    data_dict["id"]     = temp[1:,1]
    data_dict["vdsat"]  = temp[1:,2]
    data_dict["cgs"]    = -temp[1:,3]
    data_dict["cgg"]    = temp[1:,4]
    data_dict["gm"]     = temp[1:,5]
    data_dict["gds"]    = temp[1:,6]
    data_dict["gmbs"]   = temp[1:,7]
    data_dict["vth"]    = temp[1:,8]

    # custom definitions

    data_dict["gm_by_id"]   = data_dict["gm"]/data_dict["id"] 
    data_dict["gain"]       = data_dict["gm"]/data_dict["gds"]
    data_dict["ft"]         = data_dict["gm"]/data_dict["cgg"]
    data_dict["gm_by_gmbs"] = data_dict["gm"]/data_dict["gmbs"]

    # /width quantities

    data_dict["id_wid"]     = data_dict["id"]/width_c
    data_dict["gm_wid"]     = data_dict["gm"]/width_c
    data_dict["gds_wid"]    = data_dict["gds"]/width_c
    data_dict["cgg_wid"]    = data_dict["cgg"]/width_c
    data_dict["cgs_wid"]    = data_dict["cgs"]/width_c
    data_dict["gmbs_wid"]   = data_dict["gmbs"]/width_c

    return data_dict


def define_search_conditions(SEARCH_DEFINE_FILE) :
    ''' Define the constraints to search for after user-input. Writes to a file for the program to read from. 
        Range is to be entered carefully. If you want gm/W > 10, enter the range as "10 10000",
        i.e., 10 and a very large number. '''
    
    search_active = False

    print("\nWhat parameters do you have constraints on ? Enter appropriate code ...\n")
    print("\"gm_wid\" - gm/W \n\"gds_wid\" - gds/W \n\"gain\" - gm/gds \n\"ft\" - ft ")
    
    # clear already existing lines in constraints.txt (create it if it doesn' exist)
    c_file = open(SEARCH_DEFINE_FILE,'w+')
    c_file.close()

    c_file = open(SEARCH_DEFINE_FILE,'a') 

    while(True):
        ret = input("\nEnter option : ").strip()
            
        if (ret == "gm_wid") :
            while (True) :
                break_ = False
                try :
                    gm_wid_min , gm_wid_max = input("Enter gm/W range (<min> <max>) : ").split()
                    
                    try :
                        if float(gm_wid_min) < float(gm_wid_max) :
                            break_ = True

                    except ValueError :
                        print("Improper values entered. ",end="")

                except ValueError:
                    print("Enter values in the right format. ",end="")

                if break_ :
                    c_file.write("gm/W "+gm_wid_min+" "+gm_wid_max+"\n")
                    search_active = True
                    break 

        elif (ret == "gds_wid"):
            while (True) :
                break_ = False
                try :
                    gds_wid_min , gds_wid_max = input("Enter gds/W range : ").split()

                    try :
                        if float(gds_wid_min) < float(gds_wid_max) :
                            break_ = True

                    except ValueError :
                        print("Improper values entered. ",end="")

                except ValueError:
                    print("Enter values in the right format. ",end="")

                if break_ :
                    c_file.write("gds/W "+gds_wid_min+" "+gds_wid_max+"\n")
                    search_active = True
                    break
                
        elif (ret == "gain"):
            while (True) :
                break_ = False
                try :
                    gain_min , gain_max = input("Enter gain range : ").split()

                    try :
                        if float(gain_min) < float(gain_max) :
                            break_ = True

                    except ValueError :
                        print("Improper values entered. ",end="")

                except ValueError:
                    print("Enter values in the right format. ",end="")

                if break_ :
                    c_file.write("gain "+gain_min+" "+gain_max+"\n")
                    search_active = True
                    break

        elif (ret == "ft"):
            while (True) :
                break_ = False
                try :
                    ft_min , ft_max = input("Enter ft range : ").split()
                    try :
                        if float(ft_min) < float(ft_max) :
                            break_ = True
                    
                    except ValueError :
                        print("Improper values entered. ",end="")

                except ValueError:
                    print("Enter values in the right format. ",end="")

                if break_ :
                    c_file.write("ft "+ft_min+" "+ft_max+"\n")
                    search_active = True
                    break
                
        else :
            c_file.close()
            break
    
    return search_active


def opsearch(data_dict,SEARCH_DEFINE_FILE) :
    
    vgs = data_dict["vgs"]
    gm_by_id = data_dict["gm_by_id"]
    id_wid = data_dict["id_wid"]
    vdsat = data_dict["vdsat"]
    cgs_wid = data_dict["cgs_wid"]
    cgg_wid = data_dict["cgg_wid"]
    gm_wid = data_dict["gm_wid"]
    gds_wid = data_dict["gds_wid"]
    vth = data_dict["vth"]
    gain = data_dict["gain"]
    ft = data_dict["ft"]
    gmbs_wid = data_dict["gmbs_wid"]
    gm_by_gmbs = data_dict["gm_by_gmbs"]
    
    # print(vgs[(gm_wid <50) & (gm_wid > 30)])

    # initial condition values
    gm_wid_min , gds_wid_min , gain_min , ft_min = 0,0,0,0
    gm_wid_max , gds_wid_max , gain_max , ft_max = 1e16,1e16,1e16,1e16 
    
    # parse constraints text file
    with open(SEARCH_DEFINE_FILE) as c_file :
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
    
    # print(type(bool_vec))
    return bool_vec


def plot_from_data_dict(data_dict,search_active,search_result_bool_vec,length,plot_list):

    vgs = data_dict["vgs"]
    gm_by_id = data_dict["gm_by_id"]
    id_wid = data_dict["id_wid"]
    vdsat = data_dict["vdsat"]
    cgs_wid = data_dict["cgs_wid"]
    cgg_wid = data_dict["cgg_wid"]
    gm_wid = data_dict["gm_wid"]
    gds_wid = data_dict["gds_wid"]
    vth = data_dict["vth"]
    gain = data_dict["gain"]
    ft = data_dict["ft"]
    gmbs_wid = data_dict["gmbs_wid"]
    gm_by_gmbs = data_dict["gm_by_gmbs"]

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

        if search_active :
            plt.plot(vgs[search_result_bool_vec],gm_by_id[search_result_bool_vec],'g*')

    if "id/w" in plot_list:
        plt.figure(2) # log10(id/W) vs gm/Id
        plt.ylabel("Id/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of Id/W vs gm/Id")
            plt.plot( gm_by_id , id_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],id_wid[search_result_bool_vec],'g*')

        else :
            plt.xlabel("vgs")
            plt.title("Plot of Id/W vs vgs")
            plt.plot( vgs , id_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],id_wid[search_result_bool_vec],'g*')

    if "gm/w" in plot_list:
        plt.figure(3) # log10(gm/W) vs gm/Id
        plt.ylabel("gm/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gm/W vs gm/Id")
            plt.plot( gm_by_id , gm_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],gm_wid[search_result_bool_vec],'g*')

        else :
            plt.xlabel("vgs")
            plt.title("Plot of gm/W vs vgs")
            plt.plot( vgs , gm_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],gm_wid[search_result_bool_vec],'g*')


    if "gds/w" in plot_list:
        plt.figure(4) # log10(gds/W) vs gm/Id
        plt.ylabel("gds/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gds/W vs gm/Id")
            plt.plot( gm_by_id , gds_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],gds_wid[search_result_bool_vec],'g*')

        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of gds/W vs vgs")
            plt.plot( vgs , gds_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],gds_wid[search_result_bool_vec],'g*')
    
    if "gain" in plot_list:
        plt.figure(5) # log10(gain/W) vs gm/Id
        plt.ylabel("gain")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gain vs gm/Id")
            plt.plot( gm_by_id , gain , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],gain[search_result_bool_vec],'g*')

        else :
            plt.xlabel("vgs")
            plt.title("Plot of gain vs vgs")
            plt.plot( vgs , gain , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],gain[search_result_bool_vec],'g*')
    
    if "cgg/w" in plot_list:
        plt.figure(6) # log10(cgg/W) vs gm/Id
        plt.ylabel("cgg/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of cgg/W vs gm/Id")
            plt.plot( gm_by_id , cgg_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],cgg_wid[search_result_bool_vec],'g*')
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of cgg/W vs vgs")
            plt.plot( vgs , cgg_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],cgg_wid[search_result_bool_vec],'g*')

    if "cgs/w" in plot_list:
        plt.figure(7) # log10(cgs/W) vs gm/Id
        plt.ylabel("cgs/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of cgs/W vs gm/Id")
            plt.plot( gm_by_id , cgs_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],cgs_wid[search_result_bool_vec],'g*')
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of cgs/W vs vgs")
            plt.plot( vgs , cgs_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],cgs_wid[search_result_bool_vec],'g*')

    if "ft" in plot_list:
        plt.figure(8) # log10(ft) vs gm/Id
        plt.ylabel("ft")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of ft vs gm/Id")
            plt.plot( gm_by_id , ft , label='Len = '+length+'u' )
            plt.legend()
        
            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],ft[search_result_bool_vec],'g*')
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of ft vs vgs")
            plt.plot( vgs , ft , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],ft[search_result_bool_vec],'g*')
    
    if "vdsat" in plot_list:
        plt.figure(9) # vdsat vs gm/Id
        plt.ylabel("vdsat")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of vdsat vs gm/Id")
            plt.plot( gm_by_id , vdsat , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],vdsat[search_result_bool_vec],'g*')
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of vdsat vs vgs")
            plt.plot( vgs , vdsat , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],vdsat[search_result_bool_vec],'g*')

    if "vth" in plot_list:
        plt.figure(10) # vth vs gm/Id
        plt.ylabel("vth")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of vth vs gm/Id")
            plt.plot( gm_by_id , vth , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],vth[search_result_bool_vec],'g*')
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of vth vs vgs")
            plt.plot( vgs , vth , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],vth[search_result_bool_vec],'g*')

    if "gmbs/w" in plot_list:
        plt.figure(11) # log10(gmbs/W) vs gm/Id
        plt.ylabel("gmbs/W")
        plt.grid(True)
        
        if x == '1' :
            plt.xlabel("gm/Id")
            plt.title("Plot of gmbs/W vs gm/Id")
            plt.plot( gm_by_id , gmbs_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],gmbs_wid[search_result_bool_vec],'g*')
        
        else :
            plt.xlabel("vgs")
            plt.title("Plot of gmbs/W vs vgs")
            plt.plot( vgs , gmbs_wid , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],gmbs_wid[search_result_bool_vec],'g*')

    if "gm/gmbs" in plot_list:
        plt.figure(12) # log10(gm/gmbs) vs gm/Id
        plt.ylabel("gm/gmbs")
        plt.grid(True)
        
        if x == '1' :
        
            plt.xlabel("gm/Id")
            plt.title("Plot of gm/gmbs vs gm/Id")
            plt.plot( gm_by_id , gm_by_gmbs , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(gm_by_id[search_result_bool_vec],gm_by_gmbs[search_result_bool_vec],'g*')

        else :
            plt.xlabel("vgs")
            plt.title("Plot of gm/gmbs vs vgs")
            plt.plot( vgs , gm_by_gmbs , label='Len = '+length+'u' )
            plt.legend()

            if search_active :
                plt.plot(vgs[search_result_bool_vec],gm_by_gmbs[search_result_bool_vec],'g*')


def show_plots() :
    plt.show()