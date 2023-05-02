#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [13/07/2023]
# Description:      [Brief description of the purpose of the script]

# local modules
from amount_with_letter         import amount_with_letter
from canvas_writer              import drawline, draw_concept_table, draw_related_table, drawrect, drawtittle, drawsubtittle, drawimage, drawQR
from list_table_builder         import get_related_cfdi_table, get_cfdi_concepts_table
# pdf build modules
from reportlab.pdfgen          import canvas
from reportlab.lib.styles      import ParagraphStyle
from reportlab.lib.units       import inch
from reportlab.lib.pagesizes   import letter
from reportlab.platypus        import Paragraph
# directory parser modules
from xml.dom                   import minidom
import os

def canvas_pdf_parser(filename, pdfname):
    # read the XML file using the minidom module
    cfdi = minidom.parse(filename)
    
    # get cfdi nodes to build pdf with required data
    cfdi_comprobante_node        = cfdi.getElementsByTagName('cfdi:Comprobante')
    cfdi_emisor_node             = cfdi.getElementsByTagName('cfdi:Emisor')
    cfdi_receptor_node           = cfdi.getElementsByTagName('cfdi:Receptor')
    cfdi_nomina_node             = cfdi.getElementsByTagName('nomina12:Nomina')
    cfdi_nomina_emisor_node      = cfdi.getElementsByTagName('nomina12:Emisor')
    cfdi_nomina_receptor_node    = cfdi.getElementsByTagName('nomina12:Receptor')
    cfdi_timbre_node             = cfdi.getElementsByTagName('tfd:TimbreFiscalDigital')

    # 
    if cfdi_comprobante_node[0].getAttribute('Version') == '4.0':
        cfdi_related_node   = cfdi.getElementsByTagName('pago20:Pago')
        row_related_node    = 'pago20:DoctoRelacionado'
    else: 
        cfdi_related_node   = cfdi.getElementsByTagName('pago10:Pago')
        row_related_node    = 'pago10:DoctoRelacionado'
    
    # verify that the cfdi can be traversed and retrieve the voucher type before creating the canvas object
    if cfdi_comprobante_node:
        cfdi_tipo                = cfdi_comprobante_node[0].getAttribute('TipoDeComprobante')    
        cfdi_conceptos_node      = cfdi.getElementsByTagName('cfdi:Conceptos')[0]
        cfdi_relacionados_node   = cfdi.getElementsByTagName('cfdi:CfdiRelacionados')
        cfdi_document_node       = cfdi.getElementsByTagName('cfdi:CfdiRelacionado')
    else: return
    
    # create the canvas object where to layout the cfdi data
    c = canvas.Canvas(pdfname, pagesize=letter)
    c.setFontSize(9)
    
    # define the start size and position of canva
    x = 10
    y = letter[1] - 25
    
    # build the header, add the title, the folio, and the serial number to which the cfdi belongs
    drawrect(c, x, y - 18, 590, 35, True, 0)
    if cfdi_tipo == 'N': drawtittle(c, x + 240, y, 'RECIBO DE NÓMINA')
    else: drawtittle(c, x + 280, y, 'FACTURA')
    drawsubtittle(c, x + 420, y, 'Serie:')
    y = drawsubtittle(c, x + 440, y, cfdi_comprobante_node[0].getAttribute('Serie')) + 9
    drawsubtittle(c, x + 420, y, 'Folio:')
    y = drawsubtittle(c, x + 440, y, cfdi_comprobante_node[0].getAttribute('Folio')) + 3 
    
    # create the section with the data of the sender and the logo of the person who issues the cfdi
    aux = drawimage(c, x + 30, y)
    y = drawline(c, x + 275, y-12, 'Nombre Emisor:')
    y = drawline(c, x + 350, y, cfdi_emisor_node[0].getAttribute('Nombre'))-12
    y = drawline(c, x + 275, y, 'RFC Emisor:')
    y = drawline(c, x + 350, y, cfdi_emisor_node[0].getAttribute('Rfc'))-12
    y = drawline(c, x + 275, y, 'Lugar expedicion:')
    y = drawline(c, x + 350, y, cfdi_comprobante_node[0].getAttribute('LugarExpedicion'))-12
    y = drawline(c, x + 275, y, 'Régimen Fiscal:')
    y = drawline(c, x + 350, y, cfdi_emisor_node[0].getAttribute('RegimenFiscal'))-12
    if cfdi_tipo == 'N':
        y = drawline(c, x + 275, y, 'Registro Patronal IMSS:')
        if 'RegistroPatronal' in cfdi_nomina_emisor_node:
            y = drawline(c, x + 390, y, cfdi_nomina_emisor_node[0].getAttribute('RegistroPatronal'))-12
        else:
            y = drawline(c, x + 390, y, 'N/A')-12
    y = drawline(c, x + 275, y, 'No de serie del Certificado del CSD:')
    y = drawline(c, x + 430, y, cfdi_comprobante_node[0].getAttribute('NoCertificado'))-12
    y = aux
    
    # construction of the section that contains the receiver data
    if cfdi_tipo == 'N':
        y = drawrect(c, x, y, 590, 20, True, 0)
        y = drawtittle(c, x+5, y + 6, 'DATOS DEL TRABAJADOR')
        y = drawline(c, x +  40, y, 'Nombre:')
        y = drawline(c, x + 130, y, cfdi_receptor_node[0].getAttribute('Nombre'))
        y = drawline(c, x + 300, y, 'Núm. Nómina:')
        y = drawline(c, x + 390, y, cfdi_emisor_node[0].getAttribute('RegimenFiscal'))-12
        y = drawline(c, x +  40, y, 'Núm. Trabajador:')
        y = drawline(c, x + 130, y, cfdi_nomina_receptor_node[0].getAttribute('NumEmpleado'))
        y = drawline(c, x + 300, y, 'Departamento:')
        y = drawline(c, x + 390, y, cfdi_nomina_receptor_node[0].getAttribute('Departamento'))-12
        y = drawline(c, x +  40, y, 'CURP:')
        y = drawline(c, x + 130, y, cfdi_nomina_receptor_node[0].getAttribute('Curp'))
        y = drawline(c, x + 300, y, 'Puesto:')
        y = drawline(c, x + 390, y, cfdi_nomina_receptor_node[0].getAttribute('Puesto'))-12
        y = drawline(c, x +  40, y, 'RFC:')
        y = drawline(c, x + 130, y, cfdi_receptor_node[0].getAttribute('Rfc'))
        y = drawline(c, x + 300, y, 'Inicio relación lab:')
        y = drawline(c, x + 390, y, cfdi_nomina_receptor_node[0].getAttribute('FechaInicioRelLaboral'))-12
        y = drawline(c, x +  40, y, 'NSS:')
        y = drawline(c, x + 130, y, cfdi_nomina_receptor_node[0].getAttribute('NumSeguridadSocial'))
        y = drawline(c, x + 300, y, 'Periodo:')
        y = drawline(c, x + 390, y, cfdi_nomina_receptor_node[0].getAttribute('PeriodicidadPago'))-12
        y = drawline(c, x +  40, y, 'Domicilio Fiscal:')
        y = drawline(c, x + 130, y, cfdi_comprobante_node[0].getAttribute('LugarExpedicion'))
        
        # remove decimals from the number of days paid
        dias_pagados = cfdi_nomina_node[0].getAttribute('NumDiasPagados')
        try:
            dias_pagados    = float(dias_pagados)
            dias_trabajados = int(dias_pagados)
        except ValueError:
            pass

        # you can then use the days_worked variable in your code as needed
        y = drawline(c, x + 300, y, 'Días Trabajados:')
        y = drawline(c, x + 390, y, str(dias_trabajados))-12
        y = drawline(c, x +  40, y, 'Regimen Fiscal:')
        y = drawline(c, x + 130, y, cfdi_emisor_node[0].getAttribute('RegimenFiscal'))
        """ FALTAS POR SEMANA | verificar si es por quincena o semanal """
        y = drawline(c, x + 300, y, 'Faltas:')
        y = drawline(c, x + 390, y, str(dias_pagados - 7))-12
    else:
        y = drawrect(c, x, y, 590, 20, True, 0)
        y = drawtittle(c, x + 5, y + 6, 'DATOS DE CLIENTE')
        y = drawline(c, x +  40, y, 'Nombre:')
        y = drawline(c, x + 180, y, cfdi_receptor_node[0].getAttribute('Nombre'))-12
        y = drawline(c, x +  40, y, 'RFC:')
        y = drawline(c, x + 180, y, cfdi_receptor_node[0].getAttribute('Rfc'))-12
        y = drawline(c, x +  40, y, 'Domicilio Fiscal:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('LugarExpedicion'))-12
        y = drawline(c, x +  40, y, 'Regimen Fiscal:')
        y = drawline(c, x + 180, y, cfdi_emisor_node[0].getAttribute('RegimenFiscal'))-12
    
    # construction of the section that contains the cfdi data
    y = drawrect(c, x, y-18, 590, 20, True, 0)
    y = drawtittle(c, x+5, y + 6, 'DATOS DEL CFDI')
    if cfdi_tipo == 'N':
        """ REVISAR QUE CONTENGA FOLIO """
        y = drawline(c, x +  40, y, 'Folio:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('Folio'))-12
        y = drawline(c, x +  40, y, 'Fecha y hora de emisión:')
        y = drawline(c, x + 180, y, cfdi_nomina_node[0].getAttribute('FechaInicialPago'))-12
        y = drawline(c, x +  40, y, 'Fecha y hora de certificación:')
        y = drawline(c, x + 180, y, cfdi_timbre_node[0].getAttribute('FechaTimbrado'))-12
        y = drawline(c, x +  40, y, 'Uso CFDI:')
        y = drawline(c, x + 180, y, cfdi_receptor_node[0].getAttribute('UsoCFDI'))-12
        y = drawline(c, x +  40, y, 'Forma de Pago:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('FormaPago'))-12
        y = drawline(c, x +  40, y, 'Metodo de Pago:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('MetodoPago'))-12
        y = drawline(c, x +  40, y, 'Tipo de comprobante:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('TipoDeComprobante'))-12
    else:
        y = drawline(c, x +  40, y, 'Folio:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('Folio'))-12
        y = drawline(c, x +  40, y, 'Fecha y hora de emisión:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('Fecha'))-12
        y = drawline(c, x +  40, y, 'Fecha y hora de certificación:')
        y = drawline(c, x + 180, y, cfdi_timbre_node[0].getAttribute('FechaTimbrado'))-12
        y = drawline(c, x +  40, y, 'Uso CFDI:')
        y = drawline(c, x + 180, y, cfdi_receptor_node[0].getAttribute('UsoCFDI'))-12
        if cfdi_tipo == 'P':
            y = drawline(c, x +  40, y, 'Metodo de Pago:')
            y = drawline(c, x + 180, y, 'N/A')-12
            y = drawline(c, x +  40, y, 'Forma de Pago:')
            y = drawline(c, x + 180, y, 'N/A')-12
        else:
            y = drawline(c, x +  40, y, 'Metodo de Pago:')
            y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('MetodoPago'))-12
            y = drawline(c, x +  40, y, 'Forma de Pago:')
            y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('FormaPago'))-12
        y = drawline(c, x +  40, y, 'Tipo de comprobante:')
        y = drawline(c, x + 180, y, cfdi_comprobante_node[0].getAttribute('TipoDeComprobante'))-12

    # draw the relations to documents after generating the array containing the table
    y = drawrect(c, x, y-18, 590, 20, True, 0)
    y = drawtittle(c, x + 5, y + 6, 'CFDI relacionado')
    if cfdi_relacionados_node and cfdi_document_node:
        y = drawline(c, x +  40, y, 'Tipo relación:')
        y = drawline(c, x + 180, y, cfdi_relacionados_node[0].getAttribute('TipoRelacion'))-12
        y = drawline(c, x +  40, y, 'CFDI relación:')
        y = drawline(c, x + 180, y, cfdi_document_node[0].getAttribute('UUID'))-12
    elif cfdi_related_node:
        # draw the CFDI relationship list after generating the matrix containing the table
        related_rows = get_related_cfdi_table(cfdi_related_node, row_related_node)
        # draw the table at position (x, y)
        y = draw_related_table(c, related_rows, x, y-12)-12
    else: 
        y = drawline(c, x +  40, y, 'Tipo relación:')
        y = drawline(c, x + 180, y, 'N/A')-12
        y = drawline(c, x +  40, y, 'CFDI relación:')
        y = drawline(c, x + 180, y, 'N/A')-12

    # draw the invoice or payroll concepts after generating the array that contains the table
    concepts_rows = get_cfdi_concepts_table(cfdi_comprobante_node, cfdi_conceptos_node)
    
    # draw the table at position (x, y)
    y = draw_concept_table(c, concepts_rows, x, y-12, cfdi_tipo)
    y = drawrect(c, x, y-12, 590, 1, True, 0)-12

    # totals table annex, quantity segment with letter, currency and digital stamps
    y = drawline(c, x, y, 'Cantidad con Letra:')
    y = drawline(c, x + 80, y, amount_with_letter(float(cfdi_comprobante_node[0].getAttribute('Total'))))-12
    
    # defines the link to the verification web page
    url = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?&id=' + getUUID(cfdi_timbre_node) + '&re=' + cfdi_emisor_node[0].getAttribute('Rfc') + '&rr=' + cfdi_receptor_node[0].getAttribute('Rfc') + '&tt=' + cfdi_comprobante_node[0].getAttribute('Total') + '&fe=' + getSELLO(cfdi_comprobante_node)
    
    # 
    y =   drawQR(c, x + 430, y - 150, url) + 150  # 150 defines de heigth position its a standart for the size for this canvas
    y = drawline(c, x      , y      , 'Moneda:')
    y = drawline(c, x +  40, y      , cfdi_comprobante_node[0].getAttribute('Moneda'))-12
    y = drawline(c, x      , y      , 'No de Serie del Certificado del SAT:')
    y = drawline(c, x + 150, y      , cfdi_comprobante_node[0].getAttribute('NoCertificado'))-12
    
    # segment that converts the Digital Stamps with paragraph style
    style_digitalstamp  = ParagraphStyle(name='CustomStyle', fontSize=6, leading=6)
    sello_cfdi          = Paragraph(cfdi_comprobante_node[0].getAttribute('Sello'), style_digitalstamp)
    sello_sat           = Paragraph(cfdi_timbre_node[0].getAttribute('SelloSAT'), style_digitalstamp)
    
    # draw the digital stamps object on the canvas 
    y = drawline(c, x, y-12, 'Sello Digital del CFDI:')-27
    sello_cfdi.wrapOn(c,  400, inch)
    sello_cfdi.drawOn(c, x+10, y)
    y = drawline(c, x, y-12, 'Sello Digital del SAT:')-24
    sello_sat.wrapOn(c,  400, inch)
    sello_sat.drawOn(c, x+10, y)
    y = drawline(c, x, y-12, 'Cadena Original del complemento de certificación digital del SAT:')-24
    sello_sat.wrapOn(c,  400, inch)
    sello_sat.drawOn(c, x+10, y)

    # save canvas to pdf
    try:
        c.save()
        print(f'{pdfname}: Saved')
    except Exception as e:
        print(f'E1: Impossible to save the PFD: {pdfname}')
        pass

def getSELLO(comprobante):
    if comprobante:
        sello = comprobante[0].getAttribute('Sello')
    return sello[-8:]

def getUUID(timbre):
    if timbre:
        uuid = timbre[0].getAttribute('UUID')
    return str(uuid)

# iterate over each XML file in the directory and subdirectories
def filenames(directory):
    for root, dirs, files in os.walk(directory):
        if "Errors" in dirs:
            dirs.remove("Errors")
        for file in files:
            if file.endswith('.xml'):
                yield os.path.join(root, file)

def generate_pdf(rfc):
    dir = f'{rfc}/Reportes PDF'
    # create the main folder "Reportes PDF" if it does not exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    for filename in filenames(rfc):
        # get the path of the directory containing the xml file
        xml_dir = os.path.dirname(filename)
        # create the same subdirectory structure in the "RFC_Municipio" folder
        pdf_dir = os.path.join(dir, xml_dir)
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        # generate the pdf file inside the corresponding folder
        pdf_file = os.path.join(pdf_dir, os.path.basename(filename).replace('.xml', '.pdf'))
        try: 
            canvas_pdf_parser(filename, pdf_file)
        except Exception as e:
            print(f'E1: Impossible to parse the tree: {filename}')
            continue

# Main script code
if __name__ == '__main__':
    # Code that is executed when the script is called directly
    generate_pdf('MCM8501012U0')
    pass