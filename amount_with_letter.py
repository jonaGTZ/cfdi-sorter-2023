#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [25/07/2023]
# Description:      [algorithm that converts a float quantity to letter quantity]

def amount_with_letter(amount):
    units       = ['', 'UNO', 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS', 'SIETE', 'OCHO', 'NUEVE']
    tens        = ['', 'DIEZ', 'VEINTE', 'TREINTA', 'CUARENTA', 'CINCUENTA', 'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA']
    specials    = ['ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE']
    hundreds    = ['', 'CIENTO ', 'DOSCIENTOS ', 'TRECIENTOS ', 'CUATROCIENTOS ', 'QUINIENTOS ', 'SEISCIENTOS ', 'SETECIENTOS ', 'OCHOCIENTOS ', 'NOVECIENTOS ']
    thousands   = ['', 'MIL', 'MILLÓN']

    # round to two decimal places
    amount = round(amount, 2)

    # separate the integer and decimal part
    entero, decimal = str(amount).split(".")
    entero = int(entero)

    # convert integer part to letters
    letters = ""
    if entero == 0:
        return 'CERO MN'
    else:
        # convert groups of three digits to letters
        grous = []
        while entero > 0:
            grous.append(entero % 1000)
            entero //= 1000

        for i, grupo in enumerate(grous):
            if grupo == 0:
                continue

            group_letters = ""
            c = grupo // 100
            if c > 0:
                if grupo == 100 and i == 0:
                    group_letters += "CIEN"
                else:
                    group_letters += hundreds[c]
                
            d = grupo % 100 // 10
            u = grupo % 10
            if d == 0:
                if u > 0:
                    group_letters += units[u]
            elif d == 1:
                if u >= 1 and u <= 5:
                    group_letters += specials[u - 1]
                else:
                    group_letters += tens[d] + " Y " + units[u]
            else:
                if u > 0:
                    group_letters += tens[d] + " Y " + units[u]
                else:
                    group_letters += tens[d]

            if i == 1 and grupo == 1:
                group_letters = " MIL"
            elif i > 0:
                if grupo == 1:
                    group_letters += " " + thousands[i]
                else:
                    group_letters += " " + thousands[i] + " "

            letters = group_letters + " " + letters

        # remove leading and trailing spaces
        letters = letters.strip()

    # add the decimal part in letters
    if decimal != '0' and '00':
        letters += " " + decimal + "/100 MN"
    else:
        letters += ' 0/100 MN'
    return letters