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
from openpyxl.styles    import Alignment
from openpyxl           import load_workbook, Workbook
from openpyxl.styles    import Color, Font, PatternFill

# Define the ElementPath queries
version_query               = 'Version'

def filenames(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".xml"):
                yield os.path.join(root, file)

def rename_xlsx_headers(path):
    wb = load_workbook(path)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    count = {}

    for i, header in enumerate(headers):
        if header in count:
            count[header] += 1
            headers[i] = f"{header} receptor"
        else:
            count[header] = 0

    for col_num, name in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=name)
    wb.save(path)
    print('xlsx modified successfully')

def get_cfdi_version(version):
    if   version == '4.0':
        emisor_query    = '{http://www.sat.gob.mx/cfd/4}Emisor'
        receptor_query  = '{http://www.sat.gob.mx/cfd/4}Receptor'
    elif version == '3.3':
        emisor_query    = '{http://www.sat.gob.mx/cfd/3}Emisor'
        receptor_query  = '{http://www.sat.gob.mx/cfd/3}Receptor'

    return emisor_query, receptor_query

def create_xlsx(rfc, option):
    try:
        # Use set() method to save attribute names reduces the amount of memory needed
        url_cfdi40  = 'http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd'
        url_cfdi33  = 'http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd'
        cfdi40      = set()
        cfdi33      = set()

        # Reads both CFDI standards and extracts the attribute names from each CFDI version. 
        # These names are stored in two separate lists
        with urllib.request.urlopen(url_cfdi40) as response:
            tree = ET.parse(response)
            root = tree.getroot()

            for nodo in root.iter():
                if 'name' in nodo.attrib:
                    cfdi40.add(nodo.attrib['name'])

        with urllib.request.urlopen(url_cfdi33) as response:
            tree = ET.parse(response)
            root = tree.getroot()

            for nodo in root.iter():
                if 'name' in nodo.attrib:
                    cfdi33.add(nodo.attrib['name'])
                    
        # Combine the two lists of attribute names, removing any duplicates, and store the results in a new list
        attr_list = list(cfdi40 | cfdi33)

        # Gets the current date and time
        fecha_actual = datetime.now().strftime('%m%d%Y-%H%M%S')

        # In the rfc folder and its corresponding subfolder, using the name of the previously created file.
        try:
            os.makedirs(os.path.join(rfc, option))
            filename = f"{option}{fecha_actual}.xlsx"
            xlsx_path = os.path.join(rfc, option, filename)
        except FileExistsError:
            pass

        # Create an Excel file and format the header
        wb = Workbook()
        ws = wb.active
        ws.title = f"comprobante_{fecha_actual}"
        header_font = Font(color='FFFFFF')
        header_fill = PatternFill(start_color='730707', end_color='730707', fill_type='solid')

        # Write the names of the attributes of the digital tax receipts in the first row of the Excel sheet
        for col_num, name in enumerate(attr_list, 1):
            # Adding suffixes to indicate which CFDI version each attribute belongs to
            if name in cfdi40 and name not in cfdi33:
                name += '_V4'
            elif name in cfdi33 and name not in cfdi40:
                name += '_V3.3'

            cell = ws.cell(row=1, column=col_num, value=name)
            cell.font = header_font
            cell.fill = header_fill
        # Save workbook
        wb.save(xlsx_path)
        return xlsx_path

    except Exception as e:
        print(f"Error: {e}")

def cfdi_to_xlsx(rfc, option, dir):

    try:
        # 
        path = create_xlsx(rfc, option)
        rename_xlsx_headers(path)
        # 
        wb      = load_workbook(path)
        ws      = wb.active
        headers = [cell.value for cell in ws[1]]
        
    except Exception as e:
        print(f"Error: {e}")

    for filename in filenames(dir):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            # Get the cfdi version
            version                       = root.get(version_query)
            emisor_query, receptor_query  = get_cfdi_version(version)

            emisor      = root.find(emisor_query)
            receptor    = root.find(receptor_query)

        except ET.ParseError:
            print(f"{filename} could not be parsed.")
        except Exception as e:
            print(f"{filename} could not be processed due to an error: {e}.")
    

