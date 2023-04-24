# import necessary modules
import os
import pandas as pd

from lxml       import etree
from datetime   import datetime

# Gets the current date and time
now = datetime.now().strftime('%m%d%Y-%H%M%S')

def cfdi_to_xlsx(dirpath, rfc):
    # Define the list of columns for the DataFrame
    columnas = ["nombre"] 

    # Create an empty list for the rows
    filas = []

    # Iterate over all XML files in the specified path
    for dir, subdir, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".xml"):
                # Get the full path of the XML file
                filename = os.path.join(dir, file)
                
                # Parse the XML file with lxml
                arbol = etree.parse(filename)
                
                # Get all nodes and their attributes
                for nodo in arbol.iter():
                    for atributo in nodo.attrib:
                        # Add each unique attribute as a column of the DataFrame
                        if atributo not in columnas:
                            columnas.append(atributo)
                
                # Create a row for the current file
                fila = {"nombre": filename}
                
                # Get all attribute values for each node in the file
                for nodo in arbol.iter():
                    for atributo in nodo.attrib:
                        fila[atributo] = nodo.attrib[atributo]
                
                # Add the row to the list of rows
                filas.append(fila)

    # Create a DataFrame from the list of rows
    df = pd.concat([pd.DataFrame(fila, index=[0]) for fila in filas], ignore_index=True)
    
    # Create a ExcelWriter object
    writer = pd.ExcelWriter(f"{dirpath}/reporte-{now}.xlsx", engine='xlsxwriter')

    # Define the formatting for the header row
    header_format = writer.book.add_format({'bold': True, 'bg_color': '#730707', 'font_color': 'white'})

    # Convert the DataFrame to an Excel sheet
    df.to_excel(writer, sheet_name=f'{rfc}', index=False)
    
    worksheet = writer.sheets[f'{rfc}']

    # Format the header row
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Set the column widths to auto-fit
    for i, col in enumerate(df.columns):
        column_width = max(df[col].astype(str).map(len).max(), len(col))
        worksheet.set_column(i, i, column_width)

    # Save the Excel file
    writer.save()

# Main script code
# if __name__ == '__main__':
#     cfdi_to_xlsx('MHS850101F67/Receptor/Descuento_Bonificaciones_Devoluciones/', 'MHS850101F67')
#     pass
