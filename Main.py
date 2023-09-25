from connector import *
from getTemplate import get_tests_info
from provsionLabels import deploy_template


#Variables & Constants#####
OAUTH = ""
FILE_PATH = ""
HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + OAUTH}
###########################

if __name__ == "__main__":

    print("Hi, select the action you want to perform:\n1. Get template\n2. Bulk labels\n7. Quit")

    while True:
        function_input = input("Enter the function number (1, 2 or 7): ")

        if function_input.isdigit():
            function_number = int(function_input)
            
            if function_number == 1:
                print("You selected 'Get template'")
                get_tests_info(headers=HEADERS) #aquí es donde se tendría que hacer un for para todas las cuentas de PWC o ya dentro del get template
                break
            elif function_number == 2:
                print("You selected 'Bulk labels'")
                deploy_template(file_path=FILE_PATH, headers=HEADERS)
                break

            elif function_number == 7:

                print("\n\tGood Bye")
                break

            else:
                print("Invalid function number. Please enter 1 or 2.")

