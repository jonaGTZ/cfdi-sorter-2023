# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [05/15/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules
import json
from set_sat_status import set_sat_status

def cfdi_payroll_row(nodo, fila, filename, option, rfc):
    try:
        emisor      = '{http://www.sat.gob.mx/cfd/3}Emisor'
        receptor    = '{http://www.sat.gob.mx/cfd/3}Receptor'

        # Add "cfdi:Comprobante" node as new column
        if nodo.tag.endswith('Comprobante'):
            fila['Version']                 = nodo.attrib.get('Version'            , '')
            fila['Fecha Emision']           = nodo.attrib.get('Fecha'              , '')
            fila['Serie']                   = nodo.attrib.get('Serie'              , '')
            fila['Folio']                   = nodo.attrib.get('Folio'              , '')
            fila['Tipo Comprobante']        = nodo.attrib.get('TipoDeComprobante'  , '')
            fila['Tipo']                    = 'Nomina'
            fila['Metodo Pago']             = nodo.attrib.get('MetodoPago'         , '')
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
            if nodo.attrib.get('Version') == '4.0':
                emisor      = '{http://www.sat.gob.mx/cfd/4}Emisor'
                receptor    = '{http://www.sat.gob.mx/cfd/4}Receptor'

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
            
        if nodo.tag.endswith(f'{emisor}'):
            fila['RFC Emisor']              = nodo.attrib.get('Rfc'                , '')
            fila['Nombre Emisor']           = nodo.attrib.get('Nombre'             , '')
            fila['Regimen Fiscal Emisor']   = nodo.attrib.get('RegimenFiscal'      , '')

        # Add "cfdi:Receptor" attribs as new row
        if nodo.tag.endswith(f'{receptor}'):
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
                    'ClaveProdServ' : concept.get('ClaveProdServ'   , ''),
                    'Cantidad'      : concept.get('Cantidad'        , ''),
                    'Clave Unidad'  : concept.get('ClaveUnidad'     , ''),
                    'Unidad'        : concept.get('Unidad'          , ''),
                    'Descripcion'   : concept.get('Descripcion'     , ''),
                }
                concept_list.append(concept_data)
            # Add the list of concepts to the main dictionary
            fila['Lista de Conceptos']      = json.dumps(concept_list, ensure_ascii=False).encode('utf-8')
            fila['Objeto Impuesto']         = nodo.attrib.get('ObjetoImp'               , '')

        # Add "cfdi:TimbreFiscalDigital" attribs as new row
        if nodo.tag.endswith('TimbreFiscalDigital'):
            fila['Fecha Timbrado']          = nodo.attrib.get('FechaTimbrado'           , '')
            fila['UUID']                    = nodo.attrib.get('UUID'                    , '')
            # call to the data stored in the json generated in the sorter
            estado_sat, fecha_consulta      = set_sat_status(nodo.attrib.get('UUID', ''), option, rfc)
            fila['Estado SAT']              = estado_sat
            fila['Fecha Consulta']          = fecha_consulta

        # Add "nomina12:Nomina" attribs as new row
        if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Nomina"):
            fila['ISR']                     = nodo.attrib.get('TotalDeducciones'        , '')
            fila['Version Nomina']          = nodo.attrib.get('Version '                , '')
            fila['Tipo Nomina']             = nodo.attrib.get('TipoNomina'              , '')
            fila['Fecha Pago']              = nodo.attrib.get('FechaPago'               , '')
            fila['Fecha Inicial Pago']      = nodo.attrib.get('FechaInicialPago'        , '')
            fila['Fecha Final Pago']        = nodo.attrib.get('FechaFinalPago'          , '')
            fila['Num Dias Pagados']        = nodo.attrib.get('NumDiasPagados'          , '')
            fila['Total Percepciones']      = nodo.attrib.get('TotalPercepciones'       , '')
            fila['Total Deducciones']       = nodo.attrib.get('TotalDeducciones'        , '')
            fila['Total Otros Pagos']       = nodo.attrib.get('TotalOtrosPagos'         , '')
            fila['Fecha Pago']              = nodo.attrib.get('FechaPago'               , '')
        
        # Add "nomina12:Emisor" attribs as new row
        if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Emisor"):
            fila['Registro Patronal']       = nodo.attrib.get('RegistroPatronal'        , '')    
            
        # Add "nomina12:Receptor" attribs as new row
        if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Receptor"):
            fila['CURP']                    = nodo.attrib.get('Curp'                    , '')
            fila['Num Seguridad Social']    = nodo.attrib.get('NumSeguridadSocial'      , '')
            fila['Fecha Inicial Relac Lab'] = nodo.attrib.get('FechaInicioRelLaboral'   , '')
            fila['Antigüedad']              = nodo.attrib.get('Antigüedad'              , '')
            fila['Tipo Contrato']           = nodo.attrib.get('TipoContrato'            , '')
            fila['Sindicalizado']           = nodo.attrib.get('Sindicalizado'           , '')
            fila['Tipo Jornada']            = nodo.attrib.get('TipoJornada'             , '')
            fila['Tipo Regimen']            = nodo.attrib.get('TipoRegimen'             , '')
            fila['Num Empleado']            = nodo.attrib.get('NumEmpleado'             , '')
            fila['Departamento']            = nodo.attrib.get('Departamento'            , '')
            fila['Puesto']                  = nodo.attrib.get('Puesto'                  , '')
            fila['Riesgo Puesto']           = nodo.attrib.get('RiesgoPuesto'            , '')
            fila['Periodicidad Pago']       = nodo.attrib.get('PeriodicidadPago'        , '')
            fila['Banco']                   = nodo.attrib.get('Banco'                   , '')
            fila['CuentaBancaria']          = nodo.attrib.get('CuentaBancaria'          , '')
            fila['Salario Base Cotiz']      = nodo.attrib.get('SalarioBaseCotApor'      , '')
            fila['SDI']                     = nodo.attrib.get('SalarioDiarioIntegrado'  , '')
            fila['Clave Entidad']           = nodo.attrib.get('ClaveEntFed'              , '')
            fila['CuentaBancaria']          = nodo.attrib.get('CuentaBancaria'          , '')
            #

        # Add "nomina12:EntidadSNCF " attribs as new row
        if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}EntidadSNCF"):
            fila['Origen Recursos']         = nodo.attrib.get('OrigenRecurso'           , '')
            fila['Monto Recursos Propios']  = nodo.attrib.get('MontoRecursoPropio'      , '')

        # Add "nomina12:Percepciones" attribs as new row
        if nodo.tag.endswith("{http://www.sat.gob.mx/nomina12}Percepciones"):
            fila['Total Sueldos']           = nodo.attrib.get('TotalSueldos'            , '')
            fila['Total Separac Indemniz']  = nodo.attrib.get('TotalSeparacionIndemnizacion', '')
            fila['Total Jub Pens Retiro']   = nodo.attrib.get('TotalJubilacionPensionRetiro', '')

        # Add "nomina12:HorasExtra" attribs as new row
        if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}HorasExtra"):
            fila['Importe Horas Extras']    = nodo.attrib.get('ImportePagado'           , '')
        
        # Add "nomina12:SeparacionIndemnizacion" attribs as new row
        if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}SeparacionIndemnizacion"):
            fila['Importe Separac Indemniz']= nodo.attrib.get('TotalPagado'             , '')

        # Add "nomina12:Deducciones" attribs as new row
        if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}Deducciones"):
            fila['Total Otras Deducc']      = nodo.attrib.get('TotalOtrasDeducciones'   , '')
            fila['Total Imptos Ret']        = nodo.attrib.get('TotalImpuestosRetenidos' , '')

        # Add "nomina12:OtroPago" attribs as new row
        if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}OtroPago"):
            fila['Importe Otro Pago']       = nodo.attrib.get('Importe'                 , '')

        # Add "nomina12:SubsidioAlEmpleo" attribs as new row
        if nodo.tag.endswith("http://www.sat.gob.mx/nomina12}SubsidioAlEmpleo"):
            fila['SPE causado']             = nodo.attrib.get('SubsidioCausado'         , '')
    
    except Exception as e:
        raise Exception(f'R01: {e} {nodo.tag} \n {filename}')
    
    return fila