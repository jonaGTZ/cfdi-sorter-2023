# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [06/02/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import json
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

option_mapping = {
    'AYUDAS'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "Forma Pago", "Subtotal","Total", "Moneda", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Total Retenciones Locales", "Total Imp Retenidos", "Total Traslados", "Total Imp Trasladados", "Periodicidad_Global", "Meses_Global", "Año_Global", "Sello", "No Certificado", "Certificado", "Leyenda","Addenda", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'INGRESO'       : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "Forma Pago", "Subtotal", "Descuento", "IVA 16%", "Total", "Moneda", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Total Retenciones Locales", "Total Imp Retenidos", "Total Traslados", "Total Imp Trasladados", "Periodicidad_Global", "Meses_Global", "Año_Global", "Sello", "No Certificado", "Certificado", "Leyenda", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'NOMINA'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "SubTotal", "Descuento", "ISR", "Total", "Moneda", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Sello", "No Certificado", "Certificado", "Version Nomina", "Tipo Nomina", "Fecha Pago", "Fecha Inicial Pago", "Fecha Final Pago", "Num Dias Pagados", "Total Percepciones", "Total Deducciones", "Total Otros Pagos", "Registro Patronal", "Origen Recursos", "Monto Recursos Propios", "CURP", "Num Seguridad Social", "Fecha Inicial Relac Lab", "Antigüedad", "Tipo Contrato", "Sindicalizado", "Tipo Jornada", "Tipo Regimen", "Num Empleado", "Departamento", "Puesto", "Riesgo Puesto", "Periodicidad Pago", "Banco", "Cuenta Bancaria", "Salario Base Cotiz", "SDI", "Clave Entidad", "Total Sueldos", "Total Separac Indemniz", "Total Jub Pens Retiro", "Importe Horas Extras", "Importe Separac Indemniz", "Total Otras Deducc", "Total Imptos Ret", "Importe Otro Pago", "SPE causado", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'PAGO_E'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Subtotal", "Total", "Moneda", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Sello", "No Certificado", "Certificado", "Fecha Pago", "Forma Pago", "Moneda Pago", "Tipo Cambio", "Monto UUID Relac", "UUID Relacionado", "Lista de Pagos", "Serie Relac", "Folio Relac", "Impuesto 16%_Pago", "Num Parcialidad", "Saldo Anterior", "Importe Pagado", "Monto Acum Pagos", "Por Pagar", "Objeto Impuesto_DR", "Importe Impuesto 16%_DR", "Metodo Pago_DR", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'DES_BON_DEV'   : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Metodo Pago", "Forma Pago", "Subtotal",    "Lista de Traslado", "IEPS", "IVA 16%", "Retención IVA", "Retención ISR", "Imp Local Retenido", "Tasa Imp Local Retenido", "Importe Imp Local Retenido", "Total", "Moneda", "Tipo Cambio", "Tipo Relacion", "UUID Relacion", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Total Retenciones Locales", "Total Imp Retenidos", "Total Traslados", "Total Imp Trasladados", "Periodicidad_Global", "Meses_Global", "Año_Global", "Sello", "No Certificado", "Certificado", "Condiciones Pago", "Leyenda",    "Addenda", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"],
    'GASTO'         : ["Estado SAT" ,"Fecha Consulta", "Validacion EFOS" ,"Version" ,"Fecha Emision" ,"Fecha Timbrado" ,"Serie" ,"Folio" ,"UUID" ,"Tipo Comprobante" ,"Tipo" ,"Metodo Pago" ,"Forma Pago" ,"Subtotal" ,   "Lista de Traslado" ,"IEPS" ,"IVA 16%" ,"Retención IVA" ,"Retención ISR" ,"Imp Local Retenido" ,"Tasa Imp Local Retenido" ,"Importe Imp Local Retenido" ,"Total" ,"Moneda" ,"Tipo Cambio" ,"Tipo Relacion" ,"UUID Relacion" ,"CP Emisor" ,"RFC Emisor" ,"Nombre Emisor" ,"Regimen Fiscal Emisor" ,"RFC Receptor" ,"Nombre Receptor" ,"CP Receptor" ,"Regimen Fiscal Receptor" ,"Uso CFDI" ,"Lista de Conceptos" ,"Objeto Impuesto" ,"Total Retenciones Locales" ,"Total Imp Retenidos" ,"Total Traslados" ,"Total Imp Trasladados" ,"Periodicidad_Global" ,"Meses_Global" ,"Año_Global" ,"Sello" ,"No Certificado" ,"Certificado" ,"Condiciones Pago" ,"Leyenda" ,   "Addenda" ,"Archivo XML" ,"Num. Cuenta Contable" ,"Nombre Cuenta Contable" ,"Número CRI/COG" ,"Nombre CRI/COG" ,"Precisiones"],
    'PAGO_R'        : ["Estado SAT", "Fecha Consulta", "Version", "Fecha Emision", "Fecha Timbrado", "Serie", "Folio", "UUID", "Tipo Comprobante", "Tipo", "Subtotal", "Total", "Moneda", "CP Emisor", "RFC Emisor", "Nombre Emisor", "Regimen Fiscal Emisor", "RFC Receptor", "Nombre Receptor", "CP Receptor", "Regimen Fiscal Receptor", "Uso CFDI", "Lista de Conceptos", "Objeto Impuesto", "Sello", "No Certificado", "Certificado", "Fecha Pago", "Forma Pago", "Moneda Pago", "Tipo Cambio", "Monto UUID Relac", "UUID Relacionado", "Lista de Pagos", "Serie Relac", "Folio Relac", "Impuesto 16%_Pago", "Num Parcialidad", "Saldo Anterior", "Importe Pagado", "Monto Acum Pagos", "Por Pagar", "Objeto Impuesto_DR", "Importe Impuesto 16%_DR", "Metodo Pago_DR", "Archivo XML", "Num. Cuenta Contable", "Nombre Cuenta Contable", "Número CRI/COG", "Nombre CRI/COG", "Precisiones"]
}

