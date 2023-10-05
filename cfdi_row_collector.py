# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [06/02/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules

from datetime       import datetime
from set_sat_status import set_sat_status
from lxml           import etree
from cfdi_details   import get_regime_payroll, get_tax_regime, get_cfdi_usage, get_payment_method, get_payment_form, get_cfdi_type, get_exchange_type, get_related_cfdi_type, get_DR_taxes_type, get_payment_type_p, get_day_type, get_contract_type, get_periodicity_type, get_position_risk_type

def string_to_double(string):
    try:
        num = float(string)
        return num
    except ValueError:
        # Handle exception in case string is not convertible to number
        return str(string)  # Optionally, you can throw a custom exception here

def clean_concept(dic):
    # Verificamos que la entrada sea una lista de diccionarios
    if isinstance(dic, list) and all(isinstance(item, dict) for item in dic):
        # Creamos una lista para almacenar los valores
        key_value_list = []
        
        # Iteramos sobre cada diccionario en la lista
        for data in dic:
            # Iteramos sobre los valores del diccionario y los convertimos a cadena
            key_value = ", ".join([f"{key}: {value}" for key, value in data.items()])
            # Concatenamos los valores con comas y los agregamos a la lista
            key_value_list.append(f'{{{key_value}}},')
        
        # Retornamos la lista de valores como una cadena separada por saltos de línea
        return ' '.join(key_value_list)
    else:
        return "Entrada no válida, se espera una lista de diccionarios JSON."
    
def list_to_string(strings):
    key = ''
    for string in strings:
        key += string + ' '
    return key

