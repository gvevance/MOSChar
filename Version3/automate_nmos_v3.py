# This program is designed to help the IC designer to choose 
# transistor sizes upon inputting the required device parameters 
# (mainly small signal parameters). Will probably involve some 
# efficient DSA search algorithm and some efficient file handling.

from subprocess import call

vmin_tolerance = 0.05  #! cannot give voltage as 0. So min tolerance

cir_filename = 'temp_nmos_v3.cir'
value_file = 'values_nmos_v2.txt'
model_file = '130nm_bulk.pm'

def define_constraints():
    ''' Define the constraints to search for after user-input. Writes to a file for the program to read from. 
        Range is to be entered carefully. If you want gm/W > 10, enter the range as "10 10000",
        i.e., 10 and a very large number. '''
    
    print("\nWhat parameters do you have constraints on ? Enter appropriate code (\"0\" when done)...\n")
    print("\"gm_wid\" - gm/W \n\"gds_wid\" - gds/W \n\"gain\" - gm/gds \n\"ft\" - ft \n")
    
    ret = "start"
    while(ret != '0'):
        ret = input("Enter option : ")
        
        if (ret == "gm_wid") :
            gm_wid_min , gm_wid_max = input("Enter gm/W range : ").split()

        elif (ret == "gds_wid"):
            gds_wid_min , gds_wid_max = input("Enter gds/W range : ").split()

        elif (ret == "gain"):
            gain_min , gain_max = input("Enter gain range : ").split()

        elif (ret == "ft"):
            ft_min , ft_max = input("Enter ft range : ").split()

        elif (ret == "0"):
            pass

        else :
            print("Enter valid option. \"0\" if you're done.")
            ret = "invalid code"

    # printing chosen constraints
    
    
def generate_contents(len,vgs_min,vgs_max):
    
    if vgs_min == 0 :
        vgs_min += vmin_tolerance
    
    return '''Dummy script
    .control
    exit
    .endc
    .end'''

def write_cir(contents):
    with open(cir_filename,'w') as file :
        file.write(contents)

def op_search():
    pass

def main():

    print("\nSearch for the right bias point for transistors.\n")
    vgs_min , vgs_max = str(input("Enter VGS range (in volts) : ")).split()
    len = str(input("Enter length ( in um ) : "))

    define_constraints()  # does not need any input or output. Writes to a file.
    contents = generate_contents(len,vgs_min,vgs_max)
    write_cir(contents)
    call(['ngspice',cir_filename])

    op_search()  # does not need any input. Uses the sim results and constraits file 


if __name__=="__main__":
    main()