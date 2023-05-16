#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/07/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import os
from cfdi_sorter    import cfdi_sorter
from xlsx_report    import xlsx_general_report
from pdf_report     import generate_pdf
from cfdi_to_xlsx   import dict_to_xlsx

# Function to clear the console screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_type_report(rfc):

    options = {'1': 'AYUDAS', '2': 'INGRESO', '3': 'NOMINA',
               '4': 'PAGO_E', '5': 'DES_BON_DEV', '6': 'GASTO', '7': 'PAGO_R'}

    while True:
        clear()
        print("Menu [3] Select a type report:")
        print('Select an option:')
        print('1. report in excel for receipt type help')
        print('2. report in excel for receipt type income')
        print('3. report in excel for receipt type payroll')
        print('4. report in excel for receipt type issuer/pay')
        print('5. report in excel for receipt type discounts bonuses returns')
        print('6. report in excel for receipt type expense')
        print('7. report in excel for receipt type receiver/pay')
        print('8. report in excel to receive all types')
        print('9. Return to previous menu')

        opcion = input("\nSelect an option: ")

        if options.get(opcion):
            dict_to_xlsx(f'{options.get(opcion)}', rfc)
            input("Press Enter to return to the main menu...")
        elif opcion == '8':
            xlsx_general_report(rfc)
            input("Press Enter to return to the main menu...")
        elif opcion == '9':
            #
            input("Press Enter to return to the main menu...")
            break
        else:
            input('Invalid option. Press Enter to try again...')

# Function to display the municipalities menu
def select_municipality():
    while True:
        clear()
        print("Menu [1] Select a municipality:")
        print("1. MAP: MAP850101324")
        print("2. MCM: MCM8501012U0")
        print("3. MHS: MHS850101F67")
        print("4. MOP: MOP850101NX1")
        print("5. MTR: MTR93032155L8")
        print("0. Exit")
        opcion = input("\nSelect an option: ")
        if   opcion == '1':
            select_algorithm('MAP850101324')
        elif opcion == '2':
            select_algorithm('MCM8501012U0')
        elif opcion == '3':
            select_algorithm('MHS850101F67')
        elif opcion == '4':
            select_algorithm('MOP850101NX1')
        elif opcion == '5':
            select_algorithm('MTR9302155L8')
        elif opcion == '0':
            break
        else:
            input('Invalid option. Press Enter to try again...')

# Function to show algorithms menu
def select_algorithm(rfc):
    while True:
        clear()
        print(f"{rfc} Menu [2] Select:")
        print("1. Sort the xml by type of receipt and methot of payment")
        print("2. Create report Excel (xlsx)")
        print("3. Create files pdf (xml to pdf)")
        print("4. Return to previous menu")

        opcion = input("\nSelect an option: ")

        if opcion == '1':
            print(f"{rfc} : Sort the xml by type of receipt and methot of payment in progress")
            cfdi_sorter(rfc, f'Clientes/{rfc[0:3]}/')
            input("Press Enter to return to the main menu...")
            break
        elif opcion == '2':
            print(f"{rfc}: Create report Excel (xlsx)")
            select_type_report(rfc)
            break
        elif opcion == '3':
            print(f"{rfc} Create files pdf (xml to pdf)")
            generate_pdf(rfc)
            input("Press Enter to return to the main menu...")
            break
        elif opcion == '4':
            break
        else:
            input('Invalid option. Press Enter to try again...')

# Main script code
if __name__ == '__main__':
    # Code that is executed when the script is called directly
    select_municipality()
    pass
