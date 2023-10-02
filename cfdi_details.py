# script header
# Author:           [Hugo Berra Salazar, ]
# Creation date:    [04/24/2023]
# Description:      [Brief description of the purpose of the script]

# import necessary modules

def get_tax_regime(regimer):

    default_value=f'Régimen no especificado {regimer}'
    
    tax_regime = {
        '601': '601 - General de Ley Personas Morales',
        '603': '603 - Personas Morales con Fines no Lucrativos',
        '605': '605 - Sueldos y Salarios e Ingresos Asimilados a Salarios',
        '606': '606 - Arrendamiento',
        '607': '607 - Régimen de Enajenación o Adquisición de Bienes',
        '608': '608 - Demás ingresos',
        '609': '609 - Consolidación',
        '610': '610 - Residentes en el Extranjero sin Establecimiento Permanente en México',
        '611': '611 - Ingresos por Dividendos (socios y accionistas)',
        '612': '612 - Personas Físicas con Actividades Empresariales y Profesionales',
        '614': '614 - Ingresos por intereses',
        '615': '615 - Régimen de los ingresos por obtención de premios',
        '616': '616 - Sin obligaciones fiscales',
        '620': '620 - Sociedades Cooperativas de Producción que optan por diferir sus ingresos',
        '621': '621 - Incorporación Fiscal',
        '622': '622 - Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras',
        '623': '623 - Opcional para Grupos de Sociedades',
        '624': '624 - Coordinados',
        '626': '626 - Régimen Simplificado de Confianza',
        '628': '628 - Hidrocarburos',
        '607': '607 - Régimen de Enajenación o Adquisición de Bienes',
        '629': '629 - De los regímenes fiscales preferentes y de las empresas multinacionales',
        '630': '630 - Enajenación de acciones en bolsa de valores',
        '639': '639 - Régimen de los ingresos obtenidos por residentes en el extranjero',
        '640': '640 - Régimen de Consolidación Fiscal',
        '697': '697 - Régimen General de Pequeños Contribuyentes',
        '698': '698 - Régimen de actividades empresariales y profesionales',
        '699': '699 - Otros regímenes',
    }
    return tax_regime.get(regimer, default_value)

def get_cfdi_usage(usage):
    
    default_value=f'Uso del CFDI no especificado {usage}'
    
    cfdi_usage = {
        'G01': 'G01 - Adquisición de mercancías',
        'G02': 'G02 - Devoluciones, descuentos o bonificaciones',
        'G03': 'G03 - Gastos en general',
        'I01': 'I01 - Construcciones',
        'I02': 'I02 - Mobilario y equipo de oficina por inversiones',
        'I03': 'I03 - Equipo de transporte',
        'I04': 'I04 - Equipo de cómputo y accesorios',
        'I05': 'I05 - Dados, troqueles, moldes, matrices y herramental',
        'I06': 'I06 - Comunicaciones telefónicas',
        'I07': 'I07 - Comunicaciones satelitales',
        'I08': 'I08 - Otra maquinaria y equipo',
        'D01': 'D01 - Honorarios médicos, dentales y gastos hospitalarios.',
        'D02': 'D02 - Gastos médicos por incapacidad o discapacidad',
        'D03': 'D03 - Gastos funerales.',
        'D04': 'D04 - Donativos.',
        'D05': 'D05 - Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación).',
        'D06': 'D06 - Aportaciones voluntarias al SAR.',
        'D07': 'D07 - Primas por seguros de gastos médicos.',
        'D08': 'D08 - Gastos de transportación escolar obligatoria.',
        'D09': 'D09 - Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.',
        'D10': 'D10 - Pagos por servicios educativos (colegiaturas)',
        'P01': 'P01 - Por definir',
    }

    return cfdi_usage.get(usage, default_value)

def get_payment_method(payment):

    default_value=f'Método de pago no especificado {payment}'

    payment_methods = {
        'PUE': 'PUE - Pago en una sola exhibición',
        'PPD': 'PPD - Pago en parcialidades o diferido',
    }

    return payment_methods.get(payment, default_value)

