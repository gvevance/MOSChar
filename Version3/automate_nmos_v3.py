# This program is designed to help the IC designer to choose 
# transistor sizes upon inputting the required device parameters 
# (mainly small signal parameters). Will probably involve some 
# efficient DSA search algorithm and some efficient file handling.

from subprocess import call

vmin_tolerance = 0.05  #! cannot give voltage as 0. So min tolerance

cir_filename = 'temp_nmos_v2.cir'
value_file = 'values_nmos_v2.txt'
model_file = '130nm_bulk.pm'

def define_constraints():
    ''' define the constraints to search for. Writes to a file for the program to read from. '''
    pass
    
def generate_contents(len,vgs_min,vgs_max):
    
    if vgs_min == 0 :
        vgs_min += vmin_tolerance

def write_cir(contents):
    with open(cir_filename,'w') as file :
        file.write(contents)

def op_search():
    pass

def main():

    print("\nSearch for the right bias point for transistors.\n")
    vgs_min , vgs_max = str(input("Enter VGS range (in volts) : ")).split()
    len = str(input("Enter length values ( in um ) : "))

    define_constraints()  # does not need any input or output. Writes to a file.
    contents = generate_contents(len,vgs_min,vgs_max)
    write_cir(contents)
    call(['ngspice',cir_filename])

    op_search()  # does not need any input. Uses the sim results and constraits file 


if __name__=="__main__":
    main()
