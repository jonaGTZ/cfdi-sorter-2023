# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/24/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import os
import pandas as pd

from lxml           import etree
from datetime           import datetime, timedelta
from xml.dom            import minidom
from list_table_builder import get_cfdi_concepts

# Gets the current date and time
now = datetime.now().strftime('%m%d%Y-%H%M%S')

def get_concepts(filename):
    cfdi = minidom.parse(filename)
    # get cfdi nodes to build pdf with required data
    cfdi_conceptos_node   = cfdi.getElementsByTagName('cfdi:Conceptos')[0]
    concepts_rows = get_cfdi_concepts(cfdi_conceptos_node.getElementsByTagName('cfdi:Concepto'))
    return concepts_rows

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

def cfdi_to_xlsx(option, rfc):
    # Define the path of cfdi's dir 
    dirpath     = get_dir_path_data(option, rfc)
    
    # Define the list of columns for the DataFrame and an empty list for the rows
    columnas    = ["Rfc Emisor", "Nombre Emisor", "CFDI VERSION", 'Lista de Conceptos']
    filas       = []

    # # prints to the console a prediction of the delay time of the algorithm
    # remaining_time = remaining_traversal_time(dirpath)
    # print(f"Estimated remaining time (HH:MM:SS:MS): {remaining_time}")

    # Iterate over all XML files in the specified path
    for dir, subdir, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".xml"):
                # Get the full path of the XML file
                filename = os.path.join(dir, file)
            
                # Parse the XML file with lxml
                try: 
                    arbol = etree.parse(filename)
                except Exception as e:
                    print(f'E1: Impossible to parse the tree: {filename}')
                    continue
                
                # Get all nodes and their attributes
                for nodo in arbol.iter():
                    for atributo in nodo.attrib:
                        # Add each unique attribute as a column of the DataFrame
                        if atributo not in columnas:
                            columnas.append(atributo)
                
                # Create a row for the current file
                fila = {}
                
                # Get all attribute values for each node in the file
                for nodo in arbol.iter():
                    for atributo in nodo.attrib:
                        fila[atributo] = nodo.attrib[atributo]

                    # Add "Version" attribute of "cfdi:Comprobante" node as new column
                    if nodo.tag.endswith('Comprobante'):
                        if 'Version' in nodo.attrib:
                            fila['CFDI VERSION'] = nodo.attrib['Version']
                    # Add "Rfc" and "Nombre" attributes of "cfdi:Receptor" and "cfdi:Emisor" node as new columns
                    if nodo.tag.endswith('Emisor'):
                        if 'Rfc' in nodo.attrib:
                            fila['Rfc Emisor'] = nodo.attrib['Rfc']
                        if 'Nombre' in nodo.attrib:
                            fila['Nombre Emisor'] = nodo.attrib['Nombre']
                            
                # creates a list of the concepts and inserts them in the column "List of Concepts"
                conceptos = get_concepts(filename)
                fila['Lista de Conceptos'] = str(conceptos)

                # Add the row to the list of rows
                filas.append(fila)
                
    try:
        # Create a DataFrame from the list of rows
        df = pd.concat([pd.DataFrame(fila, index=[0]) for fila in filas], ignore_index=True)

        # Create a ExcelWriter object
        writer = pd.ExcelWriter(f"{dirpath}/{now}-{option}.xlsx", engine='xlsxwriter')

        # Define the formatting for the header row
        header_format = writer.book.add_format({'bold': True, 'bg_color': '#730707', 'font_color': 'white'})

        # Convert the DataFrame to an Excel sheet
        df.to_excel(writer, sheet_name=f'{option}', index=False)
        
        worksheet = writer.sheets[f'{option}']

        # Format the header row
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # # Set the column widths to auto-fit
        # for i, col in enumerate(df.columns):
        #     column_width = max(df[col].astype(str).map(len).max(), len(col))
        #     worksheet.set_column(i, i, column_width)

        # Save the Excel file
        writer.close()
    except Exception as e:
        print(f'E2: {e}')
        pass

def remaining_traversal_time(dirpath):
    file_count = 0
    for dir, subdir, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".xml"):
                file_count += 1

    # Calculate the average processing time per file (in seconds)
    avg_time_per_file = 0.5  # <-- replace with actual average processing time

    # Calculate the remaining processing time (in seconds)
    remaining_time = avg_time_per_file * file_count

    # Format the remaining time as HH:MM:SS
    remaining_time_str = str(timedelta(seconds=remaining_time))

    return remaining_time_str