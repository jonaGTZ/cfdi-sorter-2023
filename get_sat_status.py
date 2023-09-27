#!/usr/bin/env python3.11.1
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [05/17/2023]
# Description:      [Brief description of the purpose of the script]

import requests.exceptions
import html

from cfdiclient     import Validacion

# Create an instance of the Validacion class
validation = Validacion()

def get_sat_status(rfc_sender, rfc_receiver, total, uuid):
    
    # Encode RFC variables in UTF-8
    rfc_sender_encoded      = html.escape(rfc_sender)
    rfc_receiver_encoded    = html.escape(rfc_receiver)
    
    status                  = None

    while not status:
        try:
            # Usar las variables codificadas en lugar de las originales
            status = validation.obtener_estado(rfc_sender_encoded, rfc_receiver_encoded, total, uuid)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(f'{e}')
            return 'Desconocido'

    return status.get('estado')