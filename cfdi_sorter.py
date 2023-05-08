#!/usr/bin/env python3.11.1
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/26/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
from lxml import etree
import os
import shutil

# Define the subdirectories
emisor_directory        = 'Emisor'
receptor_directory      = 'Receptor'
err_directory           = 'Error'

# Define the sub-subdirectories
ingresos_directory      = 'Ingresos'
gastosR_directory       = 'Gastos'
ayudas_directory        = 'Ayudas'
des_bon_dev_directory   = 'Descuento_Bonificaciones_Devoluciones'
nomina_directory        = 'Nomina'
pagosE_directory        = 'Pagos'
pagosR_directory        = 'Pagos'

def get_cfdi_version(version):
    if   version == '4.0':
        comp_query      = '{http://www.sat.gob.mx/cfd/4}Complemento'
        emisor_query    = '{http://www.sat.gob.mx/cfd/4}Emisor'
        receptor_query  = '{http://www.sat.gob.mx/cfd/4}Receptor'
    elif version == '3.3':
        comp_query      = '{http://www.sat.gob.mx/cfd/3}Complemento'
        emisor_query    = '{http://www.sat.gob.mx/cfd/3}Emisor'
        receptor_query  = '{http://www.sat.gob.mx/cfd/3}Receptor'

    return emisor_query, receptor_query, comp_query

def filenames(directory):
    for root, dirs, files in os.walk(directory):
        #if dirpath == directory: continue
        for file in files:
            if file.endswith(".xml"):
                yield os.path.join(root, file)

def cfdi_sorter(rfc, directory):
    # Initialize the set to store the UUIDs
    uuids_set = set()

    # Calls the function "filenames" Iterating over each XML file in the directory
    for filename in filenames(directory):
        try:
            # Parse the XML file with lxml
            tree = etree.parse(filename)
            root = tree.getroot()
            
            # searches the "cfdi:Comprobante" node for the attributes that build the classification
            if root.tag.endswith('Comprobante'):
                tipo        = root.get('TipoDeComprobante')
                metodo_pago = root.get('MetodoPago')
                version     = root.get('Version')
            
            emisor_query, receptor_query, complemento_query = get_cfdi_version(version)

            uuid = root.find(f'.//{complemento_query}').find('{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital').get('UUID')

            # Check if the UUID is already in the set
            if uuid in uuids_set:
                raise Exception(f"E1: {uuid} already exists.")

            # Add the UUID to the set
            uuids_set.add(uuid)

            # Gets the RFC of the sender and receiver to whom the classification algorithm applies
            emisor      = root.find(f'.//{emisor_query}').get('Rfc')
            receptor    = root.find(f'.//{receptor_query}').get('Rfc')

            # Check if emisor, receptor, tipo, and metodo_pago are not None
            if emisor is None or receptor is None or tipo is None:
                raise Exception(f"E2: {filename} does not meet the requirements of the CFDI sorter standard.")

            # Check if the value of metodo_pago is valid
            if metodo_pago not in ['PUE', 'PPD']:
                if tipo == 'P':
                    metodo_pago = 'PAGO'
                else:
                    print(f"{filename} : E3: MetodoPago is not valid: {metodo_pago}")
                    continue

            # Create the appropriate sub-subdirectory and copy the XML file based on the attribute values
            if   tipo == 'I' and emisor      == rfc:
                subdirectory = ingresos_directory
            elif tipo == 'I' and receptor    == rfc:
                subdirectory = gastosR_directory
            elif tipo == 'E' and emisor      == rfc:
                subdirectory = ayudas_directory
            elif tipo == 'E' and receptor    == rfc:
                subdirectory = des_bon_dev_directory
            elif tipo == 'N' and emisor      == rfc:
                subdirectory = nomina_directory
            elif tipo == 'P' and emisor      == rfc:
                subdirectory = pagosE_directory
            elif tipo == 'P' and receptor    == rfc:
                subdirectory = pagosR_directory
            else:
                raise Exception(f"E4: {filename} does not belong to any of the classifier folders.")

            # Create the sub-subdirectory inside the appropriate subdirectory
            sub_subdirectory = os.path.join(emisor_directory, subdirectory, metodo_pago) if emisor == rfc else os.path.join(receptor_directory, subdirectory, metodo_pago)
            try:
                os.makedirs(os.path.join(rfc, sub_subdirectory))
            except FileExistsError :
                pass

            # Copy the XML file to the appropriate sub-subdirectory
            shutil.copy(filename, os.path.join(rfc, sub_subdirectory, os.path.basename(filename)))

        except Exception as e:
            print(f"{e}")
            try:
                os.makedirs(os.path.join(rfc, err_directory))
            except FileExistsError :
                pass
            shutil.copy(filename, os.path.join(rfc, err_directory, os.path.basename(filename)))
            continue