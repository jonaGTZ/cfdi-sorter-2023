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

def modify_headers(path):
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
    print('\nHeaders modified successfully')

def create_xlsx(type_option):
    url = 'http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd'
    response = urllib.request.urlopen(url)

    tree = ET.parse(response)
    root = tree.getroot()

    #get the names of node attributes from an XML file that defines the CFDI 3.3 standard
    name_list = []
    for nodo in root.iter():
        if 'name' in nodo.attrib:
            name_list.append(nodo.attrib['name'])

    # get actual date
    fecha_actual = datetime.now().strftime('%m%d%Y-%H%M%S')

    # create destination paths for each report
    ruta_ayudas     = 'CFDI_RFC_MUNICIPIO/Emisor/Ayudas/'
    ruta_ingreso    = 'CFDI_RFC_MUNICIPIO/Emisor/Ingresos/'
    ruta_nomina     = 'CFDI_RFC_MUNICIPIO/Emisor/Nomina/'
    ruta_desbondev  = 'CFDI_RFC_MUNICIPIO/Receptor/Descuento_Bonificaciones_Devoluciones/'
    ruta_gasto      = 'CFDI_RFC_MUNICIPIO/Receptor/Gastos/'
    ruta_pago       = 'CFDI_RFC_MUNICIPIO/Receptor/Pagos/'

    #create an excel file with the names of the attributes in the index
    wb = Workbook()
    ws = wb.active
    ws.title = "comprobante_" + fecha_actual
    header_font = Font(color='FFFFFF')
    header_fill = PatternFill(start_color='730707', end_color='730707', fill_type='solid')
    for col_num, name in enumerate(name_list, 1):
        cell = ws.cell(row=1, column=col_num, value=name)
        cell.font = header_font
        cell.fill = header_fill
    
    # case type_option
    if type_option   == 1:
        ws.title = 'ayudas_' + fecha_actual
        filename = 'ayudas_' + fecha_actual + '.xlsx'
        directory = ruta_ayudas
        xlsx_path = os.path.join(ruta_ayudas, filename)
    elif type_option == 2:
        ws.title = 'ingreso_' + fecha_actual
        filename = 'ingreso_' + fecha_actual + '.xlsx'
        directory = ruta_ingreso
        xlsx_path = os.path.join(ruta_ingreso, filename)
    elif type_option == 3:
        ws.title = 'nomina_' + fecha_actual
        filename = 'nomina_' + fecha_actual + '.xlsx'
        directory = ruta_nomina
        xlsx_path = os.path.join(ruta_nomina, filename)
    elif type_option == 4:
        ws.title = 'des_bon_dev_' + fecha_actual
        filename = 'des_bon_dev_' + fecha_actual + '.xlsx'
        directory = ruta_desbondev
        xlsx_path = os.path.join(ruta_desbondev, filename)
    elif type_option == 5:
        ws.title = 'gasto_' + fecha_actual
        filename = 'gasto_' + fecha_actual + '.xlsx'
        directory = ruta_gasto
        xlsx_path = os.path.join(ruta_gasto, filename)
    elif type_option == 6:
        ws.title = 'pago_' + fecha_actual
        filename = 'pago_' + fecha_actual + '.xlsx'
        directory = ruta_pago
        xlsx_path = os.path.join(ruta_pago, filename)
    elif type_option == 7:
        return
    
    wb.save(xlsx_path)
    print('\nXLSX file created successfully.')
    
    # function call that modifies the xlsx headers for elements repeated from the standard
    try: 
        modify_headers(xlsx_path)
        
        #traverses a directory and its subdirectories, looking for XML files
        def filenames(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.xml'):
                    yield(os.path.join(directory, filename))

        wb = load_workbook(xlsx_path)
        ws = wb.active
        headers = [cell.value for cell in ws[1]]

        #open the file "Report_CFDI.xlsx" and fill in the data rows corresponding to each XML file
        for xml_file in filenames(directory):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                emisor      = root.find('{http://www.sat.gob.mx/cfd/3}Emisor')
                receptor    = root.find('{http://www.sat.gob.mx/cfd/3}Receptor')

                if emisor is not None and receptor is not None:
                    row_data = {}
                    for nodo in root.iter():
                        if nodo.attrib:
                            for key, value in nodo.attrib.items():
                                if key in headers:
                                    row_data['Rfc']             = str(emisor.get('Rfc'))
                                    row_data['Rfc receptor']    = str(receptor.get('Rfc'))
                                    row_data['Nombre']          = str(emisor.get('Nombre'))
                                    row_data['Nombre receptor'] = str(receptor.get('Nombre'))
                                    row_data[key]               = value
                    if row_data:
                        row_num = ws.max_row + 1
                        for col_num, header in enumerate(headers, 1):
                            if header in row_data:
                                if header == 'Total' or header == 'SubTotal' or header == 'TotalImpuestosRetenidos' or header == 'Descuento' or header == 'Importe' or header == 'ValorUnitario' or header == 'Base' or header == 'TasaOCuota':
                                    ws.cell(row=row_num, column=col_num, value=float(row_data[header]))
                                    cell.alignment = Alignment(horizontal='right')
                                else:
                                    ws.cell(row=row_num, column=col_num, value=row_data[header])                

            except ET.ParseError:
                print(f'Error parsing {xml_file}: file does not comply with CFDI 3.3 standard')
        #saving the values that correspond to each header.
        wb.save(xlsx_path)
        print('\nXLSX file modified successfully.')
    except Exception as e:
        print(f"Error: {e}")

#displays a menu with three options: create the XLSX file, insert the XLSX file, and exit the program.
def print_menu():
    print('Select an option:')
    print('1. report in excel for receipt type help')
    print('2. report in excel for receipt type income')
    print('3. report in excel for receipt type expense')
    print('4. report in excel for receipt type discounts bonuses returns')
    print('5. report in excel for receipt type spent')
    print('6. report in excel for receipt type pay')
    print('7. Exit')
    
while True:
    print_menu()
    selection = input('Enter your selection: ')
    try:
        selection = int(selection)
    except ValueError:
        print('You must enter a whole number')
        continue
    create_xlsx(selection)