#!/usr/bin/env python3.11.1
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/26/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import os
import shutil
import json

from datetime       import datetime
from lxml           import etree
from get_sat_status import get_sat_status

# Define the subdirectories
emisor_directory        = 'Emisor'
receptor_directory      = 'Receptor'
err_directory           = 'Error'

# Define the sub-subdirectories
ingresos_directory      = 'Ingresos'
gastos_directory        = 'Gastos'
ayudas_directory        = 'Ayudas'
des_bon_dev_directory   = 'Descuento_Bonificaciones_Devoluciones'
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

    ingresos_dict       = {}
    gastos_dict         = {}
    ayudas_dict         = {}
    des_bon_dev_dict    = {}
    nomina_dict         = {}
    pagosE_dict         = {}
    pagosR_dict         = {}

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
                total       = root.get('Total')
            
            emisor_query, receptor_query, complemento_query = get_cfdi_version(version)

            uuid = root.find(f'.//{complemento_query}').find('{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital').get('UUID')

            # Check if the UUID is already in the set
            if uuid in uuids_set:
                try:
                    os.makedirs(os.path.join(rfc, err_directory, 'Duplicados'))
                    shutil.copy(filename, os.path.join(rfc, err_directory, 'Duplicados', os.path.basename(filename)))
                except FileExistsError :                    
                    raise FileExistsError(f"E1: {uuid} already exists.")

            # Add the UUID to the set
            uuids_set.add(uuid)

            # Gets the RFC of the sender and receiver to whom the classification algorithm applies
            emisor      = root.find(f'.//{emisor_query}').get('Rfc')
            receptor    = root.find(f'.//{receptor_query}').get('Rfc')

            # Check if emisor, receptor, tipo, and metodo_pago are not None
            if emisor is None or receptor is None or tipo is None:
                raise Exception(f"E2: {filename} does not meet the requirements of the CFDI sorter standard.")
            
            # get SAT status
            sat_status = 'Desconocido'
            try:
                sat_status = get_sat_status(emisor, receptor, total, uuid)
            except:
                raise Exception(f'E3: {filename} failed to get sat status.')

            # Create a dictionary with the data
            data = {
                'Estado SAT'    : sat_status,
                'Fecha Consulta': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            }
            
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
                ingresos_dict[uuid] = [data]
            elif tipo == 'I' and receptor    == rfc:
                subdirectory = gastos_directory
                gastos_dict[uuid] = [data]
            elif tipo == 'E' and emisor      == rfc:
                subdirectory = ayudas_directory
                ayudas_dict[uuid] = [data]
            elif tipo == 'E' and receptor    == rfc:
                subdirectory = des_bon_dev_directory
                des_bon_dev_dict[uuid] = [data]
            elif tipo == 'N' and emisor      == rfc:
                
                tipo_nomina = root.find(".//{http://www.sat.gob.mx/nomina12}Nomina")
                if tipo_nomina is not None:
                    tipo_nomina     = tipo_nomina.attrib.get('TipoNomina', '')
                nomina_directory    = f'Nomina/nomina_{tipo_nomina}'
                subdirectory        = nomina_directory
                nomina_dict[uuid]   = [data]

            elif tipo == 'P' and emisor      == rfc:
                subdirectory = pagosE_directory
                pagosE_dict[uuid] = [data]
            elif tipo == 'P' and receptor    == rfc:
                subdirectory = pagosR_directory
                pagosR_dict[uuid] = [data]
            else:
                raise Exception(f"E4: {filename} does not belong to any of the classifier folders.")

            # Create the sub-subdirectory inside the appropriate subdirectory
            sub_subdirectory = os.path.join(emisor_directory, subdirectory, sat_status, metodo_pago) if emisor == rfc else os.path.join(receptor_directory, subdirectory, sat_status, metodo_pago)
            try:
                os.makedirs(os.path.join(rfc, sub_subdirectory))
            except FileExistsError :
                pass

            # Copy the XML file to the appropriate sub-subdirectory
            shutil.copy(filename, os.path.join(rfc, sub_subdirectory, os.path.basename(filename)))
        
        except FileExistsError:
            shutil.copy(filename, os.path.join(rfc, err_directory, 'Duplicados', os.path.basename(filename)))
            
        except Exception as e:
            print(f"{filename} : {e}")
            try:
                os.makedirs(os.path.join(rfc, err_directory))
            except FileExistsError :
                pass
            shutil.copy(filename, os.path.join(rfc, err_directory, os.path.basename(filename)))
            continue
    try:
        
        carpeta_status = f'{rfc}/status'

        if not os.path.exists(carpeta_status):
            os.makedirs(carpeta_status)

        with open(f'{carpeta_status}/INGRESO.json', 'a') as file:
            json.dump(ingresos_dict, file, indent=4)

        with open(f'{carpeta_status}/GASTO.json', 'a') as file:
            json.dump(gastos_dict, file, indent=4)

        with open(f'{carpeta_status}/AYUDAS.json', 'a') as file:
            json.dump(ayudas_dict, file, indent=4)

        with open(f'{carpeta_status}/DES_BON_DEV.json', 'a') as file:
            json.dump(des_bon_dev_dict, file, indent=4)

        with open(f'{carpeta_status}/NOMINA.json', 'a') as file:
            json.dump(nomina_dict, file, indent=4)

        with open(f'{carpeta_status}/PAGO_E.json', 'a') as file:
            json.dump(pagosE_dict, file, indent=4)

        with open(f'{carpeta_status}/PAGO_R.json', 'a') as file:
            json.dump(pagosR_dict, file, indent=4)

    except (FileExistsError, Exception) as e:
        raise ('ocurrio un error inesperado')