# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [06/02/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import json
import os

from set_sat_status import set_sat_status
from lxml import etree

def type_receipt_with_letter(type_recipt):
    type_recipt_list = {
        'I':'Ingreso',
        'E':'Egreso',
        'P':'Pago',
        'N':'Nómina'
    }
    return type_recipt_list.get(type_recipt)

# set of row names to be mapped by the dictionary named row
option_mapping = {
    'AYUDAS'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "Forma Pago", "Subtotal","Total", "Moneda", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Total Retenciones Locales", "Total Imp Retenidos", "Total Traslados", "Total Imp Trasladados", "Periodicidad_Global", "Meses_Global", "Año_Global", "Sello", "No Certificado", "Certificado", "Leyenda","Addenda", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'INGRESO'       : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "Forma Pago", "Subtotal", "Descuento", "IVA 16%", "Total", "Moneda", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Total Retenciones Locales", "Total Imp Retenidos", "Total Traslados", "Total Imp Trasladados", "Periodicidad_Global", "Meses_Global", "Año_Global", "Sello", "No Certificado", "Certificado", "Leyenda", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'NOMINA'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Forma Pago", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "Subtotal", "Descuento", "ISR", "Total", "Moneda", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Sello", "No Certificado", "Certificado", "Version Nomina", "Tipo Nomina", "Fecha Pago", "Fecha Inicial Pago", "Fecha Final Pago", "Num Dias Pagados", "Total Percepciones", "Total Deducciones", "Total Otros Pagos", "Registro Patronal", "Origen Recursos", "Monto Recursos Propios", "CURP", "Num Seguridad Social", "Fecha Inicial Relac Lab", "Antigüedad", "Tipo Contrato", "Sindicalizado", "Tipo Jornada", "Tipo Regimen", "Num Empleado", "Departamento", "Puesto", "Riesgo Puesto", "Periodicidad Pago", "Banco", "Cuenta Bancaria", "Salario Base Cotiz", "SDI", "Clave Entidad", "Total Sueldos", "Total Separac Indemniz", "Total Jub Pens Retiro", "Importe Horas Extras", "Importe Separac Indemniz", "Total Otras Deducc", "Total Imptos Ret", "Importe Otro Pago", "SPE causado", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'PAGO_E'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Subtotal", "Total", "Moneda", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Sello", "No Certificado", "Certificado", "Fecha Pago", "Forma Pago", "Moneda Pago", "Tipo Cambio", "Monto UUID Relac", "UUID Relacionado", "Lista de Pagos", "Tipo Cambio P", "Serie Relac", "Folio Relac", "Impuesto 16%_Pago", "Num Parcialidad", "Saldo Anterior", "Importe Pagado", "Monto Acum Pagos", "Por Pagar", "Objeto Impuesto_DR", "Importe Impuesto 16%_DR", "Metodo Pago_DR", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'DES_BON_DEV'   : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "Forma Pago", "Subtotal", "IEPS", "IVA 16%", "Retención IVA", "Retención ISR", "Imp Local Retenido", "Tasa Imp Local Retenido", "Importe Imp Local Retenido", "Total", "Moneda", "Tipo Cambio", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Total Retenciones Locales", "Total Imp Retenidos", "Total Traslados", "Total Imp Trasladados", "Periodicidad_Global", "Meses_Global", "Año_Global", "Sello", "No Certificado", "Certificado", "Condiciones Pago", "Leyenda",    "Addenda", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'GASTO'         : ["Estado SAT" ,"Fecha Consulta", "Validacion EFOS" ,"Version" ,"Fecha Emision" ,"Fecha Timbrado" ,"Serie" ,"Folio" ,"UUID" ,"Tipo Comprobante" ,"Tipo" ,"Metodo Pago" ,"Forma Pago" ,"Subtotal", "IEPS" ,"IVA 16%" ,"Retención IVA" ,"Retención ISR" ,"Imp Local Retenido" ,"Tasa Imp Local Retenido" ,"Importe Imp Local Retenido" ,"Total" ,"Moneda" ,"Tipo Cambio" ,"Tipo Relacion" ,"UUID Relacion" ,"CP Emisor" ,"RFC Emisor" ,"Nombre Emisor" ,"Regimen Fiscal Emisor" ,"RFC Receptor" ,"Nombre Receptor" ,"CP Receptor" ,"Regimen Fiscal Receptor" ,"Uso CFDI" ,"Lista de Conceptos" ,"Objeto Impuesto" ,"Total Retenciones Locales" ,"Total Imp Retenidos" ,"Total Traslados" ,"Total Imp Trasladados" ,"Periodicidad_Global" ,"Meses_Global" ,"Año_Global" ,"Sello" ,"No Certificado" ,"Certificado" ,"Condiciones Pago" ,"Leyenda" ,   "Addenda" ,"Archivo XML" ,"Num. Cuenta Contable" ,"Nombre Cuenta Contable" ,"Número CRI/COG" ,"Nombre CRI/COG" ,"Precisiones"],
    'PAGO_R'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Subtotal", "Total", "Moneda", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Sello", "No Certificado", "Certificado", "Fecha Pago", "Forma Pago", "Moneda Pago", "Tipo Cambio", "Monto UUID Relac", "UUID Relacionado", "Lista de Pagos", "Tipo Cambio P", "Serie Relac", "Folio Relac", "Impuesto 16%_Pago", "Num Parcialidad", "Saldo Anterior", "Importe Pagado", "Monto Acum Pagos", "Por Pagar", "Objeto Impuesto_DR", "Importe Impuesto 16%_DR", "Metodo Pago_DR", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"]
}

