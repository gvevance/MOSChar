# This program is designed to help the IC designer to choose 
# transistor sizes upon inputting the required device parameters 
# (mainly small signal parameters). Will probably involve some 
# efficient DSA search algorithm and some efficient file handling.

vmin_tolerance = 0.05  #! cannot give voltage as 0. So min tolerance

def main():

    print("\nSearch for th right bias point for transistors.")
    vgs_min , vgs_max = str(input("Enter VGS range (in volts) : ")).split()
    len_list = str(input("Enter length values ( in um ) : ")).split()

if __name__=="__main__":
    main()