#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/07/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import os
import urllib.request
import xml.etree.ElementTree as ET

from datetime           import datetime
from openpyxl           import load_workbook, Workbook
from openpyxl.styles    import Font, PatternFill

# Define the ElementPath queries
version_query = 'Version'

# Gets the current date and time
fecha_actual  = datetime.now().strftime('%m%d%Y-%H%M%S')

def get_dir_path_data(option):
    dirs = {
        'AYUDAS'        : '/Emisor/Ayudas/',
        'INGRESO'       : '/Emisor/Ingresos/',
        'GASTOE'        : '/Emisor/Gastos/',
        'NOMINA'        : '/Emisor/Nomina/',
        'DES_BON_DEV'   : '/Receptor/Descuento_Bonificaciones_Devoluciones/',
        'GASTOR'        : '/Receptor/Gastos/',
        'PAGOS'         : '/Receptor/Pagos/'
    }
    return dirs.get(option)

def filenames(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".xml"):
                yield os.path.join(root, file)

def rename_xlsx_headers(path):
    # Load workbook and get active worksheet and headers from first row
    wb = load_workbook(path)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    
    # Count the occurrences of each header and rename if necessary
    count = {}
    for i, header in enumerate(headers):
        if header in count:
            count[header] += 1
            headers[i] = f"{header} receptor"
        else:
            count[header] = 0

    # Write modified headers back to worksheet
    for col_num, name in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=name)

    # Save modified workbook and print success message
    wb.save(path)
    print(f'{path}: xlsx namespaces modified successfully')

def get_cfdi_version(version):
    if version == '4.0':
        emisor_query    = '{http://www.sat.gob.mx/cfd/4}Emisor'
        receptor_query  = '{http://www.sat.gob.mx/cfd/4}Receptor'
    elif version == '3.3':
        emisor_query    = '{http://www.sat.gob.mx/cfd/3}Emisor'
        receptor_query  = '{http://www.sat.gob.mx/cfd/3}Receptor'
    return emisor_query, receptor_query

def del_empty_columns(path):
    # Load the workbook
    wb = load_workbook(path)
    ws = wb.active

    # Find the maximum number of rows and columns
    max_row = ws.max_row
    max_col = ws.max_column

    # Loop through each column
    for col in range(1, max_col + 1):
        # Check if all cells in column are empty starting from row 2
        empty = True
        for row in range(2, max_row + 1):
            if ws.cell(row=row, column=col).value != None and ws.cell(row=row, column=col).value != "":
                empty = False
                break

        # If all cells are empty, delete the column
        if empty:
            ws.delete_cols(col, 1)
    # Save the workbook
    wb.save(path)
    print(f'{path} xlsx deleted columns successfully.')

def create_xlsx(rfc, option):
    try:
        # Use set() method to save attribute names reduces the amount of memory needed
        url_cfdi40 = 'http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd'
        url_cfdi33 = 'http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd'
        cfdi40     = []
        cfdi33     = []

        # Reads both CFDI standards and extracts the attribute names from each CFDI version.
        # These names are stored in two separate lists
        with urllib.request.urlopen(url_cfdi40) as response:
            tree = ET.parse(response)
            root = tree.getroot()

            for nodo in root.iter():
                if 'name' in nodo.attrib:
                    cfdi40.append(nodo.attrib['name'])

        with urllib.request.urlopen(url_cfdi33) as response:
            tree = ET.parse(response)
            root = tree.getroot()

            for nodo in root.iter():
                if 'name' in nodo.attrib:
                    cfdi33.append(nodo.attrib['name'])

        # filter attributes only present in 4.0
        attr_40_list = [attr for attr in cfdi40 if attr not in cfdi33]

        # In the rfc folder and its corresponding subfolder, using the name of the previously created file.
        try:
            os.makedirs(os.path.join(rfc, 'xlsx_report', option))
        except FileExistsError:
            pass

        filename        = f"{option}-{fecha_actual}.xlsx"
        xlsx_path       = os.path.join(rfc, 'xlsx_report', option, filename)

        # Create an Excel file and format the header
        wb              = Workbook()
        ws              = wb.active
        ws.title        = f"{option}-{fecha_actual}"
        header_font     = Font(color='FFFFFF')
        header_fill     = PatternFill(
        start_color     ='730707', end_color='730707', fill_type='solid')

        # write headers for version 3.3
        for col_num, name in enumerate(cfdi33, 1):
            cell        = ws.cell(row=1, column=col_num, value=name)
            cell.font   = header_font
            cell.fill   = header_fill

        # write headers for version 4.0
        for col_num, name in enumerate(attr_40_list, len(cfdi33) + 1):
            cell        = ws.cell(row=1, column=col_num, value=name)
            cell.font   = header_font
            cell.fill   = header_fill

        # Save workbook
        wb.save(xlsx_path)
        print(f'{xlsx_path}: xlsx created successfully')
        return xlsx_path

    except Exception as e:
        print(f"Error: {e}")