def get_payment_form(payment):

    default_value=f'Forma de pago no especificada {payment}'
    
    payment_forms = {
        '01': '01 - Efectivo',
        '02': '02 - Cheque nominativo',
        '03': '03 - Transferencia electrónica de fondos',
        '04': '04 - Tarjeta de crédito',
        '05': '05 - Monedero electrónico',
        '06': '06 - Dinero electrónico',
        '08': '08 - Vales de despensa',
        '12': '12 - Dación en pago',
        '13': '13 - Pago por subrogación',
        '14': '14 - Pago por consignación',
        '15': '15 - Condonación',
        '17': '17 - Compensación',
        '23': '23 - Novación',
        '24': '24 - Confusión',
        '25': '25 - Remisión de deuda',
        '26': '26 - Prescripción o caducidad',
        '27': '27 - A satisfacción del acreedor',
        '28': '28 - Tarjeta de débito',
        '29': '29 - Tarjeta de servicios',
        '30': '30 - Aplicación de anticipos',
        '31': '31 - Intermediario pagos',
        '99': '99 - Por definir',
    }

    return payment_forms.get(payment, default_value)

def get_cfdi_type(cfdi):
    
    default_value=f'Tipo de CFDI no especificado {cfdi}'

    cfdi_types = {
        'I': 'I - Ingreso',
        'E': 'E - Egreso',
        'T': 'T - Traslado',
        'P': 'P - Pago',
        'N': 'N - Nómina'
    }

    return cfdi_types.get(cfdi, default_value)

def get_regime_payroll(regime):
    
    default_value=f'Regimen no especificado {regime}'

    regime_types = {
        '02': '02 - Sueldos',
        '03': '03 - Jubilados',
        '04': '04 - Pensionados',
        '09': '09 - Asimilados Honorarios',
        '13': '13 - Indemnización o Separación'
    }

    return regime_types.get(regime, default_value)

def get_related_cfdi_type(type):

    default_value=f'tipo no especificado {type}'

    related_types = {
        '01': '01 - Notas de Crédito de Documentos Relacionados',
        '02': '02 - Notas de Débito de los Documentos Relacionados',
        '03': '03 - Devolución de Mercancías sobre Facturas o Traslados Previos',
        '04': '04 - Sustitución de los CFDI Previos',
        '05': '05 - Traslados de Mercancías Facturados Previamente',
        '06': '06 - Factura Generada por los Traslados Previos',
        '07': '07 - CFDI por Aplicación de Anticipo',
        '08': '08 - Facturas Generadas por Pagos en Parcialidades',
        '09': '09 - Factura Generada por Pagos Diferidos',    
    }

    return related_types.get(type, default_value)

def get_exchange_type(type):

    default_value=f'' # value doesn't exist

    related_types = {
        '01': '01 - MXN',
        '02': '02 - XXX',
    }

    return related_types.get(type, default_value)

def get_DR_taxes_type(type):

    default_value=f'' # value doesn't exist

    taxes_DR = {
        '001': '001 - IVA',
        '002': '002 - ISR',
        '003': '003 - IEPS',
        '004': '004 - Retención de ISR por honorarios',
        '005': '005 - Retención de ISR por arrendamiento',
        '006': '006 - Retención de ISR por servicios profesionales',
        '007': '007 - Retención de ISR por enajenación de bienes',
        '008': '008 - Retención de ISR por intereses',
        '009': '009 - Retención de ISR por dividendos o utilidades',
        '010': '010 - IVA retenido por arrendamiento',
        '011': '011 - IVA retenido por servicios profesionales',
        '012': '012 - IVA retenido por enajenación de bienes',
        '013': '013 - IVA retenido por intereses',
        '014': '014 - IVA retenido por dividendos o utilidades',
        '015': '015 - IVA por traslado de bienes',
        '016': '016 - IVA por servicios profesionales',
        '017': '017 - IVA por servicios de hospedaje',
        '018': '018 - IVA por autotransporte terrestre de carga',
        '019': '019 - IVA por servicios de construcción',
        '020': '020 - IVA por prestación de servicios de arrendamiento de bienes muebles',
        '021': '021 - IVA por servicios de autotransporte terrestre de personas',
        '022': '022 - IVA por servicios de hospedaje',
        '023': '023 - IVA por servicio de comisión mercantil',
        '024': '024 - IVA por servicios de intermediación financiera',
        '025': '025 - IVA por servicios de autotransporte marítimo',
        '026': '026 - IVA por servicios de autotransporte aéreo',
        '027': '027 - IVA por servicios de autotransporte ferroviario',
        '028': '028 - IVA por servicios de mensajería',
    }   
    return taxes_DR.get(type, default_value)