def cfdi_row_collector(nodo, fila, filename, option, rfc):
    if option in option_mapping:
        keys_to_add = option_mapping[option]
        for key in keys_to_add:
            if key in fila:
                try:
                    emisor      = '{http://www.sat.gob.mx/cfd/3}Emisor'
                    receptor    = '{http://www.sat.gob.mx/cfd/3}Receptor'
                    # Add "cfdi:Comprobante" node as new column
                    if nodo.tag.endswith('Comprobante'):
                        fila['Version']                     = nodo.attrib.get('Version'                     , '')
                        fila['Fecha Emision']               = nodo.attrib.get('Fecha'                       , '')
                        fila['Serie']                       = nodo.attrib.get('Serie'                       , '')
                        fila['Folio']                       = nodo.attrib.get('Folio'                       , '')
                        fila['Tipo Comprobante']            = nodo.attrib.get('TipoDeComprobante'           , '')
                        fila['Tipo']                        = type_receipt_with_letter(nodo.attrib.get('TipoDeComprobante'))
                        fila['Metodo Pago']                 = nodo.attrib.get('MetodoPago'                  , '')
                        fila['Forma Pago']                  = nodo.attrib.get('FormaPago'                   , '')
                        fila['Subtotal']                    = nodo.attrib.get('SubTotal'                    , '')
                        fila['Descuento']                   = nodo.attrib.get('Descuento'                   , '')
                        fila['Total']                       = nodo.attrib.get('Total'                       , '')
                        fila['Moneda']                      = nodo.attrib.get('Moneda'                      , '')
                        fila['Tipo de Cambio']              = nodo.attrib.get('TipoCambio'                  , '')
                        fila['CP Emisor']                   = nodo.attrib.get('LugarExpedicion'             , '')
                        fila['Moneda']                      = nodo.attrib.get('Moneda'                      , '')
                        fila['Sello']                       = nodo.attrib.get('Sello'                       , '')
                        fila['No Certificado']              = nodo.attrib.get('NoCertificado'               , '')
                        fila['Certificado']                 = nodo.attrib.get('Certificado'                 , '')
                        fila['Condiciones Pago']            = nodo.attrib.get('CondicionesDePago'           , '')
                        if nodo.attrib.get('Version') == '4.0':
                            emisor      = '{http://www.sat.gob.mx/cfd/4}Emisor'
                            receptor    = '{http://www.sat.gob.mx/cfd/4}Receptor'
                    
                    # Add "cfdi:InformacionGlobal" attribs as new row
                    if nodo.tag.endswith('InformacionGlobal'):
                        fila['Periodicidad_Global']         = nodo.attrib.get('Periodicidad'                , '')
                        fila['Meses_Global']                = nodo.attrib.get('Meses'                       , '')
                        fila['Año_Global']                  = nodo.attrib.get('Año'                         , '')

                    # Add "cfdi:CfdiRelacionados" attribs as new row
                    if nodo.tag.endswith('CfdiRelacionados') and 'Tipo Relacion' in fila:
                        fila['Tipo Relacion']               = nodo.attrib.get('TipoRelacion'                , '')
                    
                    # Add "cfdi:CfdiRelacionado" attribs as new row
                    if nodo.tag.endswith('CfdiRelacionado') and 'UUID Relacion' in fila:
                        fila['UUID Relacion']               = nodo.attrib.get('UUID'                        , '')
                        
                    if nodo.tag.endswith(f'{emisor}'):
                        fila['RFC Emisor']                  = nodo.attrib.get('Rfc'                         , '')
                        fila['Nombre Emisor']               = nodo.attrib.get('Nombre'                      , '')
                        fila['Regimen Fiscal Emisor']       = nodo.attrib.get('RegimenFiscal'               , '')

                    # Add "cfdi:Receptor" attribs as new row
                    if nodo.tag.endswith(f'{receptor}'):
                        fila['RFC Receptor']                = nodo.attrib.get('Rfc'                         , '')
                        fila['Nombre Receptor']             = nodo.attrib.get('Nombre'                      , '')
                        fila['CP Receptor']                 = nodo.attrib.get('DomicilioFiscalReceptor'     , '')
                        fila['Regimen Fiscal Receptor']     = nodo.attrib.get('RegimenFiscalReceptor'       , '')
                        fila['Uso CFDI']                    = nodo.attrib.get('UsoCFDI'                     , '')
                    
                    # Add "leyendasFisc:Leyenda" attribs as new row
                    if nodo.tag.endswith('Leyenda'):
                        fila['Leyenda']                     = nodo.attrib.get('textoLeyenda'                , '')

                    # Add "implocal:ImpuestosLocales" attribs as new row
                    if nodo.tag.endswith('ImpuestosLocales'):
                        fila['Total Retenciones Locales']   = nodo.attrib.get('TotaldeRetenciones'          , '')
                        fila['Total Traslados']             = nodo.attrib.get('TotaldeTraslados'            , '')

                    # Add "cfdi:Impuestos" attribs as new row 
                    if nodo.tag.endswith('Impuestos'):
                        fila['Total Imp Retenidos']         = nodo.attrib.get('TotalImpuestosRetenidos'     , '')
                        fila['Total Imp Trasladados']       = nodo.attrib.get('TotalImpuestosTrasladados'   , '')

                    # Add "cfdi:TimbreFiscalDigital" attribs as new row
                    if nodo.tag.endswith('TimbreFiscalDigital'):
                        fila['Fecha Timbrado']              = nodo.attrib.get('FechaTimbrado', '')
                        fila['UUID']                        = nodo.attrib.get('UUID', '')
                        # call to the data stored in the json generated in the sorter
                        estado_sat, fecha_consulta          = set_sat_status(nodo.attrib.get('UUID', ''), option, rfc)
                        fila['Estado SAT']                  = estado_sat
                        fila['Fecha Consulta']              = fecha_consulta

                    # Add "cfdi:InformacionAduanera" attribs as new row
                    if nodo.tag.endswith('InformacionAduanera'):
                        fila['Numero Pedimento']            = nodo.attrib.get('NumeroPedimento'             , '')
                    
                    # Add "nomina12:Nomina" attribs as new row
                    if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Nomina"):
                        fila['ISR']                         = nodo.attrib.get('TotalDeducciones'            , '')
                        fila['Version Nomina']              = nodo.attrib.get('Version '                    , '')
                        fila['Tipo Nomina']                 = nodo.attrib.get('TipoNomina'                  , '')
                        fila['Fecha Pago']                  = nodo.attrib.get('FechaPago'                   , '')
                        fila['Fecha Inicial Pago']          = nodo.attrib.get('FechaInicialPago'            , '')
                        fila['Fecha Final Pago']            = nodo.attrib.get('FechaFinalPago'              , '')
                        fila['Num Dias Pagados']            = nodo.attrib.get('NumDiasPagados'              , '')
                        fila['Total Percepciones']          = nodo.attrib.get('TotalPercepciones'           , '')
                        fila['Total Deducciones']           = nodo.attrib.get('TotalDeducciones'            , '')
                        fila['Total Otros Pagos']           = nodo.attrib.get('TotalOtrosPagos'             , '')
                        fila['Fecha Pago']                  = nodo.attrib.get('FechaPago'                   , '')
                    
                    # Add "nomina12:Emisor" attribs as new row
                    if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Emisor"):
                        fila['Registro Patronal']           = nodo.attrib.get('RegistroPatronal'            , '')    
                        
                    # Add "nomina12:Receptor" attribs as new row
                    if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Receptor"):
                        fila['CURP']                        = nodo.attrib.get('Curp'                        , '')
                        fila['Num Seguridad Social']        = nodo.attrib.get('NumSeguridadSocial'          , '')
                        fila['Fecha Inicial Relac Lab']     = nodo.attrib.get('FechaInicioRelLaboral'       , '')
                        fila['Antigüedad']                  = nodo.attrib.get('Antigüedad'                  , '')
                        fila['Tipo Contrato']               = nodo.attrib.get('TipoContrato'                , '')
                        fila['Sindicalizado']               = nodo.attrib.get('Sindicalizado'               , '')
                        fila['Tipo Jornada']                = nodo.attrib.get('TipoJornada'                 , '')
                        fila['Tipo Regimen']                = nodo.attrib.get('TipoRegimen'                 , '')
                        fila['Num Empleado']                = nodo.attrib.get('NumEmpleado'                 , '')
                        fila['Departamento']                = nodo.attrib.get('Departamento'                , '')
                        fila['Puesto']                      = nodo.attrib.get('Puesto'                      , '')
                        fila['Riesgo Puesto']               = nodo.attrib.get('RiesgoPuesto'                , '')
                        fila['Periodicidad Pago']           = nodo.attrib.get('PeriodicidadPago'            , '')
                        fila['Banco']                       = nodo.attrib.get('Banco'                       , '')
                        fila['CuentaBancaria']              = nodo.attrib.get('CuentaBancaria'              , '')
                        fila['Salario Base Cotiz']          = nodo.attrib.get('SalarioBaseCotApor'          , '')
                        fila['SDI']                         = nodo.attrib.get('SalarioDiarioIntegrado'      , '')
                        fila['Clave Entidad']               = nodo.attrib.get('ClaveEntFed'                 , '')
                        fila['CuentaBancaria']              = nodo.attrib.get('CuentaBancaria'              , '')
                        #

                    # Add "nomina12:EntidadSNCF " attribs as new row
                    if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}EntidadSNCF"):
                        fila['Origen Recursos']             = nodo.attrib.get('OrigenRecurso'               , '')
                        fila['Monto Recursos Propios']      = nodo.attrib.get('MontoRecursoPropio'          , '')

                    # Add "nomina12:Percepciones" attribs as new row
                    if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Percepciones"):
                        fila['Total Sueldos']               = nodo.attrib.get('TotalSueldos'                , '')
                        fila['Total Separac Indemniz']      = nodo.attrib.get('TotalSeparacionIndemnizacion', '')
                        fila['Total Jub Pens Retiro']       = nodo.attrib.get('TotalJubilacionPensionRetiro', '')

                    # Add "nomina12:HorasExtra" attribs as new row
                    if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}HorasExtra"):
                        fila['Importe Horas Extras']        = nodo.attrib.get('ImportePagado'               , '')
                    
                    # Add "nomina12:SeparacionIndemnizacion" attribs as new row
                    if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}SeparacionIndemnizacion"):
                        fila['Importe Separac Indemniz']    = nodo.attrib.get('TotalPagado'                 , '')

                    # Add "nomina12:Deducciones" attribs as new row
                    if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}Deducciones"):
                        fila['Total Otras Deducc']          = nodo.attrib.get('TotalOtrasDeducciones'       , '')
                        fila['Total Imptos Ret']            = nodo.attrib.get('TotalImpuestosRetenidos'     , '')

                    # Add "nomina12:OtroPago" attribs as new row
                    if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}OtroPago"):
                        fila['Importe Otro Pago']           = nodo.attrib.get('Importe'                     , '')

                    # Add "nomina12:SubsidioAlEmpleo" attribs as new row
                    if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}SubsidioAlEmpleo"):
                        fila['SPE causado']                 = nodo.attrib.get('SubsidioCausado'             , '')

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
                            concept_list.append(json.loads(json.dumps(concept_data, ensure_ascii=False)))

                        # Add the list of concepts to the main dictionary
                        fila['Lista de Conceptos']          = json.dumps(concept_list, ensure_ascii=False)
                        fila['Objeto Impuesto']             = nodo.attrib.get('ObjetoImp', '')

                    # Add "cfdi:TimbreFiscalDigital" attribs as new row
                    if nodo.tag.endswith('TrasladoDR'):
                        fila['Objeto Impuesto_DR']          = nodo.attrib.get('ImporteDR', '')
                        fila['Importe Impuesto 16%_DR']     = nodo.attrib.get('ImporteDR', '')
                    

                    # Add "cfdi:Traslado" attribs as new row
                    
                    # Eliminar para ayudas
                    if nodo.tag.endswith('Traslado'):
                        # Create an empty dictionary to store the transfer data
                        transfer_list = []

                        transfers = nodo.xpath('//cfdi:Traslados/cfdi:Traslado', namespaces=nodo.nsmap)
                        
                        # Iterate over the cfdi:Traslado elements and add their data to the dictionary
                        for transfer in transfers:
                            transfer_data = {
                                'Importe': transfer.get('Importe'   , ''),
                            }
                            transfer_list.append(transfer_data)
                        # Add the list of concepts to the main dictionary
                        fila['Lista de Traslado']           = json.dumps(transfer_list, ensure_ascii=False).encode('utf-8')
                    
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
                            payment_list.append(json.loads(json.dumps(payment_data, ensure_ascii=False)))                              
                        fila['Lista de Pagos']              = json.dumps(payment_list, ensure_ascii=False)
                        fila['Fecha Pago']                  = nodo.attrib.get('FechaPago'   , '')
                        fila['Moneda Pago']                 = nodo.attrib.get('MonedaP'     , '')
                        fila['Tipo Cambio']                 = nodo.attrib.get('TipoCambioP' , '')
                        fila['Monto UUID Relac']            = nodo.attrib.get('Monto'       , '')

                except Exception as e:
                    continue
            break
    else:
        raise Exception(f'{e} \nfilename: {filename}')
    
    return fila