def cfdi_to_xlsx(rfc, option):
    # Create Excel file with headers
    path = create_xlsx(rfc, option)
    rename_xlsx_headers(path)

    # Load workbook and get active worksheet
    wb = load_workbook(path)
    ws = wb.active

    # Get headers from worksheet
    headers = [cell.value for cell in ws[1]]
    
    # Process each XML file in directory
    for filename in filenames(f"{rfc}{get_dir_path_data(option)}"):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            # Get the cfdi version
            version     = root.get(version_query)
            emisor_query, receptor_query = get_cfdi_version(version)
            emisor      = root.find(emisor_query)
            receptor    = root.find(receptor_query)

            # Create a dictionary to store row data
            row_data = {}

            # Add other attributes to dictionary
            for nodo in root.iter():
                if nodo.attrib:
                    row_data.update({key: value for key, value in nodo.attrib.items() if key in headers and key not in row_data})

            # Add RFC, Name, and Receiver RFC and Name to dictionary
            if emisor is not None:
                row_data['Rfc']             = str(emisor.get('Rfc'))
                row_data['Nombre']          = str(emisor.get('Nombre'))
            if receptor is not None:
                row_data['Rfc receptor']    = str(receptor.get('Rfc'))
                row_data['Nombre receptor'] = str(receptor.get('Nombre'))

            # Check if row_data has any data before writing to worksheet
            if row_data:
                # Write data to worksheet
                row_num = ws.max_row + 1
                for col_num, header in enumerate(headers, 1):
                    if header in row_data:
                        cell_value = row_data[header]
                        # Check if cell value is a number and convert to float if necessary
                        if isinstance(cell_value, str) and cell_value.isnumeric():
                            cell_value = float(cell_value)

                        # Write cell value to worksheet
                        ws.cell(row=row_num, column=col_num, value=cell_value)

            # saving the values that correspond to each header.
            wb.save(path)
            print(f'{filename} xlsx filled successfully.')
        except ET.ParseError:
            print(f"{filename} could not be parsed.")
        except Exception as e:
            print(f"{filename} could not be processed due to an error: {e}.")

    # Delete empty columns from worksheet
    del_empty_columns(path)

def xlsx_general_report(rfc):

    print('... xlsx in process, please wait.')

    # Set the directory paths
    directories = [
        f'{rfc}/xlsx_report/AYUDAS',
        f'{rfc}/xlsx_report/INGRESO',
        f'{rfc}/xlsx_report/GASTOE',
        f'{rfc}/xlsx_report/NOMINA',
        f'{rfc}/xlsx_report/DES_BON_DEV',
        f'{rfc}/xlsx_report/GASTOR',
        f'{rfc}/xlsx_report/PAGOS'
    ]

    # Initialize empty list to store file paths
    file_paths = []

    # Get the most recent file from each directory
    for directory in directories:
        if os.path.exists(directory):
            # Get the most recent file in the directory
            files = os.listdir(directory)
            if files:
                file_path = max([os.path.join(directory, f) for f in files if f.endswith('.xlsx')], key=os.path.getctime)
                file_paths.append(file_path)
            else:
                print(f"E1: Can't find the route: {directory}")
        else:
            print(f"E2: Doesn't exist: {directory}")

    # Create a new workbook
    nwb = Workbook()

    # Loop through each Excel file and write its contents to a separate sheet
    for file_path in file_paths:
        try:
            # Load workbook, active worksheet, get the sheet name, create a new sheet
            wb = load_workbook(file_path)
            ws = wb.active
            sn = ws.title
            ns = nwb.create_sheet(sn)

            # Copy the data from the old worksheet to the new worksheet
            for row in ws.iter_rows(values_only=True):
                ns.append(row)

            # Change the font color and fill color of the headers
            for cell in ns[1]:
                cell.font = Font(color='FFFFFF')
                cell.fill = PatternFill(
                    start_color='730707', end_color='730707', fill_type='solid')

        except Exception as e:
            print(f'E3: Error while reading book: {e}')
            continue

    # Delete any extra sheets that were created in the new workbook
    while len(nwb.sheetnames) > len(file_paths):
        nwb.remove(nwb.active)

    # Save the new workbook
    try:
        nwb.save(f'{rfc}/reporte-general-{fecha_actual}.xlsx')
    except Exception as e:
        print(f'E4: Error saving the new workbook: {e}')