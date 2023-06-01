# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [05/10/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import json
from set_sat_status import set_sat_status
from lxml import etree

def type_receipt_with_letter(type_recipt):
    type_recipt_list = {
        'I':'Ingreso',
        'E':'Egreso',
        'P':'Pago'
    }
    return type_recipt_list.get(type_recipt)

def cfdi_row(nodo, fila, filename, option, rfc):
    try:
        # Add "cfdi:Comprobante" node as new column
        if nodo.tag.endswith('Comprobante'):
            fila['Version']                 = nodo.attrib.get('Version'            , '')
            fila['Fecha Emision']           = nodo.attrib.get('Fecha'              , '')
            fila['Serie']                   = nodo.attrib.get('Serie'              , '')
            fila['Folio']                   = nodo.attrib.get('Folio'              , '')
            fila['Tipo Comprobante']        = nodo.attrib.get('TipoDeComprobante'  , '')
            fila['Tipo']                    = type_receipt_with_letter(nodo.attrib.get('TipoDeComprobante'))
            fila['Metodo Pago']             = nodo.attrib.get('MetodoPago'         , '')
            fila['Forma Pago']              = nodo.attrib.get('FormaPago'          , '')
            fila['Subtotal']                = nodo.attrib.get('SubTotal'           , '')
            fila['Descuento']               = nodo.attrib.get('Descuento'          , '')
            fila['Total']                   = nodo.attrib.get('Total'              , '')
            fila['Moneda']                  = nodo.attrib.get('Moneda'             , '')
            fila['Tipo de Cambio']          = nodo.attrib.get('TipoCambio'         , '')
            fila['CP Emisor']               = nodo.attrib.get('LugarExpedicion'    , '')
            fila['Moneda']                  = nodo.attrib.get('Moneda'             , '')
            fila['Sello']                   = nodo.attrib.get('Sello'              , '')
            fila['No Certificado']          = nodo.attrib.get('NoCertificado'      , '')
            fila['Certificado']             = nodo.attrib.get('Certificado'        , '')
            fila['Condiciones Pago']        = nodo.attrib.get('CondicionesDePago'  , '')
        
        # Add "cfdi:InformacionGlobal" attribs as new row
        if nodo.tag.endswith('InformacionGlobal'):
            fila['Periodicidad_Global']     = nodo.attrib.get('Periodicidad'       , '')
            fila['Meses_Global']            = nodo.attrib.get('Meses'              , '')
            fila['Año_Global']              = nodo.attrib.get('Año'                , '')

        # Add "cfdi:CfdiRelacionados" attribs as new row
        if nodo.tag.endswith('CfdiRelacionados'):
            fila['Tipo Relacion']           = nodo.attrib.get('TipoRelacion'       , '')
        
        # Add "cfdi:CfdiRelacionado" attribs as new row
        if nodo.tag.endswith('CfdiRelacionado'):
            fila['UUID Relacion']           = nodo.attrib.get('UUID'               , '')
            
        if nodo.tag.endswith('Emisor'):
            fila['RFC Emisor']              = nodo.attrib.get('Rfc'                , '')
            fila['Nombre Emisor']           = nodo.attrib.get('Nombre'             , '')
            fila['Regimen Fiscal Emisor']   = nodo.attrib.get('RegimenFiscal'      , '')

        # Add "cfdi:Receptor" attribs as new row
        if nodo.tag.endswith('Receptor'):
            fila['RFC Receptor']            = nodo.attrib.get('Rfc'                     , '')
            fila['Nombre Receptor']         = nodo.attrib.get('Nombre'                  , '')
            fila['CP Receptor']             = nodo.attrib.get('DomicilioFiscalReceptor' , '')
            fila['Regimen Fiscal Receptor'] = nodo.attrib.get('RegimenFiscalReceptor'   , '')
            fila['Uso CFDI']                = nodo.attrib.get('UsoCFDI'                 , '')

        if nodo.tag.endswith('Conceptos'):
            # Create an empty dictionary to store the concept data
            concept_list = []

            concepts = nodo.xpath('//cfdi:Conceptos/cfdi:Concepto', namespaces=nodo.nsmap)
            # Iterate over the cfdi:Concept elements and add their data to the dictionary
            for concept in concepts:
                concept_data = {
                    'ClaveProdServ'     : concept.get('ClaveProdServ'   , ''),
                    'NoIdentificacion'  : concept.get('NoIdentificacion', ''),
                    'Cantidad'          : concept.get('Cantidad'        , ''),
                    'Clave Unidad'      : concept.get('ClaveUnidad'     , ''),
                    'Unidad'            : concept.get('Unidad'          , ''),
                    'Descripcion'       : concept.get('Descripcion'     , ''),
                    'Valor Unitario'    : concept.get('ValorUnitario'   , ''),
                    'Importe'           : concept.get('Importe'         , ''),
                    'Descuento'         : concept.get('Descuento'       , '')
                }
                concept_list.append(concept_data)
            # Add the list of concepts to the main dictionary
            fila['Lista de Conceptos']      = json.dumps(concept_list, ensure_ascii=False).encode('utf-8')
            fila['Objeto Impuesto']         = nodo.attrib.get('ObjetoImp', '')
        
        # Add "cfdi:InformacionAduanera" attribs as new row
        if nodo.tag.endswith('InformacionAduanera'):
            fila['Numero Pedimento']        = nodo.attrib.get('NumeroPedimento', '')

        # # Add "cfdi:Traslado" attribs as new row
        if nodo.tag.endswith('Traslado'):
            # Create an empty dictionary to store the transfer data
            transfer_list = []

            transfers = nodo.xpath('//cfdi:Traslados/cfdi:Traslado', namespaces=nodo.nsmap)
            
            # Iterate over the cfdi:Traslado elements and add their data to the dictionary
            for transfer in transfers:
                transfer_data = {
                    'Importe'     : transfer.get('Importe'   , ''),
                }
                transfer_list.append(transfer_data)
            # Add the list of concepts to the main dictionary
            fila['Lista de Traslado']       = json.dumps(transfer_list)

        # Add "leyendasFisc:Leyenda" attribs as new row
        if nodo.tag.endswith('Leyenda'):
            fila['Leyenda']                 = nodo.attrib.get('textoLeyenda', '')

        # Add "implocal:ImpuestosLocales" attribs as new row
        if nodo.tag.endswith('ImpuestosLocales'):
            fila['Total Retenciones Locales']   = nodo.attrib.get('TotaldeRetenciones', '')
            fila['Total Traslados']             = nodo.attrib.get('TotaldeTraslados', '')

        # Add "cfdi:Impuestos" attribs as new row 
        if nodo.tag.endswith('Impuestos'):
            fila['Total Imp Retenidos']     = nodo.attrib.get('TotalImpuestosRetenidos', '')
            fila['Total Imp Trasladados']   = nodo.attrib.get('TotalImpuestosTrasladados', '')

        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if nodo.tag.endswith('TimbreFiscalDigital'):
            fila['Fecha Timbrado']          = nodo.attrib.get('FechaTimbrado', '')
            fila['UUID']                    = nodo.attrib.get('UUID', '')
            # call to the data stored in the json generated in the sorter
            estado_sat, fecha_consulta      = set_sat_status(nodo.attrib.get('UUID', ''), option, rfc)
            fila['Estado SAT']              = estado_sat
            fila['Fecha Consulta']          = fecha_consulta
        
        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if nodo.tag.endswith('Pagos'):
            # Create an empty dictionary to store the payment data
            payment_list = []

            try:
                # set payment namespace for CFDI version
                namespace = 'pago10'
                
                if nodo.attrib.get('Version') == '2.0':
                    namespace = 'pago20'

                payments = nodo.xpath(f'//{namespace}:Pago/{namespace}:DoctoRelacionado', namespaces=nodo.nsmap)
            
            except etree.XPathEvalError as e:
                return fila
            
            # Iterate over the cfdi:Concept elements and add their data to the dictionary 
            for payment in payments:
                payment_data = {
                    'UUID Relacionado'  : payment.get('IdDocumento'         , ''),
                    'Serie Relac'       : payment.get('Serie'               , ''),
                    'Folio Relac'       : payment.get('Folio'               , ''),
                    'NumParcialidad'    : payment.get('NumParcialidad'      , ''),
                    'Saldo Anterior'    : payment.get('ImpSaldoAnt'         , ''),
                    'Importe Pagado'    : payment.get('ImpPagado'           , ''),
                    'Por Pagar'         : payment.get('ImpSaldoInsoluto'    , '')
                }
                payment_list.append(payment_data)
                    
                fila['Lista de Pagos']      = json.dumps(payment_list)
            
            fila['Fecha Pago']              = nodo.attrib.get('FechaPago'   , '')
            fila['Moneda Pago']             = nodo.attrib.get('MonedaP'     , '')
            fila['Tipo Cambio']             = nodo.attrib.get('TipoCambioP' , '')
            fila['Monto UUID Relac']        = nodo.attrib.get('Monto' , '')

        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if nodo.tag.endswith('TrasladoDR'):
            fila['Objeto Impuesto_DR']      = nodo.attrib.get('ImporteDR', '')
            fila['Importe Impuesto 16%_DR'] = nodo.attrib.get('ImporteDR', '')
    
    except Exception as e:
            print(f'{e} \nfilename: {filename}')
            pass
    
    return fila