# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [06/02/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import json

from datetime       import datetime
from set_sat_status import set_sat_status
from lxml           import etree
from cfdi_details   import get_regime_payroll, get_tax_regime, get_cfdi_usage, get_payment_method, get_payment_form, get_cfdi_type

def string_to_double(string):
    try:
        num = float(string)
        return num
    except ValueError:
        # Handle exception in case string is not convertible to number
        return string  # Optionally, you can throw a custom exception here

def clean_concept(dic):
    # Verificamos que la entrada sea una lista de diccionarios
    if isinstance(dic, list) and all(isinstance(item, dict) for item in dic):
        # Creamos una lista para almacenar los valores
        key_value_list = []
        
        # Iteramos sobre cada diccionario en la lista
        for data in dic:
            # Iteramos sobre los valores del diccionario y los convertimos a cadena
            key_value = ", ".join([f"{key}: {value}" for key, value in data.items()])
            key_value_list.append(key_value)
            # Concatenamos los valores con comas y los agregamos a la lista
            key_value_list.append(key_value)
        
        # Retornamos la lista de valores como una cadena separada por saltos de línea
        return "\n".join(key_value_list)
    else:
        return "Entrada no válida, se espera una lista de diccionarios JSON."
    
def list_to_string(strings):
    key = ''
    for string in strings:
        key += string + ' '
    return key

