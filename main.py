'''
main.py
Program starts from here.  '''

from Demo.start_demo import start_demo

def main():
    print("\n****** MOSChar project ******\n")
    print("1. Demo \n2. Exit \n")
    choice = input("Enter option : ")

    if choice == '1' :
        start_demo()

    elif choice == '2' :
        exit()

    else :
        print("Wrong option entered. Aborting ... ")
        exit()

if __name__ == "__main__" :
    main()