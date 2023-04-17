#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/07/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import os
from cfdi_sorter import cfdi_sorter
from xlsx_report import cfdi_to_xlsx, xlsx_general_report
from pdf_report  import generate_pdf

# Function to clear the console screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_type_report(rfc):

    options = {'1': 'AYUDAS', '2': 'INGRESO', '3': 'GASTOE',
               '4': 'DES_BON_DEV', '5': 'GASTOR', '6': 'PAGOS', '7': 'NOMINA'}

    while True:
        clear()
        print("Menu [3] Select a type report:")
        print('Select an option:')
        print('1. report in excel for receipt type help')
        print('2. report in excel for receipt type income')
        print('3. report in excel for receipt type issuer/expense')
        print('4. report in excel for receipt type discounts bonuses returns')
        print('5. report in excel for receipt type receiver/expense')
        print('6. report in excel for receipt type pay')
        print('7. report in excel for receipt type payroll')
        print('8. report in excel to receive all types')
        print('9. Return to previous menu')

        opcion = input("\nSelect an option: ")

        if options.get(opcion):
            cfdi_to_xlsx(rfc, options.get(opcion))
        elif opcion == '8':
            xlsx_general_report(rfc)
        elif opcion == '9':
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
        if opcion == '1':
            clear()
            print('Atexcal, Puebla Municipality')
            select_algorithm('MAP850101324')
        elif opcion == '2':
            clear()
            print('Cañada Morelos Municipality')
            select_algorithm('MCM8501012U0')
        elif opcion == '3':
            clear()
            print('Huitzilan de Serdán Municipality')
            select_algorithm('MHS850101F67')
        elif opcion == '4':
            clear()
            print('Ocoyucan Puebla Municipality')
            select_algorithm('MOP850101NX1')
        elif opcion == '5':
            clear()
            print('Tepexi de Rodríguez Municipality')
            select_algorithm('MTR9302155L8')
        elif opcion == '0':
            break
        else:
            input('Invalid option. Press Enter to try again...')

# Function to show algorithms menu
def select_algorithm(rfc):
    while True:
        # clear()
        print(f"{rfc} Menu [2] Select:")
        print("1. Sort the xml by type of receipt and methot of payment")
        print("2. Create report Excel (xlsx)")
        print("3. Create files pdf (xml to pdf)")
        print("4. Return to previous menu")
        opcion = input("\nSelect an option: ")
        if opcion == '1':
            print(f"{rfc} : Sort the xml by type of receipt and methot of payment")
            # cfdi_sorter(rfc, 'Clientes/' + rfc[0:3] + '/')
            """ 
                XML DE PRUEBA 
            """
            cfdi_sorter(rfc, 'xml_new_data')
            input("Press Enter to return to the main menu...")
            break
        elif opcion == '2':
            clear()
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
