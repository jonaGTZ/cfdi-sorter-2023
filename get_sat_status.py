#!/usr/bin/env python3.11.1
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [05/17/2023]
# Description:      [Brief description of the purpose of the script]

import requests.exceptions


from cfdiclient import Validacion

# Create an instance of the Validacion class
validation = Validacion()

def get_sat_status(rfc_sender, rfc_receiver, total, uuid):

    status = None
    while not status:
        try:
            status = validation.obtener_estado(rfc_sender, rfc_receiver, total, uuid)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(f'{e}')
            return 'Cancelado'

    return status.get('estado')
