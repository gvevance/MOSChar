import numpy as np
import matplotlib.pyplot as plt

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


def plot_from_data_dict(params,length,plot_list):

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


def show_plots() :
    plt.show()