def cfdi_row_collector(node, row, filename, option, rfc):

    emisor      = ''
    receptor    = ''
    
    if node.tag.endswith('Comprobante'):
        if node.attrib.get('Version') == '4.0':
            emisor      = '{http://www.sat.gob.mx/cfd/4}Emisor'
            receptor    = '{http://www.sat.gob.mx/cfd/4}Receptor'
    
    if option in option_mapping:
        keys_to_add = option_mapping[option]
        for key in keys_to_add:
            if key in row:
                try:
                    # Add "cfdi:Comprobante" node as new column
                    if node.tag.endswith('Comprobante'):
                        row['Version']                     = node.attrib.get('Version'                     , '')
                        row['Fecha Emision']               = node.attrib.get('Fecha'                       , '')
                        row['Serie']                       = node.attrib.get('Serie'                       , '')
                        row['Folio']                       = node.attrib.get('Folio'                       , '')
                        row['Tipo Comprobante']            = node.attrib.get('TipoDeComprobante'           , '')
                        row['Tipo']                        = type_receipt_with_letter(node.attrib.get('TipoDeComprobante'))
                        if not (option == 'PAGO_R' or option == 'PAGO_E'):
                            row['Metodo Pago']             = node.attrib.get('MetodoPago'                  , '')
                        row['Forma Pago']                  = node.attrib.get('FormaPago'                   , '')
                        row['Subtotal']                    = node.attrib.get('SubTotal'                    , '')
                        if not (option == 'GASTO' or option == 'PAGO_R' or option == 'PAGO_E'):
                            row['Descuento']               = node.attrib.get('Descuento'                   , '')

                        row['Total']                       = node.attrib.get('Total'                       , '')
                        row['Moneda']                      = node.attrib.get('Moneda'                      , '')
                        if not (option == 'NOMINA' or option == 'AYUDA' or option == 'INGRESO'):
                            row['Tipo Cambio']             = node.attrib.get('TipoCambio'                  , '')
                        row['CP Emisor']                   = node.attrib.get('LugarExpedicion'             , '')
                        row['Moneda']                      = node.attrib.get('Moneda'                      , '')
                        row['Sello']                       = node.attrib.get('Sello'                       , '')
                        row['No Certificado']              = node.attrib.get('NoCertificado'               , '')
                        row['Certificado']                 = node.attrib.get('Certificado'                 , '')
                        if option == 'DES_BON_DEV' or option == 'GASTO':
                            row['Condiciones Pago']            = node.attrib.get('CondicionesDePago'           , '')
                        
                    
                    # Add "cfdi:InformacionGlobal" attribs as new row
                    if node.tag.endswith('InformacionGlobal'):
                        row['Periodicidad_Global']         = node.attrib.get('Periodicidad'                , '')
                        row['Meses_Global']                = node.attrib.get('Meses'                       , '')
                        row['Año_Global']                  = node.attrib.get('Año'                         , '')

                    # Add "cfdi:CfdiRelacionados" attribs as new row
                    if node.tag.endswith('CfdiRelacionados'):
                        row['Tipo Relacion']               = node.attrib.get('TipoRelacion'                , '')
                    
                    # Add "cfdi:CfdiRelacionado" attribs as new row
                    if node.tag.endswith('CfdiRelacionado'):
                        row['UUID Relacion']               = node.attrib.get('UUID'                        , '')
                    
                    # Add "cfdi:Emisor" attribs as new row
                    if node.tag.endswith('{http://www.sat.gob.mx/cfd/3}Emisor'):
                        row['RFC Emisor']                  = node.attrib.get('Rfc'                         , '')
                        row['Nombre Emisor']               = node.attrib.get('Nombre'                      , '')
                        row['Regimen Fiscal Emisor']       = node.attrib.get('RegimenFiscal'               , '')
                    elif node.tag.endswith('{http://www.sat.gob.mx/cfd/4}Emisor'):
                        row['RFC Emisor']                  = node.attrib.get('Rfc'                         , '')
                        row['Nombre Emisor']               = node.attrib.get('Nombre'                      , '')
                        row['Regimen Fiscal Emisor']       = node.attrib.get('RegimenFiscal'               , '')

                    # Add "cfdi:Receptor" attribs as new row
                    if node.tag.endswith('{http://www.sat.gob.mx/cfd/3}Receptor'):
                        row['RFC Receptor']                = node.attrib.get('Rfc'                         , '')
                        row['Nombre Receptor']             = node.attrib.get('Nombre'                      , '')
                        row['CP Receptor']                 = node.attrib.get('DomicilioFiscalReceptor'     , '')
                        row['Regimen Fiscal Receptor']     = node.attrib.get('RegimenFiscalReceptor'       , '')
                        row['Uso CFDI']                    = node.attrib.get('UsoCFDI'                     , '')
                    elif node.tag.endswith('{http://www.sat.gob.mx/cfd/4}Receptor'):
                        row['RFC Receptor']                = node.attrib.get('Rfc'                         , '')
                        row['Nombre Receptor']             = node.attrib.get('Nombre'                      , '')
                        row['CP Receptor']                 = node.attrib.get('DomicilioFiscalReceptor'     , '')
                        row['Regimen Fiscal Receptor']     = node.attrib.get('RegimenFiscalReceptor'       , '')
                        row['Uso CFDI']                    = node.attrib.get('UsoCFDI'                     , '')

                    # Add "leyendasFisc:Leyenda" attribs as new row
                    if node.tag.endswith('Leyenda'):
                        row['Leyenda']                     = node.attrib.get('textoLeyenda'                , '')

                    # Add "implocal:ImpuestosLocales" attribs as new row
                    if node.tag.endswith('ImpuestosLocales'):
                        # row['Total Retenciones Locales']   = node.attrib.get('TotaldeRetenciones'        , '')
                        # row['Total Traslados']             = node.attrib.get('TotaldeTraslados'          , '')
                        row['Imp Local Retenido']          = node.attrib.get('ImpLocRetenido'              , '')
                        row['Tasa Imp Local Retenido']     = node.attrib.get('TasadeRetencion'             , '')
                        row['Importe Imp Local Retenido']  = node.attrib.get('Importe'                     , '')

                    # Add "cfdi:Impuestos" attribs as new row 
                    if node.tag.endswith('Impuestos'):
                        row['Total Imp Retenidos']         = node.attrib.get('TotalImpuestosRetenidos'     , '')
                        row['Total Imp Trasladados']       = node.attrib.get('TotalImpuestosTrasladados'   , '')

                    # Add "cfdi:TimbreFiscalDigital" attribs as new row
                    if node.tag.endswith('TimbreFiscalDigital'):
                        row['Fecha Timbrado']              = node.attrib.get('FechaTimbrado', '')
                        row['UUID']                        = node.attrib.get('UUID', '')
                        # call to the data stored in the json generated in the sorter
                        estado_sat, fecha_consulta          = set_sat_status(node.attrib.get('UUID', ''), option, rfc)
                        row['Estado SAT']                  = estado_sat
                        row['Fecha Consulta']              = fecha_consulta

                    # Add "cfdi:InformacionAduanera" attribs as new row
                    if node.tag.endswith('InformacionAduanera'):
                        row['Numero Pedimento']            = node.attrib.get('NumeroPedimento'             , '')
                    
                    # Add "nomina12:Nomina" attribs as new row
                    if node.tag.endswith("{http://www.sat.gob.mx/nomina12}Nomina"):
                        row['ISR']                         = node.attrib.get('TotalDeducciones'            , '')
                        row['Version Nomina']              = node.attrib.get('Version '                    , '')
                        row['Tipo Nomina']                 = node.attrib.get('TipoNomina'                  , '')
                        row['Fecha Pago']                  = node.attrib.get('FechaPago'                   , '')
                        row['Fecha Inicial Pago']          = node.attrib.get('FechaInicialPago'            , '')
                        row['Fecha Final Pago']            = node.attrib.get('FechaFinalPago'              , '')
                        row['Num Dias Pagados']            = node.attrib.get('NumDiasPagados'              , '')
                        row['Total Percepciones']          = node.attrib.get('TotalPercepciones'           , '')
                        row['Total Deducciones']           = node.attrib.get('TotalDeducciones'            , '')
                        row['Total Otros Pagos']           = node.attrib.get('TotalOtrosPagos'             , '')
                        row['Fecha Pago']                  = node.attrib.get('FechaPago'                   , '')
                    
                    # Add "nomina12:Emisor" attribs as new row
                    if node.tag.endswith("{http://www.sat.gob.mx/nomina12}Emisor"):
                        row['Registro Patronal']           = node.attrib.get('RegistroPatronal'            , '')    
                        
                    # Add "nomina12:Receptor" attribs as new row
                    if node.tag.endswith("{http://www.sat.gob.mx/nomina12}Receptor"):
                        row['CURP']                        = node.attrib.get('Curp'                        , '')
                        row['Num Seguridad Social']        = node.attrib.get('NumSeguridadSocial'          , '')
                        row['Fecha Inicial Relac Lab']     = node.attrib.get('FechaInicioRelLaboral'       , '')
                        row['Antigüedad']                  = node.attrib.get('Antigüedad'                  , '')
                        row['Tipo Contrato']               = node.attrib.get('TipoContrato'                , '')
                        row['Sindicalizado']               = node.attrib.get('Sindicalizado'               , '')
                        row['Tipo Jornada']                = node.attrib.get('TipoJornada'                 , '')
                        row['Tipo Regimen']                = node.attrib.get('TipoRegimen'                 , '')
                        row['Num Empleado']                = node.attrib.get('NumEmpleado'                 , '')
                        row['Departamento']                = node.attrib.get('Departamento'                , '')
                        row['Puesto']                      = node.attrib.get('Puesto'                      , '')
                        row['Riesgo Puesto']               = node.attrib.get('RiesgoPuesto'                , '')
                        row['Periodicidad Pago']           = node.attrib.get('PeriodicidadPago'            , '')
                        row['Banco']                       = node.attrib.get('Banco'                       , '')
                        row['Cuenta Bancaria']              = node.attrib.get('CuentaBancaria'              , '')
                        row['Salario Base Cotiz']          = node.attrib.get('SalarioBaseCotApor'          , '')
                        row['SDI']                         = node.attrib.get('SalarioDiarioIntegrado'      , '')
                        row['Clave Entidad']               = node.attrib.get('ClaveEntFed'                 , '')

                    # Add "nomina12:EntidadSNCF " attribs as new row
                    if node.tag.endswith("{http://www.sat.gob.mx/nomina12}EntidadSNCF"):
                        row['Origen Recursos']             = node.attrib.get('OrigenRecurso'               , '')
                        row['Monto Recursos Propios']      = node.attrib.get('MontoRecursoPropio'          , '')

                    # Add "nomina12:Percepciones" attribs as new row
                    if node.tag.endswith("{http://www.sat.gob.mx/nomina12}Percepciones"):
                        row['Total Sueldos']               = node.attrib.get('TotalSueldos'                , '')
                        row['Total Separac Indemniz']      = node.attrib.get('TotalSeparacionIndemnizacion', '')
                        row['Total Jub Pens Retiro']       = node.attrib.get('TotalJubilacionPensionRetiro', '')

                    # Add "nomina12:HorasExtra" attribs as new row
                    if node.tag.endswith("http://www.sat.gob.mx/nomina12}HorasExtra"):
                        row['Importe Horas Extras']        = node.attrib.get('ImportePagado'               , '')
                    
                    # Add "nomina12:SeparacionIndemnizacion" attribs as new row
                    if node.tag.endswith("http://www.sat.gob.mx/nomina12}SeparacionIndemnizacion"):
                        row['Importe Separac Indemniz']    = node.attrib.get('TotalPagado'                 , '')

                    # Add "nomina12:Deducciones" attribs as new row
                    if node.tag.endswith("http://www.sat.gob.mx/nomina12}Deducciones"):
                        row['Total Otras Deducc']          = node.attrib.get('TotalOtrasDeducciones'       , '')
                        row['Total Imptos Ret']            = node.attrib.get('TotalImpuestosRetenidos'     , '')

                    # Add "nomina12:OtroPago" attribs as new row
                    if node.tag.endswith("http://www.sat.gob.mx/nomina12}OtroPago"):
                        row['Importe Otro Pago']           = node.attrib.get('Importe'                     , '')

                    # Add "nomina12:SubsidioAlEmpleo" attribs as new row
                    if node.tag.endswith("http://www.sat.gob.mx/nomina12}SubsidioAlEmpleo"):
                        row['SPE causado']                 = node.attrib.get('SubsidioCausado'             , '')
                    
                    # Add "cfdi:TimbreFiscalDigital" attribs as new row
                    if node.tag.endswith('TrasladoDR'):
                        row['Objeto Impuesto_DR']          = node.attrib.get('ImporteDR', '')
                        row['Importe Impuesto 16%_DR']     = node.attrib.get('ImporteDR', '')

                    if node.tag.endswith('Conceptos'):
                        # Create an empty dictionary to store the concept data, set child node to parse 
                        concept_list = []
                        concepts = node.xpath('//cfdi:Conceptos/cfdi:Concepto', namespaces=node.nsmap)
                        
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
                            concept_list.append(json.loads(json.dumps(concept_data, ensure_ascii=False)))

                        # Add the list of concepts to the main dictionary
                        row['Lista de Conceptos']          = json.dumps(concept_list, ensure_ascii=False)
                        row['Objeto Impuesto']             = node.attrib.get('ObjetoImp', '')

                    # Add "cfdi:Retenciones" attribs as new row
                    if node.tag.endswith('Retenciones'):
                        # set child node to parse 
                        transfers = node.xpath('//cfdi:Retenciones/cfdi:Retencion', namespaces=node.nsmap)

                        # Iterate over the cfdi:Retenciones elements and add their data to the dictionary
                        for transfer in transfers:
                            if   transfer.get('Impuesto') == "001":
                                row['Retención ISR']             = node.attrib.get('Importe', '')

                            elif transfer.get('Impuesto') == "002":
                                row['Retención IVA']             = node.attrib.get('Importe', '')

                            elif transfer.get('Impuesto') == "003":
                                row['Retención IEPS']             = node.attrib.get('Importe', '')

                    # Add "cfdi:Traslado" attribs as new row 
                    # subnode on "cfdi:Impuestos"
                    if node.tag.endswith('Traslado'):
                        # set child node to parse 
                        transfers = node.xpath('//cfdi:Traslados/cfdi:Traslado', namespaces=node.nsmap)
                        
                        # Iterate over the cfdi:Traslado elements and add their data to the dictionary
                        for transfer in transfers:
                            if   transfer.get('Impuesto') == "001":
                                row['ISR']      = node.attrib.get('Importe', '')

                            elif transfer.get('Impuesto') == "002":
                                row['IVA 16%']  = node.attrib.get('Importe', '')

                            elif transfer.get('Impuesto') == "003":
                                row['IEPS']     = node.attrib.get('Importe', '')
                    
                    # Add "cfdi:Pagos" attribs as new row
                    if node.tag.endswith('Pagos'):
                        # Create an empty dictionary to store the payment data
                        payment_list = []
                        
                        # set child node to parse with namespace
                        try:
                            # set payment namespace for CFDI version
                            namespace = 'pago10'
                            if node.attrib.get('Version') == '2.0':
                                namespace = 'pago20'

                            payments = node.xpath(f'//{namespace}:Pago/{namespace}:DoctoRelacionado', namespaces=node.nsmap)
                        
                        except etree.XPathEvalError as e:
                            return row
                        
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
                            payment_list.append(json.loads(json.dumps(payment_data, ensure_ascii=False)))

                        row['Lista de Pagos']              = json.dumps(payment_list, ensure_ascii=False)
                        row['Fecha Pago']                  = node.attrib.get('FechaPago'        , '')
                        row['Moneda Pago']                 = node.attrib.get('MonedaP'          , '')
                        if not (option == 'PAGO_R' or option == 'PAGO_E'):
                            row['Tipo Cambio P']                 = node.attrib.get('TipoCambioP'    , '')
                        row['Monto UUID Relac']            = node.attrib.get('Monto'            , '')

                # understand that the exception that is handled is for cases where fila[row name] does not exist
                except Exception as e:
                    continue
            break
    else:
        raise Exception(f'{e} \nfilename: {filename}')
    
    # returns the matrix with the rows and their respective information
    return row