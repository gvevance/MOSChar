''' demo programs '''

def start_demo() :
    
    print("\n****** Demo ****** \n")
    print("1. MOS device characterisation \n2. Search for operating point staisfying constraints \n3. Exit")
    choice = input("\nEnter option : ")

    if choice == '1' :
        print("\n1. Diode connected NMOS \n2. Diode connected PMOS \n\
3. NMOS with fixed Id with width sweep \n4. PMOS with fixed Id with width sweep \n5. Exit ")
        choice2 = input("\nEnter choice : ")

        if choice2 == '1' :
            pass

        elif choice2 == '2' :
            pass

        elif choice2 == '3' :
            pass
    
        elif choice2 == '4' :
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
            pass

        elif choice2 == '2' :
            pass

        elif choice2 == '3' :
            pass
    
        elif choice2 == '4' :
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