def get_payment_type_p(type):

    default_value=f'' # value doesn't exist
    
    payment_methods_P = {
        '01': '01 - Efectivo',
        '02': '02 - Cheque nominativo',
        '03': '03 - Transferencia electrónica de fondos',
        '04': '04 - Tarjeta de crédito',
        '05': '05 - Monedero electrónico',
        '06': '06 - Dinero electrónico',
        '08': '08 - Vales de despensa',
        '28': '28 - Tarjeta de débito',
        '29': '29 - Tarjeta de servicios',
        '30': '30 - Aplicación de pagos',
        '31': '31 - Domiciliación',
        '32': '32 - Pago por subrogación',
        '33': '33 - Pago por consignación',
        '34': '34 - Condonación',
        '35': '35 - Compensación',
        '36': '36 - Novación',
        '37': '37 - Confusión',
        '38': '38 - Remisión de deuda',
        '39': '39 - Prescripción o caducidad',
        '40': '40 - A satisfacción del acreedor',
        '41': '41 - Tarjeta de débito',
        '42': '42 - Tarjeta de servicios',
        '43': '43 - Aplicación de pagos'
    }
    return payment_methods_P.get(type, default_value)

def get_day_type(type):

    default_value=f'' # value doesn't exist
    
    day_type = {
        '01': '01 - Diurna',
        '02': '02 - Nocturna',
        '03': '03 - Mixta',
        '04': '04 - Por hora',
        '05': '05 - Reducida',
        '06': '06 - Continuada',
        '07': '07 - Partida',
        '08': '08 - Por turnos',
        '09': '09 - Descanso',
        '10': '10 - Días naturales',
        '11': '11 - Indeterminada'
    }

    return day_type.get(type, default_value)

def get_contract_type(type):

    default_value=f'' # value doesn't exist
    
    contract_type = {
        '01': '01 - Contrato a plazo fijo',
        '02': '02 - Contrato a plazo indefinido',
        '03': '03 - Contrato de obra o labor determinada',
        '04': '04 - Contrato de temporada',
        '05': '05 - Contrato eventual',
        '06': '06 - Contrato de aprendizaje',
        '07': '07 - Contrato por jornada parcial',
        '08': '08 - Contrato por jornada completa',
        '09': '09 - Contrato por hora',
        '10': '10 - Contrato de tiempo compartido',
        '11': '11 - Contrato por comisión',
        # Puedes agregar más elementos según tus necesidades
    }

    return contract_type.get(type, default_value)

def get_periodicity_type(type):

    default_value=f'' # value doesn't exist
    
    periodicity_type = {
        '01': '01 - Diario',
        '02': '02 - Semanal',
        '03': '03 - Catorcenal',
        '04': '04 - Mensual',
        '05': '05 - Bimestral',
        '06': '06 - Unidad de obra',
        '07': '07 - Comisión',
        '08': '08 - Precio alzado',
        '09': '09 - Otros',
        # Puedes agregar más elementos según tus necesidades
    }
    return periodicity_type.get(type, default_value)

def get_position_risk_type(type):

    default_value=f'' # value doesn't exist
    
    position_risk_type = {
        '01': '01 - Riesgo mínimo',
        '02': '02 - Riesgo bajo',
        '03': '03 - Riesgo medio',
        '04': '04 - Riesgo alto',
        '05': '05 - Riesgo máximo',
        # Puedes agregar más elementos según tus necesidades
    }

    return position_risk_type.get(type, default_value)