def cfdi_row_collector(node, row, option, rfc):

    def set_cfdi_attrib(attrib):
        return node.attrib.get(attrib, '')
    
    try:
        # Add "cfdi:Comprobante" node as new column
        if str(node.tag).endswith('Comprobante'):
            row['Version']          = set_cfdi_attrib('Version')
            row['Fecha Emision']    = datetime.strptime(set_cfdi_attrib('Fecha'), '%Y-%m-%dT%H:%M:%S')
            row['Serie']            = set_cfdi_attrib('Serie')
            row['Folio']            = set_cfdi_attrib('Folio')
            row['Tipo Comprobante'] = get_cfdi_type(set_cfdi_attrib('TipoDeComprobante'))
            row['Subtotal']         = string_to_double(set_cfdi_attrib('SubTotal'))
            row['Total']            = string_to_double(set_cfdi_attrib('Total'))
            row['Moneda']           = set_cfdi_attrib('Moneda')
            row['CP Emisor']        = set_cfdi_attrib('LugarExpedicion')
            row['Moneda']           = set_cfdi_attrib('Moneda')
            row['Sello']            = set_cfdi_attrib('Sello')
            row['No Certificado']   = set_cfdi_attrib('NoCertificado')
            row['Certificado']      = set_cfdi_attrib('Certificado')
            if not (option == 'PAGO_R' or option == 'PAGO_E'):
                row['Forma Pago']       = get_payment_form(set_cfdi_attrib('FormaPago'))
                row['Tipo Cambio']      = get_exchange_type(set_cfdi_attrib('TipoCambio'))
                row['Condiciones Pago'] = set_cfdi_attrib('CondicionesDePago')
                row['Descuento']        = string_to_double(set_cfdi_attrib('Descuento'))
                row['Metodo Pago']      = get_payment_method(set_cfdi_attrib('MetodoPago'))

        # Add "cfdi:CfdiRelacionados" attribs as new row
        if str(node.tag).endswith('CfdiRelacionados'):
            row['Tipo Relacion'] = get_related_cfdi_type(set_cfdi_attrib('TipoRelacion'))

        # Add "cfdi:CfdiRelacionado" attribs as new row
        if str(node.tag).endswith('CfdiRelacionado'):
            row['UUID Relacion'] = set_cfdi_attrib('UUID')

        # Add "cfdi:Emisor" attribs as new row
        if str(node.tag).endswith('{http://www.sat.gob.mx/cfd/3}Emisor'):
            row['RFC Emisor']               = set_cfdi_attrib('Rfc')
            row['Nombre Emisor']            = set_cfdi_attrib('Nombre')
            row['Regimen Fiscal Emisor']    = get_tax_regime(set_cfdi_attrib('RegimenFiscal'))
        elif str(node.tag).endswith('{http://www.sat.gob.mx/cfd/4}Emisor'):
            row['RFC Emisor']               = set_cfdi_attrib('Rfc')
            row['Nombre Emisor']            = set_cfdi_attrib('Nombre')
            row['Regimen Fiscal Emisor']    = get_tax_regime(set_cfdi_attrib('RegimenFiscal'))

        # Add "cfdi:Receptor" attribs as new row
        if str(node.tag).endswith('{http://www.sat.gob.mx/cfd/3}Receptor'):
            row['RFC Receptor']             = set_cfdi_attrib('Rfc')
            row['Nombre Receptor']          = set_cfdi_attrib('Nombre')
            row['CP Receptor']              = set_cfdi_attrib('DomicilioFiscalReceptor')
            row['Regimen Fiscal Receptor']  = get_tax_regime(set_cfdi_attrib('RegimenFiscalReceptor'))
            row['Uso CFDI']                 = get_cfdi_usage(set_cfdi_attrib('UsoCFDI'))
        elif str(node.tag).endswith('{http://www.sat.gob.mx/cfd/4}Receptor'):
            row['RFC Receptor']             = set_cfdi_attrib('Rfc')
            row['Nombre Receptor']          = set_cfdi_attrib('Nombre')
            row['CP Receptor']              = set_cfdi_attrib('DomicilioFiscalReceptor')
            row['Regimen Fiscal Receptor']  = get_tax_regime(set_cfdi_attrib('RegimenFiscalReceptor'))
            row['Uso CFDI']                 = get_cfdi_usage(set_cfdi_attrib('UsoCFDI'))

        # Add "leyendasFisc:Leyenda" attribs as new row
        if str(node.tag).endswith('Leyenda'):
            row['Leyenda'] = set_cfdi_attrib('textoLeyenda')

        # Add "cfdi:Impuestos" attribs as new row 
        if str(node.tag).endswith('Impuestos'):
            row['Total Imp Retenidos']      = string_to_double(set_cfdi_attrib('TotalImpuestosRetenidos'))
            row['Total Imp Trasladados']    = string_to_double(set_cfdi_attrib('TotalImpuestosTrasladados'))

        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if str(node.tag).endswith('TimbreFiscalDigital'):
            row['Fecha Timbrado']   = datetime.strptime(set_cfdi_attrib('FechaTimbrado'), '%Y-%m-%dT%H:%M:%S')
            row['UUID']             = set_cfdi_attrib('UUID')
            # call to the data stored in the json generated in the sorter
            estado_sat, fecha_consulta = set_sat_status(set_cfdi_attrib('UUID'), option, rfc)
            row['Estado SAT']       = estado_sat
            row['Fecha Consulta']   = datetime.strptime(fecha_consulta, '%Y-%m-%dT%H:%M:%S')

        # Add "cfdi:InformacionAduanera" attribs as new row
        if str(node.tag).endswith('InformacionAduanera'):
            row['Numero Pedimento'] = set_cfdi_attrib('NumeroPedimento')
        
        # Add "nomina12:Nomina" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}Nomina"):
            row['ISR']                  = string_to_double(set_cfdi_attrib('TotalDeducciones'))
            row['Version Nomina']       = set_cfdi_attrib('Version')
            row['Tipo Nomina']          = set_cfdi_attrib('TipoNomina')
            row['Fecha Pago']           = datetime.strptime(set_cfdi_attrib('FechaPago'), '%Y-%m-%d')
            row['Fecha Inicial Pago']   = datetime.strptime(set_cfdi_attrib('FechaInicialPago'), '%Y-%m-%d')
            row['Fecha Final Pago']     = datetime.strptime(set_cfdi_attrib('FechaFinalPago'), '%Y-%m-%d')
            row['Num Dias Pagados']     = string_to_double(set_cfdi_attrib('NumDiasPagados'))
            row['Total Percepciones']   = string_to_double(set_cfdi_attrib('TotalPercepciones'))
            row['Total Deducciones']    = string_to_double(set_cfdi_attrib('TotalDeducciones'))
            row['Total Otros Pagos']    = string_to_double(set_cfdi_attrib('TotalOtrosPagos'))
        
        # Add "nomina12:Emisor" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}Emisor"):
            row['Registro Patronal'] = set_cfdi_attrib('RegistroPatronal')    
            
        # Add "nomina12:Receptor" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}Receptor"):
            row['CURP']                     = set_cfdi_attrib('Curp')
            row['Num Seguridad Social']     = set_cfdi_attrib('NumSeguridadSocial')
            row['Fecha Inicial Relac Lab']  = datetime.strptime(set_cfdi_attrib('FechaInicioRelLaboral'), '%Y-%m-%d')
            row['Antigüedad']               = set_cfdi_attrib('Antigüedad')
            row['Tipo Contrato']            = get_contract_type(set_cfdi_attrib('TipoContrato'))
            row['Sindicalizado']            = set_cfdi_attrib('Sindicalizado')
            row['Tipo Jornada']             = get_day_type(set_cfdi_attrib('TipoJornada'))
            row['Tipo Regimen']             = get_regime_payroll(set_cfdi_attrib('TipoRegimen'))
            row['Num Empleado']             = set_cfdi_attrib('NumEmpleado')
            row['Departamento']             = set_cfdi_attrib('Departamento')
            row['Puesto']                   = set_cfdi_attrib('Puesto')
            row['Riesgo Puesto']            = get_position_risk_type(set_cfdi_attrib('RiesgoPuesto'))
            row['Periodicidad Pago']        = get_periodicity_type(set_cfdi_attrib('PeriodicidadPago'))
            row['Banco']                    = set_cfdi_attrib('Banco')
            row['Cuenta Bancaria']          = set_cfdi_attrib('CuentaBancaria')
            row['Salario Base Cotiz']       = string_to_double(set_cfdi_attrib('SalarioBaseCotApor'))
            row['SDI']                      = string_to_double(set_cfdi_attrib('SalarioDiarioIntegrado'))
            row['Clave Entidad']            = set_cfdi_attrib('ClaveEntFed')

        # Add "nomina12:EntidadSNCF " attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}EntidadSNCF"):
            row['Origen Recursos']          = set_cfdi_attrib('OrigenRecurso')

        # Add "nomina12:Percepciones" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}Percepciones"):
            row['Total Sueldos']            = string_to_double(set_cfdi_attrib('TotalSueldos'))
            row['Total Separac Indemniz']   = string_to_double(set_cfdi_attrib('TotalSeparacionIndemnizacion'))
            row['Total Jub Pens Retiro']    = string_to_double(set_cfdi_attrib('TotalJubilacionPensionRetiro'))

        # Add "nomina12:HorasExtra" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}HorasExtra"):
            row['Importe Horas Extras'] = string_to_double(set_cfdi_attrib('ImportePagado'))
        
        # Add "nomina12:SeparacionIndemnizacion" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}SeparacionIndemnizacion"):
            row['Importe Separac Indemniz'] = string_to_double(set_cfdi_attrib('TotalPagado'))

        # Add "nomina12:Deducciones" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}Deducciones"):
            row['Total Otras Deducc'] = string_to_double(set_cfdi_attrib('TotalOtrasDeducciones'))
            row['Total Imptos Ret']   = string_to_double(set_cfdi_attrib('TotalImpuestosRetenidos'))

        # Add "nomina12:OtroPago" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}OtroPago"):
            row['Importe Otro Pago'] = string_to_double(set_cfdi_attrib('Importe'))

        # Add "nomina12:SubsidioAlEmpleo" attribs as new row
        if str(node.tag).endswith("{http://www.sat.gob.mx/nomina12}SubsidioAlEmpleo"):
            row['SPE causado'] = string_to_double(set_cfdi_attrib('SubsidioCausado'))
        
        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if str(node.tag).endswith('TrasladoDR'):
            row['Objeto Impuesto_DR']       = get_DR_taxes_type(set_cfdi_attrib('ImpuestoDR'))
            row['Importe Impuesto 16%_DR']  = string_to_double(set_cfdi_attrib('ImporteDR'))

        if str(node.tag).endswith('Conceptos'):
            # Create an empty dictionary to store the concept data, set child node to parse 
            concept_list    = []
            prod_list       = []
            key_unit_list   = []
            unit_list       = []
            
            concepts = node.xpath('//cfdi:Conceptos/cfdi:Concepto', namespaces=node.nsmap)
            
            # Iterate over the cfdi:Concept elements and add their data to the dictionary
            for concept in concepts:
            
                concept_data = {
                    'ClaveProdServ'     : concept.get('ClaveProdServ'   , ''),
                    'NoIdentificacion'  : concept.get('NoIdentificacion', ''),
                    'Cantidad'          : concept.get('Cantidad'        , ''),
                    'Clave Unidad'      : concept.get('ClaveUnidad'     , ''),
                    'Unidad'            : concept.get('Unidad'          , ''),
                    'Objeto Impuesto'   : concept.get('ObjetoImp'       , ''),
                    'Descripcion'       : concept.get('Descripcion'     , ''),
                    'Valor Unitario'    : concept.get('ValorUnitario'   , ''),
                    'Importe'           : concept.get('Importe'         , ''),
                    'Descuento'         : concept.get('Descuento'       , '')
                }
                concept_list.append(concept_data)
                prod_list.append(concept_data['ClaveProdServ'])
                key_unit_list.append(concept_data['Clave Unidad'])
                unit_list.append(concept_data['Unidad'])
                
            # Add the list of concepts to the main dictionary
            row['Lista de Conceptos']       = clean_concept(concept_list)
            row['Lista Clave de Producto']  = list_to_string(prod_list)
            row['Lista Clave de Unidad']    = list_to_string(key_unit_list)
            row['Lista Unidad']             = list_to_string(unit_list)
            
        # Add "cfdi:Retenciones" attribs as new row
        if str(node.tag).endswith('Impuestos'):
            # set child node to parse 
            taxes = node.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=node.nsmap)
            transfers = node.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=node.nsmap)

            # Usar un diccionario auxiliar para rastrear la sumatoria de valores para cada impuesto
            impuestos = {
                "001": 0.0,
                "002": 0.0,
                "003": 0.0
            }

            retenciones = {
                "001": 0.0,
                "002": 0.0,
                "003": 0.0
            }

            for tax in taxes:
                if tax.get('TipoFactor') == 'Exento':
                    continue

                impuesto = tax.get('Impuesto')
                importe = string_to_double(tax.get('Importe'))
                impuestos[impuesto] += importe

            for transfer in transfers:
                if transfer.get('TipoFactor') == 'Exento':
                    continue

                impuesto = transfer.get('Impuesto')
                importe = string_to_double(transfer.get('Importe'))
                retenciones[impuesto] += importe

            rows = {
                'ISR'            : impuestos["001"],
                'IVA 16%'        : impuestos["002"],
                'IEPS'           : impuestos["003"],
                'Retención ISR'  : retenciones["001"],
                'Retención IVA'  : retenciones["002"],
                'Retención IEPS' : retenciones["003"]
            }

            # Eliminar las entradas con valores 0
            rows = {key: value for key, value in rows.items() if value != 0.0}

            for key, value in rows.items():
                row[key] = value


        # Add "cfdi:Pagos" attribs as new row
        if str(node.tag).endswith('Pagos'):

            namespaces={
                'pago10': 'http://www.sat.gob.mx/Pagos',
                'pago20': 'http://www.sat.gob.mx/Pagos20'
            }

            version = 'pago20'
            if set_cfdi_attrib('Version') == '1.0':
                version = 'pago10'
            
            # Create an empty dictionary to store the payment data
            payments = []

            try:
                payments = node.xpath(f'//{version}:Pago', namespaces=namespaces)
            except Exception as e :
                print(e)

            for payment in payments:
                row['Tipo Cambio Pago']     = get_exchange_type(payment.get('TipoCambioP'))
                row['Fecha Pago P']         = datetime.strptime(payment.get('FechaPago'), '%Y-%m-%dT%H:%M:%S')
                row['Forma Pago P']         = get_payment_type_p(payment.get('FormaDePagoP'))
                row['Moneda Pago']          = payment.get('MonedaP')
                row['Monto UUID Relac']     = string_to_double(payment.get('Monto'))
        
        # Add "cfdi:Pagos" attribs as new row
            
            payment_list = []

            try:
                related_payment = node.xpath(f'//{version}:Pago/{version}:DoctoRelacionado', namespaces=namespaces)
            except Exception as e :
                print(e)

            # Iterate over the cfdi:Concept elements and add their data to the dictionary 
            for payment in related_payment:
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
            
            if payment_list:
                row['Lista de Pagos'] = clean_concept(payment_list)

        # specific complementary nodes for each report
        if (option == 'GASTO'):
            if str(node.tag).endswith('implocal:ImpuestosLocales'):
                row['Total Retenciones Locales'] = set_cfdi_attrib('TotaldeRetenciones')
                #row['Total de Traslados']        = set_cfdi_attrib('TotaldeTraslados')
            
            if str(node.tag).endswith('implocal:RetencionesLocales'):
                row['Imp Local Retenido']          = set_cfdi_attrib('ImpLocRetenido')
                row['Tasa Imp Local Retenido']     = set_cfdi_attrib('TasadeRetencion')
                row['Importe Imp Local Retenido']  = set_cfdi_attrib('Importe')

        # returns the matrix with the rows and their respective information
        return row

    # understand that the exception that is handled is for cases where fila[row name] does not exist
    except Exception as e:
        print (f'Error mapping : {e} in {node.tag}')
        