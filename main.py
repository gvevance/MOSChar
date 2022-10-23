'''
main.py
Program starts from here.  '''

from Demo.nmos_plotparams import nmos_plot_demo_1
from Demo.pmos_plotparams import pmos_plot_demo_1
from Demo.nmos_plotparams2 import nmos_plot_demo_2
from Demo.pmos_plotparams2 import pmos_plot_demo_2
from Demo.nmos_opsearch import nmos_opsearch_demo_1
from Demo.pmos_opsearch import pmos_opsearch_demo_1
from Demo.nmos_opsearch2 import nmos_opsearch_demo_2
from Demo.pmos_opsearch2 import pmos_opsearch_demo_2

def start_menu() :

    print("1. MOS device characterisation \n2. Search for operating point staisfying constraints \n3. Exit")
    choice = input("\nEnter option : ")

    if choice == '1' :
        print("\n1. Diode connected NMOS \n2. Diode connected PMOS \n\
3. NMOS with fixed Id with width sweep \n4. PMOS with fixed Id with width sweep \n5. Exit ")
        choice2 = input("\nEnter choice : ")

        if choice2 == '1' :
            nmos_plot_demo_1()

        elif choice2 == '2' :
            pmos_plot_demo_1()

        elif choice2 == '3' :
            nmos_plot_demo_2()
    
        elif choice2 == '4' :
            pmos_plot_demo_2()
            pass

        elif choice2 == '5' :
            exit()

        else :
            print("Wrong option entered. Aborting ... ")
            exit()

    elif choice == '2' :
        print("\n1. Diode connected NMOS \n2. Diode connected PMOS \n\
3. NMOS with fixed Id with width sweep \n4. PMOS with fixed Id with width sweep \n5. Exit ")
        choice2 = input("\nEnter choice : ")

        if choice2 == '1' :
            nmos_opsearch_demo_1()

        elif choice2 == '2' :
            pmos_opsearch_demo_1()

        elif choice2 == '3' :
            nmos_opsearch_demo_2()
            pass

        elif choice2 == '4' :
            pmos_opsearch_demo_2()
            pass

        elif choice2 == '5' :
            exit()

        else :
            print("Wrong option entered. Aborting ... ")
            exit()

    elif choice == '3' :
        exit()

    else :
        print("Wrong option entered. Aborting ... ")
        exit()


def main():
    opening_message = "\n****** MOSChar project ******\n"
    print(opening_message)
    
    start_menu()

if __name__ == "__main__" :
    main()