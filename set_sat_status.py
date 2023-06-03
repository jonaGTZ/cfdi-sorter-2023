#!/usr/bin/env python3.11.1
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [05/18/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import json

def get_file(option, rfc):
    dirs = {
        'AYUDAS'        : f'{rfc}/status/AYUDAS.json',
        'INGRESO'       : f'{rfc}/status/INGRESO.json',
        'NOMINA'        : f'{rfc}/status/NOMINA.json',
        'PAGO_E'        : f'{rfc}/status/PAGO_E.json',
        'DES_BON_DEV'   : f'{rfc}/status/DES_BON_DEV.json',
        'GASTO'         : f'{rfc}/status/GASTO.json',
        'PAGO_R'        : f'{rfc}/status/PAGO_R.json'
    }
    return dirs.get(option)

def set_sat_status(uuid, option, rfc):

    # Load the JSON file
    with open(get_file(option, rfc), "r") as file:
        data = json.load(file)

    # Find the key and get its value
    clave           = data.get(uuid)
    estado_sat      = None
    fecha_consulta  = None

    if isinstance(clave, list):
        if len(clave) > 0 and isinstance(clave[0], dict):
            estado_sat      = clave[0].get('Estado SAT')
            fecha_consulta  = clave[0].get('Fecha Consulta')

    return estado_sat, fecha_consulta