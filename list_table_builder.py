#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [25/07/2023]
# Description:      [list of specific functions to chart a CFDI in PDF format]

# import necessary modules
from reportlab.lib.styles           import getSampleStyleSheet
from reportlab.platypus             import Paragraph

def get_related_cfdi_table(rows, row_related_node):
    # define related cfdi table header instance
    table = []
    # loop through the list of rows containing the cfdi in node pago10:Pago
    for row in rows:
        nodes = row.getElementsByTagName(row_related_node)
        # create a list comprehension to extract the required attributes of each related cfdi node
        related_cfdi = [value for node in nodes for value in [node.getAttribute('IdDocumento'), node.getAttribute('Serie'), node.getAttribute('Folio'), node.getAttribute('ImpSaldoAnt'), node.getAttribute('ImpPagado')]]
        # insert the list of attributes of the related cfdi at the beginning of the table
        if related_cfdi:
            table.insert(0, related_cfdi)
    # return the table built with the required attributes of the related cfdi
    return table

def get_cfdi_concepts(docs):
    # Loop through all "cfdi:Concept" nodes and store selected attributes in a list
    concepto_attrs_list = []
    for doc in docs:
        # Get the selected attributes of the current "cfdi:Concept" node
        clave_prodserv    = doc.getAttribute('ClaveProdServ')
        cantidad          = int(float(doc.getAttribute('Cantidad')))
        clave_unidad      = doc.getAttribute('ClaveUnidad')
        descripcion       = doc.getAttribute('Descripcion')
        if '.' in descripcion:
            descripcion = descripcion[:descripcion.index('.')+3]
        else:
            descripcion += '.00'
        valor_unitario_str = doc.getAttribute('ValorUnitario')
        if '.' in valor_unitario_str:
            # If 'ValorUnitario' has decimals, only consider the first two
            valor_unitario_str = valor_unitario_str[:valor_unitario_str.index('.')+3]
        else:
            # If 'ValorUnitario' does not have decimals, add '.00'
            valor_unitario_str += '.00'
        valor_unitario    = float(valor_unitario_str)

        # Save the attributes in a list and add it to the list
        attrs_list = [clave_prodserv, cantidad, clave_unidad, descripcion, valor_unitario]
        concepto_attrs_list.append(attrs_list)

    # return the list of attributes of the "cfdi:Concept" nodes
    return concepto_attrs_list

def get_transfers(taxes):
    # receives the cfdi:Impuestos node, to parse its content and collect transfers
    transfer_list = {}
    try:
        transfers = taxes.getElementsByTagName('cfdi:Traslado')
    except AttributeError:
        transfers = []
    # relocates the value of the attributes in the dictionary transfer_list
    for transfer in transfers:
        try:
            amount  = transfer.getAttribute('Importe')
            tax     = transfer.getAttribute('Impuesto')
            transfer_list[tax] = amount
        except:
            continue
    return transfer_list

def get_withholdings(taxes):
    # receives the "cfdi:Impuestos" node, to parse its content and collect withholdings
    withholdings_list = {}
    try:
        withholdings = taxes.getElementsByTagName('cfdi:Retencion')
    except AttributeError:
        withholdings = []

    # relocates the value of the attributes in the dictionary withholdings_list
    for withholding in withholdings:
        try:
            amount  = withholding.getAttribute('Importe')
            tax     = withholding.getAttribute('Impuesto')
            withholdings_list[tax] = amount
        except:
            continue
    return withholdings_list

def get_cfdi_concepts_table(receipt, concepts, taxes, type):
    # remaps the contents of the dictionary to use its values for each tax
    transfers       = get_transfers(taxes)
    withholdings    = get_withholdings(taxes)

    # definition of attributes to build the part of totals and taxes of the table of concepts
    subtotal        = '{:.2f}'.format(float(receipt[0].getAttribute('SubTotal')))
    discount        = receipt[0].getAttribute('Descuento') or '0.00'
    total           = '{:.2f}'.format(float(receipt[0].getAttribute('Total')))
    isr             = '0.00' 
    iva             = '0.00'
    ieps            = '0.00'
    ret_iva         = '0.00'
    ret_isr         = '0.00'
    
    # assign tax to its corresponding variable
    if '001' in transfers:
        isr     = '{:.2f}'.format(round(float(transfers['001']), 2))
    if '002' in transfers:
        iva     = '{:.2f}'.format(round(float(transfers['002']), 2))
    if '003' in transfers:
        ieps    = '{:.2f}'.format(round(float(transfers['003']), 2))
        
    if '001' in withholdings: 
        ret_isr = '{:.2f}'.format(round(float(withholdings['001']), 2))
    if '002' in withholdings:
        ret_iva = '{:.2f}'.format(round(float(withholdings['002']), 2))

    # define header instance, totals and taxes from cfdi table concepts
    table = [
        ['', '', '', '', '', '  SubTotal $' , subtotal],
        ['', '', '', '', '', '- Descuento $', discount],
        ['', '', '', '', '', '+ IEPS $'     , ieps],
        ['', '', '', '', '', '+ IEPS $'     , isr],
        ['', '', '', '', '', '+ IVA 16% $'  , iva],
        ['', '', '', '', '', '- Ret __% ISR', ret_isr],
        ['', '', '', '', '', '- Ret __% IVA', ret_iva],
        ['', '', '', '', '', '= Total $'    , total]
    ]
    
    concepts = get_cfdi_concepts(concepts.getElementsByTagName('cfdi:Concepto'))
    
    # inserts into the table the required attributes of the cfdi concepts
    for concept in reversed(concepts):
        table.insert(0, concept)
    
    # create a paragraph style object for the text in column "descripción"
    styledesc           = getSampleStyleSheet()['Normal']
    styledesc.alignment = 0     # concept alignment type
    styledesc.leading   = 7     # size between each line break of the concept
    styledesc.fontSize  = 7     # concept font size
    
    # split column "descripción" text into multiple lines
    for row in table[0:]:
        row[3] = Paragraph(row[3], styledesc)
    
    return table