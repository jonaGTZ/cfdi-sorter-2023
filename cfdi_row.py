# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [05/10/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import json
from lxml import etree

def type_receipt_with_letter(type_recipt):
    type_recipt_list = {
        'I':'Ingreso',
        'N':'Nomina',
        'E':'Egreso',
        'P':'Pago'
    }
    return type_recipt_list.get(type_recipt)

def cfdi_row(nodo, fila):
    # Add "cfdi:Comprobante" node as new column
    if nodo.tag.endswith('Comprobante'):
        fila['Serie']               = nodo.attrib.get('Serie'              , '')
        fila['Folio']               = nodo.attrib.get('Folio'              , '')
        fila['Subtotal']            = nodo.attrib.get('SubTotal'           , '')
        fila['Descuento']           = nodo.attrib.get('Descuento'          , '')
        fila['Tipo de Cambio']      = nodo.attrib.get('TipoCambio'         , '')
        fila['Version']             = nodo.attrib.get('Version'            , '')
        fila['Fecha Emision']       = nodo.attrib.get('Fecha'              , '')
        fila['Tipo Comprobante']    = nodo.attrib.get('TipoDeComprobante'  , '')
        fila['Subtotal']            = nodo.attrib.get('SubTotal'           , '')
        fila['Total']               = nodo.attrib.get('Total'              , '')
        fila['Moneda']              = nodo.attrib.get('Moneda'             , '')
        fila['CP Emisor']           = nodo.attrib.get('LugarExpedicion'    , '')
        fila['Moneda']              = nodo.attrib.get('Moneda'             , '')
        fila['Metodo Pago']         = nodo.attrib.get('MetodoPago'         , '')
        fila['Forma Pago']          = nodo.attrib.get('FormaPago'          , '')
        fila['Tipo']                = type_receipt_with_letter(nodo.attrib.get('TipoDeComprobante'))
        fila['Sello']               = nodo.attrib.get('Sello'              , '')
        fila['No Certificado']      = nodo.attrib.get('NoCertificado'      , '')
        fila['Certificado']         = nodo.attrib.get('Certificado'        , '')
        fila['Condiciones Pago']    = nodo.attrib.get('CondicionesDePago'  , '')
    
    # Add "cfdi:InformacionGlobal" attribs as new row
    if nodo.tag.endswith('InformacionGlobal'):
        fila['Periodicidad_Global'] = nodo.attrib.get('Periodicidad', '')
        fila['Meses_Global']        = nodo.attrib.get('Meses', '')
        fila['Año_Global']          = nodo.attrib.get('Año', '')

    # Add "cfdi:CfdiRelacionados" attribs as new row
    if nodo.tag.endswith('CfdiRelacionados'):
        fila['Tipo Relacion']    = nodo.attrib.get('TipoRelacion', '')
    
    # Add "cfdi:CfdiRelacionado" attribs as new row
    if nodo.tag.endswith('CfdiRelacionado'):
        fila['UUID Relacion']    = nodo.attrib.get('UUID', '')
        
    if nodo.tag.endswith('Emisor'):
        fila['RFC Emisor']              = nodo.attrib.get('Rfc'             , '')
        fila['Nombre Emisor']           = nodo.attrib.get('Nombre'          , '')
        fila['Regimen Fiscal Emisor']   = nodo.attrib.get('RegimenFiscal'   , '')

    # Add "cfdi:Receptor" attribs as new row
    if nodo.tag.endswith('Receptor'):
        fila['RFC Receptor']            = nodo.attrib.get('Rfc'                     , '')
        fila['Nombre Receptor']         = nodo.attrib.get('Nombre'                  , '')
        fila['CP Receptor']             = nodo.attrib.get('DomicilioFiscalReceptor' , '')
        fila['Regimen Fiscal Receptor'] = nodo.attrib.get('RegimenFiscalReceptor'   , '')
        fila['Uso CFDI']                = nodo.attrib.get('UsoCFDI'                 , '')

    if nodo.tag.endswith('Conceptos'):
        # Create an empty dictionary to store the concept data
        lista_conceptos = []

        conceptos = nodo.xpath('//cfdi:Conceptos/cfdi:Concepto', namespaces=nodo.nsmap)
        # Iterate over the cfdi:Concept elements and add their data to the dictionary
        for concepto in conceptos:
            datos_concepto = {
                'ClaveProdServ'     : concepto.get('ClaveProdServ'   , ''),
                'NoIdentificacion'  : concepto.get('NoIdentificacion', ''),
                'Cantidad'          : concepto.get('Cantidad'        , ''),
                'Clave Unidad'      : concepto.get('ClaveUnidad'     , ''),
                'Unidad'            : concepto.get('Unidad'          , ''),
                'Descripcion'       : concepto.get('Descripcion'     , ''),
                'Valor Unitario'    : concepto.get('ValorUnitario'   , ''),
                'Importe'           : concepto.get('Importe'         , ''),
                'Descuento'         : concepto.get('Descuento'       , '')
            }
            lista_conceptos.append(datos_concepto)
        # Add the list of concepts to the main dictionary
        fila['Lista de Conceptos']  = json.dumps(lista_conceptos)
        fila['Objeto Impuesto']     = concepto.get('ObjetoImp', '')
    
    # Add "cfdi:InformacionAduanera" attribs as new row
    if nodo.tag.endswith('InformacionAduanera'):
        fila['Numero Pedimento']   = nodo.attrib.get('NumeroPedimento', '')

    # Add "leyendasFisc:Leyenda" attribs as new row
    if nodo.tag.endswith('Leyenda'):
        fila['Leyenda']   = nodo.attrib.get('textoLeyenda', '')

    # Add "implocal:ImpuestosLocales" attribs as new row
    if nodo.tag.endswith('ImpuestosLocales'):
        fila['Total Retenciones Locales']   = nodo.attrib.get('TotaldeRetenciones', '')
        fila['Total Traslados']             = nodo.attrib.get('TotaldeTraslados', '')

    # Add "cfdi:TimbreFiscalDigital" attribs as new row 
    if nodo.tag.endswith('Impuestos'):
        fila['Total Imp Retenidos']     = nodo.attrib.get('TotalImpuestosRetenidos', '')
        fila['Total Imp Trasladados']   = nodo.attrib.get('TotalImpuestosTrasladados', '')

    # Add "cfdi:TimbreFiscalDigital" attribs as new row
    if nodo.tag.endswith('TimbreFiscalDigital'):
        fila['Fecha Timbrado']  = nodo.attrib.get('FechaTimbrado', '')
        fila['UUID']            = nodo.attrib.get('UUID', '')
    
    # Add "cfdi:TimbreFiscalDigital" attribs as new row
    if nodo.tag.endswith('Pago'):
        # Create an empty dictionary to store the payment data
        payment_list = []

        # set payment namespace for CFDI version
        if nodo.attrib.get('Version') == '4.0':
            paynamespace = 'pago20:'
        else:
             paynamespace = 'pago10:'

        payments = nodo.xpath(f'//{paynamespace}Pago/{paynamespace}DoctoRelacionado', namespaces=nodo.nsmap)
        
        # Iterate over the cfdi:Concept elements and add their data to the dictionary 
        for payment in payments:
            payment_data = {
                'UUID Relacionado'  : payment.get('IdDocumento'         , ''),
                'Serie Relac'       : payment.get('Serie'               , ''),
                'Folio Relac'       : payment.get('Folio'               , ''),
                'NumParcialidad'    : payment.get('NumParcialidad'      , ''),
                'Saldo Anterior'    : payment.get('ImpSaldoAnt'         , ''),
                'Importe Pagado'    : payment.get('ImpPagado'           , ''),
                'Por Pagar'  : payment.get('ImpSaldoInsoluto'    , '')
            }
            payment_list.append(payment_data)
            
        fila['Lista de Pagos']      = json.dumps(payment_list)
        fila['Fecha Pago']          = nodo.attrib.get('FechaPago'   , '')
        fila['Moneda Pago']         = nodo.attrib.get('MonedaP'     , '')
        fila['Tipo Cambio']         = nodo.attrib.get('TipoCambioP' , '')
        fila['Monto UUID Relac']    = nodo.attrib.get('Monto' , '')

    # Add "cfdi:TimbreFiscalDigital" attribs as new row
    if nodo.tag.endswith('TrasladoDR'):
        fila['Objeto Impuesto_DR']      = nodo.attrib.get(''            , '')
        fila['Importe Impuesto 16%_DR'] = nodo.attrib.get('ImporteDR'   , '')

    return fila