#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/07/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import os
import shutil
import xml.etree.ElementTree as ET

# Define the subdirectories
emisor_directory            = 'Emisor'
receptor_directory          = 'Receptor'
err_directory               = 'Errors'

# Define the sub-subdirectories
ingresos_directory          = 'Ingresos'
gastos_receptor_directory   = 'Gastos'
gastos_emitidos_directory   = 'Gastos'
ayudas_directory            = 'Ayudas'
des_bon_dev_directory       = 'Descuento_Bonificaciones_Devoluciones'
nomina_directory            = 'Nomina'
pagosE_directory            = 'Pagos'
pagosR_directory            = 'Pagos'

# Define the ElementPath queries
emisor_query                = '{http://www.sat.gob.mx/cfd/3}Emisor'
receptor_query              = '{http://www.sat.gob.mx/cfd/3}Receptor'
tipo_query                  = 'TipoDeComprobante'
mpago_query                 = 'MetodoPago'
fpago_query                 = 'FormaPago'

def filenames(directory):
    for root, dirs, files in os.walk(directory):
        #if dirpath == directory: continue
        for file in files:
            if file.endswith(".xml"):
                yield os.path.join(root, file)

def cfdi_sorter(rfc, directory):

    # Calls the function "filenames" Iterating over each XML file in the directory
    for filename in filenames(directory):
        try:
            # Parse the XML file with ElementTree
            tree = ET.parse(filename)
            root = tree.getroot()   

            # Get the value of the "TipoDeComprobante", "FormaPago", "MetodoPago" attributes
            tipo        = root.get(tipo_query)
            metodo_pago = root.get(mpago_query)

            # Get the "Emisor" element
            emisor      = root.find(emisor_query)
            # Get the "Receptor" element
            receptor    = root.find(receptor_query)
            
            # Check if emisor, tipo and receptor are not None
            if emisor is None or receptor is None:
                print(f"{filename} : E1: does not meet the requirements of the CFDI standard.")
                shutil.copy(filename, os.path.join(rfc, err_directory, os.path.basename(filename)))
                continue

            # Create the appropriate sub-subdirectory and copy the XML file based on the attribute values
            if   tipo == 'I' and emisor.get('Rfc')      == rfc:
                subdirectory = ingresos_directory
            elif tipo == 'I' and receptor.get('Rfc')    == rfc:
                subdirectory = gastos_receptor_directory
            elif tipo == 'I' and emisor.get('Rfc')      == rfc:
                subdirectory = gastos_emitidos_directory
            elif tipo == 'E' and emisor.get('Rfc')      == rfc:
                subdirectory = ayudas_directory
            elif tipo == 'E' and receptor.get('Rfc')    == rfc:
                subdirectory = des_bon_dev_directory
            elif tipo == 'N' and emisor.get('Rfc')      == rfc:
                subdirectory = nomina_directory
            elif tipo == 'P' and emisor.get('Rfc')      == rfc:
                subdirectory = pagosE_directory
            elif tipo == 'P' and receptor.get('Rfc')    == rfc:
                subdirectory = pagosR_directory
            else:       
                print(f"{filename} : E2: does not meet the requirements of the CFDI standard. Or Wrong RFC")
                continue
            
            if metodo_pago == 'PPD':
                subdirectory += "/PPD"
            else:
                subdirectory += "/PUE"

            # Create the sub-subdirectory inside the appropriate subdirectory
            sub_subdirectory = os.path.join(emisor_directory, subdirectory) if emisor.get('Rfc') == rfc else os.path.join(receptor_directory, subdirectory)
            
            try:
                os.makedirs(os.path.join(rfc, sub_subdirectory))
            except FileExistsError:
                pass

            # Copy the XML file to the appropriate sub-subdirectory
            shutil.copy(filename, os.path.join(rfc, sub_subdirectory, os.path.basename(filename)))

        except ET.ParseError:
            print(f"{filename} could not be parsed.")
        except Exception as e:
            print(f"{filename} could not be processed due to an error: {e}.")