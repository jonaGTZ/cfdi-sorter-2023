# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/24/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import os
import pandas as pd
import json

from lxml               import etree
from datetime           import datetime
from cfdi_row_collector import cfdi_row_collector

def get_dir_path_data(option, rfc):
    dirs = {
        'AYUDAS'        : f'{rfc}/Emisor/Ayudas/',
        'INGRESO'       : f'{rfc}/Emisor/Ingresos/',
        'NOMINA'        : f'{rfc}/Emisor/Nomina/',
        'PAGO_E'        : f'{rfc}/Emisor/Pagos/',
        'DES_BON_DEV'   : f'{rfc}/Receptor/Descuento_Bonificaciones_Devoluciones/',
        'GASTO'         : f'{rfc}/Receptor/Gastos/',
        'PAGO_R'        : f'{rfc}/Receptor/Pagos/'
    }
    return dirs.get(option)

def get_columns_template(option):
    dirs = {
        'AYUDAS'        : 'xlsx_report_template/help-columns.json',
        'INGRESO'       : 'xlsx_report_template/income-columns.json',
        'NOMINA'        : 'xlsx_report_template/payroll-columns.json',
        'PAGO_E'        : 'xlsx_report_template/payment-columns.json',
        'DES_BON_DEV'   : 'xlsx_report_template/dis-reb-ref-columns.json',
        'GASTO'         : 'xlsx_report_template/expense-columns.json',
        'PAGO_R'        : 'xlsx_report_template/payment-columns.json'
    }
    return dirs.get(option)

def cfdi_to_dict(option, rfc):

    # Define the path of cfdi's dir 
    dirpath     = get_dir_path_data(option, rfc)
    filas       = []
    
    try:
        # Iterate over all XML files in the specified path
        for dir, subdir, files in os.walk(dirpath):
            for file in files:
                if file.endswith(".xml"):
                    # Get the full path of the XML file
                    filename = os.path.join(dir, file)
                
                    # Parse the XML file with lxml
                    try: 
                        arbol = etree.parse(filename)
                    except:
                        raise Exception(f'E1: Impossible to parse the tree: {filename}')
                    
                    # Create a columns for the current file
                    try:
                        with open(get_columns_template(option), encoding='utf-8') as f:
                            fila = json.load(f)
                            for nodo in arbol.iter():
                                try:
                                    fila = cfdi_row_collector(nodo, fila, option, rfc)
                                except:
                                    raise Exception(f'E2: an error occurred filling the dictionary {filename}')
                    except:
                        raise Exception(f'E3: Impossible to get xlsx columns: {filename}')
                    
                    # Get all attribute values for each node in the file
                    fila['Archivo XML'] = filename

                    # Add the row to the list of rows
                    filas.append(fila)
                # break #
        return filas, dirpath
    
    except:
        raise Exception(f'E4: Impossible to get xlsx columns: {filename}')

def dict_to_xlsx(option, rfc):
    try:
        # calls the cfdi_to_dict function that returns the address where to save the xlsx and the array of the cfdi data
        filas, dirpath = cfdi_to_dict(option, rfc)
        
        # Create a DataFrame from the list of rows
        df = pd.concat([pd.DataFrame(fila, index=[0]) for fila in filas], ignore_index=True)

        # Create a ExcelWriter object
        writer = pd.ExcelWriter(f"{dirpath}/{option}-{datetime.now().strftime('%m%d%Y-%H%M%S')}.xlsx", engine='xlsxwriter')

        # Define the formatting for the header row
        header_format = writer.book.add_format({'bold': True, 'bg_color': '#730707', 'font_color': 'white'})

        # Convert the DataFrame to an Excel sheet
        df.to_excel(writer, sheet_name=f'{option}', index=False, float_format='%.2f')
        
        worksheet = writer.sheets[f'{option}']

        # Format the header row
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Save the Excel file
        writer.close()

        # # after using the status dictionary it is removed
        # template_status_path = f'{rfc}/status/{option}.json'
        # if os.path.exists(template_status_path):
        #     os.remove(template_status_path)
        #     print("SAT state dictionary cleared successfully")

    except Exception as e:
        print (e)
        pass