def cfdi_row_collector(node, row, filename, option, rfc):

    emisor      = ''
    receptor    = ''
    
    if node.tag.endswith('Comprobante'):
        if node.attrib.get('Version') == '4.0':
            emisor      = '{http://www.sat.gob.mx/cfd/4}Emisor'
            receptor    = '{http://www.sat.gob.mx/cfd/4}Receptor'
    
    try:
        # Add "cfdi:Comprobante" node as new column
        if node.tag.endswith('Comprobante'):
            row['Version']                     = node.attrib.get('Version'                     , '')
            row['Fecha Emision']               = datetime.strptime(node.attrib.get('Fecha'), '%Y-%m-%dT%H:%M:%S')
            row['Serie']                       = node.attrib.get('Serie'                       , '')
            row['Folio']                       = node.attrib.get('Folio'                       , '')
            row['Tipo Comprobante']            = node.attrib.get('TipoDeComprobante'           , '')
            row['Tipo']                        = get_cfdi_type(node.attrib.get('TipoDeComprobante'))
            if not (option == 'PAGO_R' or option == 'PAGO_E'):
                row['Metodo Pago']             = get_payment_method(node.attrib.get('MetodoPago'                , ''))
            row['Forma Pago']                  = get_payment_form(node.attrib.get('FormaPago'                   , ''))
            row['Subtotal']                    = string_to_double(node.attrib.get('SubTotal'                    , ''))
            if not (option == 'GASTO' or option == 'PAGO_R' or option == 'PAGO_E'):
                row['Descuento']               = node.attrib.get('Descuento'                   , '')

            row['Total']                       = string_to_double(node.attrib.get('Total'                       , ''))
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
            row['Regimen Fiscal Emisor']       = get_tax_regime(node.attrib.get('RegimenFiscal'               , ''))
        elif node.tag.endswith('{http://www.sat.gob.mx/cfd/4}Emisor'):
            row['RFC Emisor']                  = node.attrib.get('Rfc'                         , '')
            row['Nombre Emisor']               = node.attrib.get('Nombre'                      , '')
            row['Regimen Fiscal Emisor']       = get_tax_regime(node.attrib.get('RegimenFiscal'               , ''))

        # Add "cfdi:Receptor" attribs as new row
        if node.tag.endswith('{http://www.sat.gob.mx/cfd/3}Receptor'):
            row['RFC Receptor']                = node.attrib.get('Rfc'                         , '')
            row['Nombre Receptor']             = node.attrib.get('Nombre'                      , '')
            row['CP Receptor']                 = node.attrib.get('DomicilioFiscalReceptor'     , '')
            row['Regimen Fiscal Receptor']     = get_tax_regime(node.attrib.get('RegimenFiscalReceptor'       , ''))
            row['Uso CFDI']                    = get_cfdi_usage(node.attrib.get('UsoCFDI'                     , ''))
        elif node.tag.endswith('{http://www.sat.gob.mx/cfd/4}Receptor'):
            row['RFC Receptor']                = node.attrib.get('Rfc'                         , '')
            row['Nombre Receptor']             = node.attrib.get('Nombre'                      , '')
            row['CP Receptor']                 = node.attrib.get('DomicilioFiscalReceptor'     , '')
            row['Regimen Fiscal Receptor']     = get_tax_regime(node.attrib.get('RegimenFiscalReceptor'       , ''))
            row['Uso CFDI']                    = get_cfdi_usage(node.attrib.get('UsoCFDI'                     , ''))

        # Add "leyendasFisc:Leyenda" attribs as new row
        if node.tag.endswith('Leyenda'):
            row['Leyenda']                     = node.attrib.get('textoLeyenda'                , '')

        # Add "cfdi:Impuestos" attribs as new row 
        if node.tag.endswith('Impuestos'):
            row['Total Imp Retenidos']         = string_to_double(node.attrib.get('TotalImpuestosRetenidos'     , ''))
            row['Total Imp Trasladados']       = string_to_double(node.attrib.get('TotalImpuestosTrasladados'   , ''))

        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if node.tag.endswith('TimbreFiscalDigital'):
            row['Fecha Timbrado']              = datetime.strptime(node.attrib.get('FechaTimbrado'), '%Y-%m-%dT%H:%M:%S')
            row['UUID']                        = node.attrib.get('UUID', '')
            # call to the data stored in the json generated in the sorter
            estado_sat, fecha_consulta          = set_sat_status(node.attrib.get('UUID', ''), option, rfc)
            row['Estado SAT']                  = estado_sat
            row['Fecha Consulta']              = datetime.strptime(fecha_consulta, '%Y-%m-%dT%H:%M:%S')

        # Add "cfdi:InformacionAduanera" attribs as new row
        if node.tag.endswith('InformacionAduanera'):
            row['Numero Pedimento']            = node.attrib.get('NumeroPedimento'             , '')
        
        # Add "nomina12:Nomina" attribs as new row
        if node.tag.endswith("{http://www.sat.gob.mx/nomina12}Nomina"):
            row['ISR']                         = string_to_double(node.attrib.get('TotalDeducciones'            , ''))
            row['Version Nomina']              = node.attrib.get('Version '                    , '')
            row['Tipo Nomina']                 = node.attrib.get('TipoNomina'                  , '')
            row['Fecha Pago']                  = node.attrib.get('FechaPago'                   , '')
            row['Fecha Inicial Pago']          = node.attrib.get('FechaInicialPago'            , '')
            row['Fecha Final Pago']            = node.attrib.get('FechaFinalPago'              , '')
            row['Num Dias Pagados']            = node.attrib.get('NumDiasPagados'              , '')
            row['Total Percepciones']          = string_to_double(node.attrib.get('TotalPercepciones'           , ''))
            row['Total Deducciones']           = string_to_double(node.attrib.get('TotalDeducciones'            , ''))
            row['Total Otros Pagos']           = string_to_double(node.attrib.get('TotalOtrosPagos'             , ''))
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
            row['Tipo Regimen']                = get_regime_payroll(node.attrib.get('TipoRegimen'                 , ''))
            row['Num Empleado']                = node.attrib.get('NumEmpleado'                 , '')
            row['Departamento']                = node.attrib.get('Departamento'                , '')
            row['Puesto']                      = node.attrib.get('Puesto'                      , '')
            row['Riesgo Puesto']               = node.attrib.get('RiesgoPuesto'                , '')
            row['Periodicidad Pago']           = node.attrib.get('PeriodicidadPago'            , '')
            row['Banco']                       = node.attrib.get('Banco'                       , '')
            row['Cuenta Bancaria']             = node.attrib.get('CuentaBancaria'              , '')
            row['Salario Base Cotiz']          = node.attrib.get('SalarioBaseCotApor'          , '')
            row['SDI']                         = node.attrib.get('SalarioDiarioIntegrado'      , '')
            row['Clave Entidad']               = node.attrib.get('ClaveEntFed'                 , '')

        # Add "nomina12:EntidadSNCF " attribs as new row
        if node.tag.endswith("{http://www.sat.gob.mx/nomina12}EntidadSNCF"):
            row['Origen Recursos']             = node.attrib.get('OrigenRecurso'               , '')
            row['Monto Recursos Propios']      = node.attrib.get('MontoRecursoPropio'          , '')

        # Add "nomina12:Percepciones" attribs as new row
        if node.tag.endswith("{http://www.sat.gob.mx/nomina12}Percepciones"):
            row['Total Sueldos']               = string_to_double(node.attrib.get('TotalSueldos'                , ''))
            row['Total Separac Indemniz']      = string_to_double(node.attrib.get('TotalSeparacionIndemnizacion', ''))
            row['Total Jub Pens Retiro']       = string_to_double(node.attrib.get('TotalJubilacionPensionRetiro', ''))

        # Add "nomina12:HorasExtra" attribs as new row
        if node.tag.endswith("http://www.sat.gob.mx/nomina12}HorasExtra"):
            row['Importe Horas Extras']        = string_to_double(node.attrib.get('ImportePagado'               , ''))
        
        # Add "nomina12:SeparacionIndemnizacion" attribs as new row
        if node.tag.endswith("http://www.sat.gob.mx/nomina12}SeparacionIndemnizacion"):
            row['Importe Separac Indemniz']    = string_to_double(node.attrib.get('TotalPagado'                 , ''))

        # Add "nomina12:Deducciones" attribs as new row
        if node.tag.endswith("http://www.sat.gob.mx/nomina12}Deducciones"):
            row['Total Otras Deducc']          = string_to_double(node.attrib.get('TotalOtrasDeducciones'       , ''))
            row['Total Imptos Ret']            = string_to_double(node.attrib.get('TotalImpuestosRetenidos'     , ''))

        # Add "nomina12:OtroPago" attribs as new row
        if node.tag.endswith("http://www.sat.gob.mx/nomina12}OtroPago"):
            row['Importe Otro Pago']           = string_to_double(node.attrib.get('Importe'                     , ''))

        # Add "nomina12:SubsidioAlEmpleo" attribs as new row
        if node.tag.endswith("http://www.sat.gob.mx/nomina12}SubsidioAlEmpleo"):
            row['SPE causado']                 = node.attrib.get('SubsidioCausado'             , '')
        
        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if node.tag.endswith('TrasladoDR'):
            row['Objeto Impuesto_DR']          = string_to_double(node.attrib.get('ImporteDR', ''))
            row['Importe Impuesto 16%_DR']     = string_to_double(node.attrib.get('ImporteDR', ''))

        if node.tag.endswith('Conceptos'):
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
        if node.tag.endswith('Impuestos'):
            # set child node to parse 
            taxes       = node.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=node.nsmap)
            transfers   = node.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=node.nsmap)

            isr     = 0.0
            ret_isr = 0.0
            iva     = 0.0
            ret_iva = 0.0 
            ieps    = 0.0
            ret_ieps= 0.0
            
            for tax in taxes:
                if   tax.get('Impuesto') == "001":
                    isr += string_to_double(tax.get('Importe')) 
                elif tax.get('Impuesto') == "002":
                    iva += string_to_double(tax.get('Importe'))
                elif tax.get('Impuesto') == "003":
                    ieps += string_to_double(tax.get('Importe'))

            for transfer in transfers:
                if   transfer.get('Impuesto') == "001":
                    ret_isr += string_to_double(transfer.get('Importe')) 
                elif transfer.get('Impuesto') == "002":
                    ret_iva += string_to_double(transfer.get('Importe'))
                elif transfer.get('Impuesto') == "003":
                    ret_ieps += string_to_double(transfer.get('Importe'))

            columns = {
                isr: 'ISR',
                iva: 'IVA 16%',
                ieps: 'IEPS',
                ret_isr: 'Retención ISR',
                ret_iva: 'Retención IVA',
                ret_ieps: 'Retención IEPS',
            }

            for key, value in columns.items():
                if key > 0:
                    row[value] = key

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

        # returns the matrix with the rows and their respective information
        return row

    # understand that the exception that is handled is for cases where fila[row name] does not exist
    except:
        raise Exception('')