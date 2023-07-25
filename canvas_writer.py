#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [25/07/2023]
# Description:      [list of specific functions to chart a CFDI in PDF format]

# pdf build modules
from reportlab.lib.utils            import ImageReader
from reportlab.platypus             import Table, TableStyle
from reportlab.lib                  import colors
from reportlab.lib.units            import inch
from reportlab.lib.pagesizes        import letter
# qr build modules
from reportlab.graphics             import renderPDF
from reportlab.graphics.shapes      import Drawing
from reportlab.graphics.barcode.qr  import QrCodeWidget

""" 
    preliminary function definition addendum for drawing on the canvas that builds a pdf for each cfdi

"""
# Tandem image path
image_path = 'tandemlogo.png'

def drawline(c, x, y, text):
    c.setFillColorRGB(0, 0, 0)
    c.setFontSize(9)
    # Check if the y position exceeds the page height and create a new page if necessary
    if y < 25:
        c.showPage()
        c.setFontSize(9)
        y = letter[1] - 25
    c.drawString(x, y, text)
    return y

def draw_concept_table(c, rows, x, y, cfdi_tipo):
    
    # obtain the height of the table | 18' is the size of each row
    limit = len(rows) * 18
    
    if cfdi_tipo == 'E':
        limit = len(rows) * 21    

    data = [['ClaveProdServ', 'Cantidad', 'Unidad Medida', 'Descripción', 'Valor Unitario', 'Impuestos', 'Importe']]

    # algorithm to lay the table in the PDF respectively at its height
    if y <= 25:
        c.showPage()
        y = letter[1] - 25
    else: 
        while limit > 0 and y > 25:
            if rows:
                data.append(rows.pop(0))
            if cfdi_tipo == 'E':
                y -= 21
                limit -= 21
            else:
                y -= 18
                limit -= 18
            
    # generate size and style of concept table
    table = Table(data, colWidths=[75, 45, 60, 200, 70, 75, 65])
    table.setStyle(TableStyle([
        ('FONTNAME'  , (0,0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE'  , (0,0), (-1, 0), 8),
        ('BACKGROUND', (0,0), (-1, 0), colors.Color(0.447, 0.027, 0.027)),
        ('TEXTCOLOR' , (0,0), (-1, 0), colors.white),
        ('ALIGN'     , (0,0), (-1,-1), 'CENTER'),
        ('ALIGN'     , (4,1), ( 4,-1), 'RIGHT'),
        ('ALIGN'     , (5,1), ( 5,-1), 'RIGHT'),
        ('ALIGN'     , (6,1), ( 6,-1), 'RIGHT'),
    ]))

    if table._nrows > 1:
        table.wrapOn(c, inch, inch)
        table.drawOn(c, x, y)

    if rows:
        y = draw_concept_table(c, rows, x, y, cfdi_tipo)
    return y

def draw_related_table(c, rows, x, y):
    
    # obtain the height of the table | 18' is the size of each row (needs adjustment) 
    limit = len(rows) * 18
    data = [['IdDocumento', 'Serie', 'Folio', 'ImpSaldoAnt', 'ImpPagado'],]

    # algorithm to lay the table in the PDF respectively at its height
    if y <= 25:
        c.showPage()
        y = letter[1] - 25
    else: 
        while limit > 0 and y > 25:
            if rows:
                data.append(rows.pop(0))
            y -= 18
            limit -= 18
    
    # generate size and style of concept table
    table = Table(data, colWidths=[260, 70, 70, 95, 95])
    table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.Color(0.447, 0.027, 0.027)),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 8)
    ]))
    table.wrapOn(c, inch, inch)
    table.drawOn(c, x, y)
    if rows:
        y = draw_related_table(c, rows, x, y)
    return y

def drawrect(c, x, y, w, h, f, s): 
    c.setFillColorRGB(0.447, 0.027, 0.027)    
    if y < 25:
        c.showPage()
        c.setFillColorRGB(0.447, 0.027, 0.027)
        y = letter[1] - 25
        y -= h
    c.rect(x, y, w, h, fill=f, stroke=s)
    return y

def drawtittle(c, x, y, text):
    c.setFillColorRGB( 1, 1, 1)
    c.setFontSize(12)
    # Check if the y position exceeds the page height and create a new page if necessary
    if y < 25:
        c.showPage()
        y = letter[1] - 25
    c.drawString(x, y, text)
    return y - 18

def drawsubtittle(c, x, y, text):
    c.setFillColorRGB( 1, 1, 1)
    c.setFontSize(7)
    # Check if the y position exceeds the page height and create a new page if necessary
    if y < 25:
        c.showPage()
        y = letter[1] - 25
    c.drawString(x, y, text)
    return y - 18

def drawimage(c, x, y):
    logo = ImageReader(image_path)
    logo_width, logo_height = logo.getSize()
    y -= (logo_height / 7.5)
    c.drawImage(logo, x, y, logo_width/7.5, logo_height/7.5)
    return y - 24

def drawQR(c, x, y, url):
    # create a QR code widget with the qrcode library
    qr_code = QrCodeWidget(url)
    bounds = qr_code.getBounds()
    # calculate the scale needed for the QR code to
    width, height = 170, 170
    x_scale = width / (bounds[2] - bounds[0])
    y_scale = height / (bounds[3] - bounds[1])
    d = Drawing(width, height, transform=[x_scale, 0, 0, y_scale, -bounds[0] * x_scale, -bounds[1] * y_scale])
    d.add(qr_code)
    if y < 25:
        c.showPage()
        y = letter[1] - 25
        y -= 150
    # draw the QR code on the PDF file
    renderPDF.draw(d, c, x, y)
    return y