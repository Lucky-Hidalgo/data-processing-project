"""Módulo para realizar el cálculo de los indicadores """
import pandas as pd

# Se considera que una carrera desea recibir el resultado de sus estudiantes #
# si el porcentaje de respuesta es mayor al 5%
TASA_DE_TOLERANCIA  = 0.05

def _formatear_columnas(list):
    # Se cambia el fac por facultad
    list = [c.replace('_fac','_facultad') for c in list]
    # Se eliminan los espacios vacíos
    list = [c.strip().upper().replace('_', ' ') for c in list]
    return list

def _formatear_data_set(data):
    data.fillna(0, inplace=True)
    return data


def guardar_resumen(data, nombre_archivo, nombre_hoja):
    data.columns = _formatear_columnas(data.columns)
    data.to_excel(nombre_archivo + '.xlsx', sheet_name=nombre_hoja[0:30],  index=True)
    return True

def crear_df_carreras(data):
    # Crea dataframe para almacenar resultados, con columnas
    # CARRERA (Index)
    # FACULTAD
    # TOTAL DE ESTUDIANTES
    # Conteo de cada diagnóstico
    diagnosticos = ['RESPONDIÓ_CUESTIONARIO_SOCIOEDUCATIVO',
                    'RESPONDIÓ_MATEMÁTICA_"A"',
                    'RESPONDIÓ_MATEMÁTICA_"B"',
                    'RESPONDIÓ_PENSAMIENTO_CIENTÍFICO',
                    'RESPONDIÓ_ESCRITURA_ACADÉMICA']
    new_df = data.filter(['FACULTAD',
                    'CARRERA',
                    'RESPONDIÓ_CUESTIONARIO_SOCIOEDUCATIVO',
                    'RESPONDIÓ_MATEMÁTICA_"A"',
                    'RESPONDIÓ_MATEMÁTICA_"B"',
                    'RESPONDIÓ_PENSAMIENTO_CIENTÍFICO',
                    'RESPONDIÓ_ESCRITURA_ACADÉMICA'])

    another_df = data.filter(['FACULTAD','CARRERA'])
    
    another_df.drop_duplicates(inplace=True)
    another_df.set_index('CARRERA', drop=True, inplace=True)

    # Se agrega el conteo por carrera
    out = new_df.groupby('CARRERA').agg(
        INSCRITOS = ('CARRERA', 'count')
    )

    out = pd.merge(out, another_df, how='left', on='CARRERA')
    i = 0
    while i < 5 :
        # Se crea una serie con la gente que respondió cada diagnóstico
        aux = new_df.groupby('CARRERA')[diagnosticos[i]].value_counts()
        # Se convierte a DF
        aux = pd.DataFrame(aux)
        # Se cambian los nombres de los índices
        aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
        # Se elimina el multiindice
        aux.reset_index(inplace=True)
        # Se mueve la tabla para que quede como se necesita
        aux  = aux.pivot(index='CARRERA',columns='RESPUESTA', values=diagnosticos[i])
        aux['SI'] = aux['SI'].fillna(0)
        aux['NO'] = aux['NO'].fillna(0)
        aux = aux.astype({'SI':'int32', 'NO': 'int32'})
        
        # Se renombran los indices
        if i == 0 :
            aux = aux.rename(columns={'SI': 'SI_SE', 'NO':'NO_SE'})
        if i == 1 :
            aux = aux.rename(columns={'SI': 'SI_MA', 'NO':'NO_MA'})
        if i == 2 :
            aux = aux.rename(columns={'SI': 'SI_MB', 'NO':'NO_MB'})
        if i == 3 :
            aux = aux.rename(columns={'SI': 'SI_PC', 'NO':'NO_PC'})
        if i == 4 :
            aux = aux.rename(columns={'SI': 'SI_EA', 'NO':'NO_EA'})
        i = i + 1

        out = out.merge(aux, left_index=True, right_index=True)
        
    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = [c.upper() for c in out.columns]
    return out


def crear_df_estadisticas_generales(data, resumen):
    # Función que crea el dataframe con el resumen de las estadísticas generales
    # que sirven para la generación de todos los reportes
    vias_ingreso = ['CUPO BEA',			
                    'CUPO DEPORTE',			
                    'CUPO EXPLORA',			
                    'CUPO HIJO FUNC.',			
                    'CUPO INDIGENA',		
                    'CUPO OFICIO DEMRE',			
                    'CUPO P.S.U',			
                    'CUPO PACE',			
                    'CUPO PARES',			
                    'CUPO PROPEDEUTICO',			
                    'CUPO R850',			
                    'PROSECUCION ESTUDIOS',			
                    'OTROS',			
                    ]

    # SEXO

    # FEMENINO
    aux_data = data[data['SEXO'] == 'FEMENINO']
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['SEXO'].count()
    out = pd.merge(resumen, aux_serie.rename('femenino'), how='left', on='CARRERA')
     
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['SEXO'].count()
    out.reset_index(inplace=True)
   
    out = pd.merge(out, aux_serie.rename('femenino_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['femenino_usach'] = aux_data['SEXO'].count()
    # MASCULINO
    aux_data = data[data['SEXO'] == 'MASCULINO']
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['SEXO'].count()
    out = pd.merge(out, aux_serie.rename('masculino'), how='left', on='CARRERA')
     
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['SEXO'].count()
    out.reset_index(inplace=True)
   
    out = pd.merge(out, aux_serie.rename('masculino_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['masculino_usach'] = aux_data['SEXO'].count()

    # EDAD
    # PENDIENTE AÚN

    # VIA INGRESO
    i = 0
    while i < len(vias_ingreso):
        columna = vias_ingreso[i]
        aux_data = data[data['VIA_INGRESO'] == vias_ingreso[i]] 
        # CARRERA
        aux_serie = aux_data.groupby('CARRERA')['VIA_INGRESO'].count()
        out = pd.merge(out, aux_serie.rename(columna), how='left', on='CARRERA')
        # FACULTAD
        
        aux_serie = aux_data.groupby('FACULTAD')['VIA_INGRESO'].count()
        out.reset_index(inplace=True)
        out = pd.merge(out, aux_serie.rename(columna+'_fac'), how='left', on='FACULTAD')
        out.set_index('CARRERA', inplace=True)
        # USACH
        out[columna + '_usach'] = aux_data['VIA_INGRESO'].count()
        i = i + 1

    # FORMATEAR COLUMNAS PARA SALIDA
    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = [c.upper() for c in out.columns]
    out = _formatear_data_set(out)

    return out


def crear_resumen_socioeducativo(data, resumen):
    # Los cálculos resumidos se hacen para todos, pero solo se agregan
    # a los que alcancen esta tasa mínima
    condicion = resumen['SI_SE'] > resumen['INSCRITOS'] * TASA_DE_TOLERANCIA
    
    carreras_diagnostico = resumen[condicion]

    carreras_diagnostico = carreras_diagnostico.filter(['CARRERA',
                                                        'FACULTAD',
                                                        'INSCRITOS',
                                                        'SI_SE',
                                                        'NO_SE'])

    columnas = list(data.columns)
    columnas =  ['CARRERA', 'FACULTAD'] + columnas[columnas.index('RESPONDIÓ_CUESTIONARIO_SOCIOEDUCATIVO'):columnas.index('RESPONDIÓ_MATEMÁTICA_"A"')]
    aux_data  = data.filter(columnas)

    
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2')
    out = pd.merge(carreras_diagnostico, aux, how='left', on='CARRERA')
    '''
    # FEMENINO
    aux_data = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'] == 'FEMENINO']
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    out = pd.merge(carreras_diagnostico, aux_serie.rename('femenino'), how='left', on='CARRERA')
     
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    out.reset_index(inplace=True)
   
    out = pd.merge(out, aux_serie.rename('femenino_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['femenino_usach'] = aux_data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()

    # MASCULINO
    aux_data = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'] == 'MASCULINO']
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    out = pd.merge(out, aux_serie.rename('masculino'), how='left', on='CARRERA')
     
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    out.reset_index(inplace=True)
   
    out = pd.merge(out, aux_serie.rename('masculino_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['masculino_usach'] = aux_data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()

    # OTRO 
    aux_data = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'] == 'OTRO']
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    out = pd.merge(out, aux_serie.rename('otro'), how='left', on='CARRERA')
     
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    out.reset_index(inplace=True)
    out = pd.merge(out, aux_serie.rename('otro_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['otro_usach'] = aux_data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    '''
    # EDAD 
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_3'].mean()
    out = pd.merge(out, aux_serie.rename('edad'), how='left', on='CARRERA')
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_3'].mean()
    out.reset_index(inplace=True)
    out = pd.merge(out, aux_serie.rename('edad_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['edad_usach'] = aux_data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_3'].mean()

    # NACIONALIDAD
    # Chileno (a)
    aux_data = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'] == 'CHILENO(A)']
    aux_total = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'] != '']
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie2 = aux_total.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie = aux_serie / aux_serie2
    out = pd.merge(out, aux_serie.rename('chileno'), how='left', on='CARRERA')
     
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie2 = aux_total.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie = aux_serie / aux_serie2
    out.reset_index(inplace=True)
    out = pd.merge(out, aux_serie.rename('chileno_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['chileno_usach'] = aux_data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count() / aux_total['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    # Extranjero (a)
    aux_data = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'] != 'CHILENO(A)']
    aux_data = aux_data[aux_data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'] != '']
    # CARRERA
    aux_serie = aux_data.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie2 = aux_total.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie = aux_serie / aux_serie2
    out = pd.merge(out, aux_serie.rename('extranjero'), how='left', on='CARRERA')
     
    # FACULTAD
    aux_serie = aux_data.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie2 = aux_total.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()
    aux_serie = aux_serie / aux_serie2
    out.reset_index(inplace=True)
   
    out = pd.merge(out, aux_serie.rename('extranjero_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['extranjero_usach'] = aux_data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count() / aux_total['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_4'].count()


    return out


def crear_resumen_matematica_a(data, resumen):

    # Los calculos resumidos se hacen para todos, pero solo se agregan 
    # a los que alcancen esta tasa mínima
    condicion = resumen['SI_MA'] > resumen['INSCRITOS'] * TASA_DE_TOLERANCIA
    
    carreras_diagnostico = resumen[condicion]
    # TODO EN RESUMEN CALCULAR LOS CUPOS CON VALUES COUNT Y AGREGARLOS AL REPORTE 
    carreras_diagnostico = carreras_diagnostico.filter(['CARRERA',
                                                        'FACULTAD',
                                                        'INSCRITOS',
                                                        'SI_MA',
                                                        'NO_MA']
                                                        )
    

    aux_data = data.filter(['CARRERA',
                            'FACULTAD',
                            'PUNTAJE_TOTAL_(MA)',
                            'PORCENTAJE_DE_LOGRO_(MA)',
                            'OBJETIVO_1_(MA)',
                            'OBJETIVO_2_(MA)',
                            'OBJETIVO_3_(MA)',
                            'OBJETIVO_4_(MA)',
                            'OBJETIVO_5_(MA)',
                            'OBJETIVO_6_(MA)',
                            'OBJETIVO_7_(MA)',
                            'OBJETIVO_8_(MA)',
                            'OBJETIVO_9_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_6_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_7_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_8_(MA)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_9_(MA)',
                            'EJE_TEMÁTICO_1_(MA)',
                            'EJE_TEMÁTICO_2_(MA)',
                            'EJE_TEMÁTICO_3_(MA)',
                            'EJE_TEMÁTICO_4_(MA)',
                            'PORCENTAJE_DE_LOGRO_EJE_1_(MA)',
                            'PORCENTAJE_DE_LOGRO_EJE_2_(MA)',
                            'PORCENTAJE_DE_LOGRO_EJE_3_(MA)',
                            'PORCENTAJE_DE_LOGRO_EJE_4_(MA)'
                            ])
    
    calculos_x_facultad = aux_data.groupby('FACULTAD').agg(
        # Puntaje promedio de la facultad
        puntaje_total_promedio_fac = ('PUNTAJE_TOTAL_(MA)', 'mean'),
        # Porcentaje de logro promedio de la facultad
        porcentaje_de_logro_promedio_fac = ('PORCENTAJE_DE_LOGRO_(MA)', 'mean'),
        
        # Porcentaje de logro x eje temático por facultad 
        porcentaje_promedio_eje_1_fac = ('PORCENTAJE_DE_LOGRO_EJE_1_(MA)', 'mean'),
        porcentaje_promedio_eje_2_fac = ('PORCENTAJE_DE_LOGRO_EJE_2_(MA)', 'mean'),
        porcentaje_promedio_eje_3_fac = ('PORCENTAJE_DE_LOGRO_EJE_3_(MA)', 'mean'),
        porcentaje_promedio_eje_4_fac = ('PORCENTAJE_DE_LOGRO_EJE_4_(MA)', 'mean'),
        # Porcentaje de logro x objetivo por facultad
        porcentaje_promedio_obj_1_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MA)', 'mean'),
        porcentaje_promedio_obj_2_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MA)', 'mean'),
        porcentaje_promedio_obj_3_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MA)', 'mean'),
        porcentaje_promedio_obj_4_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MA)', 'mean'),
        porcentaje_promedio_obj_5_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MA)', 'mean'),
        porcentaje_promedio_obj_6_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_6_(MA)', 'mean'),
        porcentaje_promedio_obj_7_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_7_(MA)', 'mean'),
        porcentaje_promedio_obj_8_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_8_(MA)', 'mean'),
        porcentaje_promedio_obj_9_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_9_(MA)', 'mean')
    )

    out = aux_data.groupby('CARRERA').agg(
        # Puntaje promedio de la carrera
        puntaje_total_promedio = ('PUNTAJE_TOTAL_(MA)', 'mean'),
        # Porcentaje de logro promedio
        porcentaje_de_logro_promedio = ('PORCENTAJE_DE_LOGRO_(MA)', 'mean'),
        # Porcentaje de logro x eje temático por carrera 
        porcentaje_promedio_eje_1 = ('PORCENTAJE_DE_LOGRO_EJE_1_(MA)', 'mean'),
        porcentaje_promedio_eje_2 = ('PORCENTAJE_DE_LOGRO_EJE_2_(MA)', 'mean'),
        porcentaje_promedio_eje_3 = ('PORCENTAJE_DE_LOGRO_EJE_3_(MA)', 'mean'),
        porcentaje_promedio_eje_4 = ('PORCENTAJE_DE_LOGRO_EJE_4_(MA)', 'mean'),
        # Porcentaje de logro x objetivo por carrera
        porcentaje_promedio_obj_1 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MA)', 'mean'),
        porcentaje_promedio_obj_2 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MA)', 'mean'),
        porcentaje_promedio_obj_3 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MA)', 'mean'),
        porcentaje_promedio_obj_4 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MA)', 'mean'),
        porcentaje_promedio_obj_5 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MA)', 'mean'),
        porcentaje_promedio_obj_6 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_6_(MA)', 'mean'),
        porcentaje_promedio_obj_7 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_7_(MA)', 'mean'),
        porcentaje_promedio_obj_8 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_8_(MA)', 'mean'),
        porcentaje_promedio_obj_9 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_9_(MA)', 'mean')
               
    )
    # Se calculan los valores para todos los datos del conjunto
    puntaje_total_promedio_usach = aux_data['PUNTAJE_TOTAL_(MA)'].mean()
    porcentaje_de_logro_usach = aux_data['PORCENTAJE_DE_LOGRO_(MA)'].mean()
    # Porcentaje de logro x eje temático total 
    porcentaje_promedio_eje_1_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_1_(MA)'].mean()
    porcentaje_promedio_eje_2_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_2_(MA)'].mean()
    porcentaje_promedio_eje_3_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_3_(MA)'].mean()
    porcentaje_promedio_eje_4_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_4_(MA)'].mean()
    # Porcentaje de logro x objetivo total
    porcentaje_promedio_obj_1_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MA)'].mean()
    porcentaje_promedio_obj_2_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MA)'].mean()
    porcentaje_promedio_obj_3_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MA)'].mean()
    porcentaje_promedio_obj_4_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MA)'].mean()
    porcentaje_promedio_obj_5_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MA)'].mean()
    porcentaje_promedio_obj_6_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_6_(MA)'].mean()
    porcentaje_promedio_obj_7_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_7_(MA)'].mean()
    porcentaje_promedio_obj_8_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_8_(MA)'].mean()
    porcentaje_promedio_obj_9_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_9_(MA)'].mean()

    # Se agregan los valores globales de la usach como columna en cada caso
    out['puntaje_total_promedio_usach'] = puntaje_total_promedio_usach
    out['porcentaje_logro_promedio_usach'] = porcentaje_de_logro_usach
    out['porcentaje_promedio_eje_1_usach'] = porcentaje_promedio_eje_1_usach
    out['porcentaje_promedio_eje_2_usach'] = porcentaje_promedio_eje_2_usach
    out['porcentaje_promedio_eje_3_usach'] = porcentaje_promedio_eje_3_usach
    out['porcentaje_promedio_eje_4_usach'] = porcentaje_promedio_eje_4_usach
    out['porcentaje_promedio_obj_1_usach'] = porcentaje_promedio_obj_1_usach
    out['porcentaje_promedio_obj_2_usach'] = porcentaje_promedio_obj_2_usach
    out['porcentaje_promedio_obj_3_usach'] = porcentaje_promedio_obj_3_usach
    out['porcentaje_promedio_obj_4_usach'] = porcentaje_promedio_obj_4_usach
    out['porcentaje_promedio_obj_5_usach'] = porcentaje_promedio_obj_5_usach
    out['porcentaje_promedio_obj_6_usach'] = porcentaje_promedio_obj_6_usach
    out['porcentaje_promedio_obj_7_usach'] = porcentaje_promedio_obj_7_usach
    out['porcentaje_promedio_obj_8_usach'] = porcentaje_promedio_obj_8_usach
    out['porcentaje_promedio_obj_9_usach'] = porcentaje_promedio_obj_9_usach

    # Se calculan los valores de diferencia con la usach
    diferencia_puntaje_total_usach = out['puntaje_total_promedio'] - puntaje_total_promedio_usach
    diferencia_porcentaje_de_logro_usach = out['porcentaje_de_logro_promedio'] - porcentaje_de_logro_usach 
    diferencia_promedio_eje_1_usach = out['porcentaje_promedio_eje_1'] - porcentaje_promedio_eje_1_usach
    diferencia_promedio_eje_2_usach = out['porcentaje_promedio_eje_2'] - porcentaje_promedio_eje_2_usach
    diferencia_promedio_eje_3_usach = out['porcentaje_promedio_eje_3'] - porcentaje_promedio_eje_3_usach
    diferencia_promedio_eje_4_usach = out['porcentaje_promedio_eje_4'] - porcentaje_promedio_eje_4_usach
    diferencia_promedio_obj_1_usach = out['porcentaje_promedio_obj_1'] - porcentaje_promedio_obj_1_usach
    diferencia_promedio_obj_2_usach = out['porcentaje_promedio_obj_2'] - porcentaje_promedio_obj_2_usach
    diferencia_promedio_obj_3_usach = out['porcentaje_promedio_obj_3'] - porcentaje_promedio_obj_3_usach
    diferencia_promedio_obj_4_usach = out['porcentaje_promedio_obj_4'] - porcentaje_promedio_obj_4_usach
    diferencia_promedio_obj_5_usach = out['porcentaje_promedio_obj_5'] - porcentaje_promedio_obj_5_usach
    diferencia_promedio_obj_6_usach = out['porcentaje_promedio_obj_6'] - porcentaje_promedio_obj_6_usach
    diferencia_promedio_obj_7_usach = out['porcentaje_promedio_obj_7'] - porcentaje_promedio_obj_7_usach
    diferencia_promedio_obj_8_usach = out['porcentaje_promedio_obj_8'] - porcentaje_promedio_obj_8_usach
    diferencia_promedio_obj_9_usach = out['porcentaje_promedio_obj_9'] - porcentaje_promedio_obj_9_usach
    

    
    # Se agregan las diferencias con los valores globales de la Universidad
    out = pd.merge(out, diferencia_puntaje_total_usach.rename('DIFERENCIA_PUNTAJE_TOTAL_USACH'), how='left', on='CARRERA')
    out = pd.merge(out, diferencia_porcentaje_de_logro_usach.rename('DIFERENCIA_PORCENTAJE_DE_LOGRO_USACH'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_1_usach.rename('diferencia_promedio_eje_1_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_2_usach.rename('diferencia_promedio_eje_2_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_3_usach.rename('diferencia_promedio_eje_3_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_4_usach.rename('diferencia_promedio_eje_4_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_1_usach.rename('diferencia_promedio_obj_1_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_2_usach.rename('diferencia_promedio_obj_2_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_3_usach.rename('diferencia_promedio_obj_3_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_4_usach.rename('diferencia_promedio_obj_4_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_5_usach.rename('diferencia_promedio_obj_5_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_6_usach.rename('diferencia_promedio_obj_6_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_7_usach.rename('diferencia_promedio_obj_7_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_8_usach.rename('diferencia_promedio_obj_8_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_9_usach.rename('diferencia_promedio_obj_9_usach'), how='left', on='CARRERA')


    # Se realiza el merge solo con las carreras a las que les interesa la información
    out = pd.merge(carreras_diagnostico, out, how='left', on='CARRERA')
    out.reset_index(inplace=True)
   
    out = pd.merge(out, calculos_x_facultad, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # Calcular diferencia con FACULTADES
    out['diferencia_puntaje_total_fac'] = out['puntaje_total_promedio'] - out['puntaje_total_promedio_fac']
    out['diferencia_porcentaje_de_logro_fac'] = out['porcentaje_de_logro_promedio'] - out['porcentaje_de_logro_promedio_fac']

    out['diferencia_promedio_eje_1_fac'] = out['porcentaje_promedio_eje_1'] - out['porcentaje_promedio_eje_1_fac']
    out['diferencia_promedio_eje_2_fac'] = out['porcentaje_promedio_eje_2'] - out['porcentaje_promedio_eje_2_fac']
    out['diferencia_promedio_eje_3_fac'] = out['porcentaje_promedio_eje_3'] - out['porcentaje_promedio_eje_3_fac']
    out['diferencia_promedio_eje_4_fac'] = out['porcentaje_promedio_eje_4'] - out['porcentaje_promedio_eje_4_fac']
    out['diferencia_promedio_obj_1_fac'] = out['porcentaje_promedio_obj_1'] - out['porcentaje_promedio_obj_1_fac']
    out['diferencia_promedio_obj_2_fac'] = out['porcentaje_promedio_obj_2'] - out['porcentaje_promedio_obj_2_fac']
    out['diferencia_promedio_obj_3_fac'] = out['porcentaje_promedio_obj_3'] - out['porcentaje_promedio_obj_3_fac']
    out['diferencia_promedio_obj_4_fac'] = out['porcentaje_promedio_obj_4'] - out['porcentaje_promedio_obj_4_fac']
    out['diferencia_promedio_obj_5_fac'] = out['porcentaje_promedio_obj_5'] - out['porcentaje_promedio_obj_5_fac']
    out['diferencia_promedio_obj_6_fac'] = out['porcentaje_promedio_obj_6'] - out['porcentaje_promedio_obj_6_fac']
    out['diferencia_promedio_obj_7_fac'] = out['porcentaje_promedio_obj_7'] - out['porcentaje_promedio_obj_7_fac']
    out['diferencia_promedio_obj_8_fac'] = out['porcentaje_promedio_obj_8'] - out['porcentaje_promedio_obj_8_fac']
    out['diferencia_promedio_obj_9_fac'] = out['porcentaje_promedio_obj_9'] - out['porcentaje_promedio_obj_9_fac']

    # CALCULAR CANTIDAD DE CASOS CRITICOS
    
    new_aux_data = aux_data[aux_data['PORCENTAJE_DE_LOGRO_(MA)'] < 0.6]
    
    estudiantes_con_puntaje_bajo = new_aux_data.groupby('CARRERA')['PORCENTAJE_DE_LOGRO_(MA)'].count()
    
    out = pd.merge(out,estudiantes_con_puntaje_bajo.rename('estudiantes_con_puntaje_bajo'), how='left', on='CARRERA')
    out['porcentaje_estudiantes_con_puntaje_bajo'] = out['estudiantes_con_puntaje_bajo'] / out['INSCRITOS']
    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = [c.upper() for c in out.columns]
    out = _formatear_data_set(out)
    return out


def crear_resumen_matematica_b(data, resumen):

    # Los calculos resumidos se hacen para todos, pero solo se agregan 
    # a los que alcancen esta tasa mínima
    condicion = resumen['SI_MB'] > resumen['INSCRITOS'] * TASA_DE_TOLERANCIA
    
    carreras_diagnostico = resumen[condicion]
    # TODO EN RESUMEN CALCULAR LOS CUPOS CON VALUES COUNT Y AGREGARLOS AL REPORTE 
    carreras_diagnostico = carreras_diagnostico.filter(['CARRERA',
                                                        'FACULTAD',
                                                        'INSCRITOS',
                                                        'SI_MB',
                                                        'NO_MB']
                                                        )
    

    aux_data = data.filter(['CARRERA',
                            'FACULTAD',
                            'PUNTAJE_TOTAL_(MB)',
                            'PORCENTAJE_DE_LOGRO_(MB)',
                            'OBJETIVO_1_(MB)',
                            'OBJETIVO_2_(MB)',
                            'OBJETIVO_3_(MB)',
                            'OBJETIVO_4_(MB)',
                            'OBJETIVO_5_(MB)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MB)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MB)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MB)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MB)',
                            'PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MB)',
                            'EJE_TEMÁTICO_1_(MB)',
                            'EJE_TEMÁTICO_2_(MB)',
                            'EJE_TEMÁTICO_3_(MB)',
                            'EJE_TEMÁTICO_4_(MB)',
                            'PORCENTAJE_DE_LOGRO_EJE_1_(MB)',
                            'PORCENTAJE_DE_LOGRO_EJE_2_(MB)',
                            'PORCENTAJE_DE_LOGRO_EJE_3_(MB)',
                            'PORCENTAJE_DE_LOGRO_EJE_4_(MB)'
                            ])
    
    calculos_x_facultad = aux_data.groupby('FACULTAD').agg(
        # Puntaje promedio de la facultad
        puntaje_total_promedio_fac = ('PUNTAJE_TOTAL_(MB)', 'mean'),
        # Porcentaje de logro promedio de la facultad
        porcentaje_de_logro_promedio_fac = ('PORCENTAJE_DE_LOGRO_(MB)', 'mean'),
        
        # Porcentaje de logro x eje temático por facultad 
        porcentaje_promedio_eje_1_fac = ('PORCENTAJE_DE_LOGRO_EJE_1_(MB)', 'mean'),
        porcentaje_promedio_eje_2_fac = ('PORCENTAJE_DE_LOGRO_EJE_2_(MB)', 'mean'),
        porcentaje_promedio_eje_3_fac = ('PORCENTAJE_DE_LOGRO_EJE_3_(MB)', 'mean'),
        porcentaje_promedio_eje_4_fac = ('PORCENTAJE_DE_LOGRO_EJE_4_(MB)', 'mean'),
        # Porcentaje de logro x objetivo por facultad
        porcentaje_promedio_obj_1_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MB)', 'mean'),
        porcentaje_promedio_obj_2_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MB)', 'mean'),
        porcentaje_promedio_obj_3_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MB)', 'mean'),
        porcentaje_promedio_obj_4_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MB)', 'mean'),
        porcentaje_promedio_obj_5_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MB)', 'mean')

    )

    out = aux_data.groupby('CARRERA').agg(
        # Puntaje promedio de la carrera
        puntaje_total_promedio = ('PUNTAJE_TOTAL_(MB)', 'mean'),
        # Porcentaje de logro promedio
        porcentaje_de_logro_promedio = ('PORCENTAJE_DE_LOGRO_(MB)', 'mean'),
        # Porcentaje de logro x eje temático por carrera 
        porcentaje_promedio_eje_1 = ('PORCENTAJE_DE_LOGRO_EJE_1_(MB)', 'mean'),
        porcentaje_promedio_eje_2 = ('PORCENTAJE_DE_LOGRO_EJE_2_(MB)', 'mean'),
        porcentaje_promedio_eje_3 = ('PORCENTAJE_DE_LOGRO_EJE_3_(MB)', 'mean'),
        porcentaje_promedio_eje_4 = ('PORCENTAJE_DE_LOGRO_EJE_4_(MB)', 'mean'),
        # Porcentaje de logro x objetivo por carrera
        porcentaje_promedio_obj_1 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MB)', 'mean'),
        porcentaje_promedio_obj_2 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MB)', 'mean'),
        porcentaje_promedio_obj_3 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MB)', 'mean'),
        porcentaje_promedio_obj_4 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MB)', 'mean'),
        porcentaje_promedio_obj_5 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MB)', 'mean')
               
    )
    # Se calculan los valores para todos los datos del conjunto
    puntaje_total_promedio_usach = aux_data['PUNTAJE_TOTAL_(MB)'].mean()
    porcentaje_de_logro_usach = aux_data['PORCENTAJE_DE_LOGRO_(MB)'].mean()
    # Porcentaje de logro x eje temático total 
    porcentaje_promedio_eje_1_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_1_(MB)'].mean()
    porcentaje_promedio_eje_2_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_2_(MB)'].mean()
    porcentaje_promedio_eje_3_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_3_(MB)'].mean()
    porcentaje_promedio_eje_4_usach = aux_data['PORCENTAJE_DE_LOGRO_EJE_4_(MB)'].mean()
    # Porcentaje de logro x objetivo total
    porcentaje_promedio_obj_1_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_1_(MB)'].mean()
    porcentaje_promedio_obj_2_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_2_(MB)'].mean()
    porcentaje_promedio_obj_3_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_3_(MB)'].mean()
    porcentaje_promedio_obj_4_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_4_(MB)'].mean()
    porcentaje_promedio_obj_5_usach = aux_data['PORCENTAJE_DE_LOGRO_OBJETIVO_5_(MB)'].mean()


    # Se agregan los valores globales de la usach como columna en cada caso
    out['puntaje_total_promedio_usach'] = puntaje_total_promedio_usach
    out['porcentaje_logro_promedio_usach'] = porcentaje_de_logro_usach
    out['porcentaje_promedio_eje_1_usach'] = porcentaje_promedio_eje_1_usach
    out['porcentaje_promedio_eje_2_usach'] = porcentaje_promedio_eje_2_usach
    out['porcentaje_promedio_eje_3_usach'] = porcentaje_promedio_eje_3_usach
    out['porcentaje_promedio_eje_4_usach'] = porcentaje_promedio_eje_4_usach
    out['porcentaje_promedio_obj_1_usach'] = porcentaje_promedio_obj_1_usach
    out['porcentaje_promedio_obj_2_usach'] = porcentaje_promedio_obj_2_usach
    out['porcentaje_promedio_obj_3_usach'] = porcentaje_promedio_obj_3_usach
    out['porcentaje_promedio_obj_4_usach'] = porcentaje_promedio_obj_4_usach
    out['porcentaje_promedio_obj_5_usach'] = porcentaje_promedio_obj_5_usach


    # Se calculan los valores de diferencia con la usach
    diferencia_puntaje_total_usach = out['puntaje_total_promedio'] - puntaje_total_promedio_usach
    diferencia_porcentaje_de_logro_usach = out['porcentaje_de_logro_promedio'] - porcentaje_de_logro_usach 
    diferencia_promedio_eje_1_usach = out['porcentaje_promedio_eje_1'] - porcentaje_promedio_eje_1_usach
    diferencia_promedio_eje_2_usach = out['porcentaje_promedio_eje_2'] - porcentaje_promedio_eje_2_usach
    diferencia_promedio_eje_3_usach = out['porcentaje_promedio_eje_3'] - porcentaje_promedio_eje_3_usach
    diferencia_promedio_eje_4_usach = out['porcentaje_promedio_eje_4'] - porcentaje_promedio_eje_4_usach
    diferencia_promedio_obj_1_usach = out['porcentaje_promedio_obj_1'] - porcentaje_promedio_obj_1_usach
    diferencia_promedio_obj_2_usach = out['porcentaje_promedio_obj_2'] - porcentaje_promedio_obj_2_usach
    diferencia_promedio_obj_3_usach = out['porcentaje_promedio_obj_3'] - porcentaje_promedio_obj_3_usach
    diferencia_promedio_obj_4_usach = out['porcentaje_promedio_obj_4'] - porcentaje_promedio_obj_4_usach
    diferencia_promedio_obj_5_usach = out['porcentaje_promedio_obj_5'] - porcentaje_promedio_obj_5_usach

    # Se agregan las diferencias con los valores globales de la Universidad
    out = pd.merge(out, diferencia_puntaje_total_usach.rename('DIFERENCIA_PUNTAJE_TOTAL_USACH'), how='left', on='CARRERA')
    out = pd.merge(out, diferencia_porcentaje_de_logro_usach.rename('DIFERENCIA_PORCENTAJE_DE_LOGRO_USACH'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_1_usach.rename('diferencia_promedio_eje_1_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_2_usach.rename('diferencia_promedio_eje_2_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_3_usach.rename('diferencia_promedio_eje_3_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_eje_4_usach.rename('diferencia_promedio_eje_4_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_1_usach.rename('diferencia_promedio_obj_1_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_2_usach.rename('diferencia_promedio_obj_2_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_3_usach.rename('diferencia_promedio_obj_3_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_4_usach.rename('diferencia_promedio_obj_4_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_obj_5_usach.rename('diferencia_promedio_obj_5_usach'), how='left', on='CARRERA')



    # Se realiza el merge solo con las carreras a las que les interesa la información
    out = pd.merge(carreras_diagnostico, out, how='left', on='CARRERA')
    out.reset_index(inplace=True)
   
    out = pd.merge(out, calculos_x_facultad, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # Calcular diferencia con FACULTADES
    out['diferencia_puntaje_total_fac'] = out['puntaje_total_promedio'] - out['puntaje_total_promedio_fac']
    out['diferencia_porcentaje_de_logro_fac'] = out['porcentaje_de_logro_promedio'] - out['porcentaje_de_logro_promedio_fac']

    out['diferencia_promedio_eje_1_fac'] = out['porcentaje_promedio_eje_1'] - out['porcentaje_promedio_eje_1_fac']
    out['diferencia_promedio_eje_2_fac'] = out['porcentaje_promedio_eje_2'] - out['porcentaje_promedio_eje_2_fac']
    out['diferencia_promedio_eje_3_fac'] = out['porcentaje_promedio_eje_3'] - out['porcentaje_promedio_eje_3_fac']
    out['diferencia_promedio_eje_4_fac'] = out['porcentaje_promedio_eje_4'] - out['porcentaje_promedio_eje_4_fac']
    out['diferencia_promedio_obj_1_fac'] = out['porcentaje_promedio_obj_1'] - out['porcentaje_promedio_obj_1_fac']
    out['diferencia_promedio_obj_2_fac'] = out['porcentaje_promedio_obj_2'] - out['porcentaje_promedio_obj_2_fac']
    out['diferencia_promedio_obj_3_fac'] = out['porcentaje_promedio_obj_3'] - out['porcentaje_promedio_obj_3_fac']
    out['diferencia_promedio_obj_4_fac'] = out['porcentaje_promedio_obj_4'] - out['porcentaje_promedio_obj_4_fac']
    out['diferencia_promedio_obj_5_fac'] = out['porcentaje_promedio_obj_5'] - out['porcentaje_promedio_obj_5_fac']

    # CALCULAR CANTIDAD DE CASOS CRITICOS
    
    new_aux_data = aux_data[aux_data['PORCENTAJE_DE_LOGRO_(MB)'] < 0.6]
    
    estudiantes_con_puntaje_bajo = new_aux_data.groupby('CARRERA')['PORCENTAJE_DE_LOGRO_(MB)'].count()
    
    out = pd.merge(out,estudiantes_con_puntaje_bajo.rename('estudiantes_con_puntaje_bajo'), how='left', on='CARRERA')
    out['porcentaje_estudiantes_con_puntaje_bajo'] = out['estudiantes_con_puntaje_bajo'] / out['INSCRITOS']
    # CAMBIAR VALORES NAN POR 0s
    out = _formatear_data_set(out)
    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = [c.upper() for c in out.columns]
    return out


def crear_resumen_pensamiento_cientifico(data, resumen):
    # Los calculos resumidos se hacen para todos, pero solo se agregan 
    # a los que alcancen esta tasa mínima
    condicion = resumen['SI_PC'] > resumen['INSCRITOS'] * TASA_DE_TOLERANCIA
    
    carreras_diagnostico = resumen[condicion]
    # TODO EN RESUMEN CALCULAR LOS CUPOS CON VALUES COUNT Y AGREGARLOS AL REPORTE 
    carreras_diagnostico = carreras_diagnostico.filter(['CARRERA',
                                                        'FACULTAD',
                                                        'INSCRITOS',
                                                        'SI_PC',
                                                        'NO_PC']
                                                        )
    

    aux_data = data.filter(['CARRERA',
                            'FACULTAD',
                            'PUNTAJE_TOTAL_(PC)',
                            'PORCENTAJE_DE_LOGRO_(PC)',
                            'PENSAMIENTO_CIENTÍFICO_DIMENSIÓN_1',
                            'PENSAMIENTO_CIENTÍFICO_DIMENSIÓN_2',
                            'PENSAMIENTO_CIENTÍFICO_DIMENSIÓN_3',
                            'PENSAMIENTO_CIENTÍFICO_DIMENSIÓN_4',
                            'PENSAMIENTO_CIENTÍFICO_DIMENSIÓN_5',
                            'PORCENTAJE_LOGRO_DIMENSIÓN_1_PC',
                            'PORCENTAJE_LOGRO_DIMENSIÓN_2_PC',
                            'PORCENTAJE_LOGRO_DIMENSIÓN_3_PC',
                            'PORCENTAJE_LOGRO_DIMENSIÓN_4_PC',
                            'PORCENTAJE_LOGRO_DIMENSIÓN_5_PC',
                            'PENSAMIENTO_CIENTÍFICO_CATEGORÍA'

                            ])

    calculos_x_facultad = aux_data.groupby('FACULTAD').agg(
        # Puntaje promedio de la facultad
        puntaje_total_promedio_fac = ('PUNTAJE_TOTAL_(PC)', 'mean'),
        # Porcentaje de logro promedio de la facultad
        porcentaje_de_logro_promedio_fac = ('PORCENTAJE_DE_LOGRO_(PC)', 'mean'),
        
        # Porcentaje de logro x dimensión temático por facultad 
        porcentaje_promedio_dim_1_fac = ('PORCENTAJE_LOGRO_DIMENSIÓN_1_PC', 'mean'),
        porcentaje_promedio_dim_2_fac = ('PORCENTAJE_LOGRO_DIMENSIÓN_2_PC', 'mean'),
        porcentaje_promedio_dim_3_fac = ('PORCENTAJE_LOGRO_DIMENSIÓN_3_PC', 'mean'),
        porcentaje_promedio_dim_4_fac = ('PORCENTAJE_LOGRO_DIMENSIÓN_4_PC', 'mean'),
        porcentaje_promedio_dim_5_fac = ('PORCENTAJE_LOGRO_DIMENSIÓN_5_PC', 'mean'),
    )

    out = aux_data.groupby('CARRERA').agg(
        # Puntaje promedio de la carrera
        puntaje_total_promedio = ('PUNTAJE_TOTAL_(PC)', 'mean'),
        # Porcentaje de logro promedio de la carrera
        porcentaje_de_logro_promedio = ('PORCENTAJE_DE_LOGRO_(PC)', 'mean'),
        
        # Porcentaje de logro x dimensión de la carrera 
        porcentaje_promedio_dim_1 = ('PORCENTAJE_LOGRO_DIMENSIÓN_1_PC', 'mean'),
        porcentaje_promedio_dim_2 = ('PORCENTAJE_LOGRO_DIMENSIÓN_2_PC', 'mean'),
        porcentaje_promedio_dim_3 = ('PORCENTAJE_LOGRO_DIMENSIÓN_3_PC', 'mean'),
        porcentaje_promedio_dim_4 = ('PORCENTAJE_LOGRO_DIMENSIÓN_4_PC', 'mean'),
        porcentaje_promedio_dim_5 = ('PORCENTAJE_LOGRO_DIMENSIÓN_5_PC', 'mean'),
    )

    # Se calculan los valores para todos los datos del conjunto
    puntaje_total_promedio_usach = aux_data['PUNTAJE_TOTAL_(PC)'].mean()
    porcentaje_de_logro_usach = aux_data['PORCENTAJE_DE_LOGRO_(PC)'].mean()
    # Porcentaje de logro x eje temático total 
    porcentaje_promedio_dim_1_usach = aux_data['PORCENTAJE_LOGRO_DIMENSIÓN_1_PC'].mean()
    porcentaje_promedio_dim_2_usach = aux_data['PORCENTAJE_LOGRO_DIMENSIÓN_2_PC'].mean()
    porcentaje_promedio_dim_3_usach = aux_data['PORCENTAJE_LOGRO_DIMENSIÓN_3_PC'].mean()
    porcentaje_promedio_dim_4_usach = aux_data['PORCENTAJE_LOGRO_DIMENSIÓN_4_PC'].mean()
    porcentaje_promedio_dim_5_usach = aux_data['PORCENTAJE_LOGRO_DIMENSIÓN_5_PC'].mean()

    # Se calculan los valores de diferencia con la usach
    diferencia_puntaje_total_usach = out['puntaje_total_promedio'] - puntaje_total_promedio_usach
    diferencia_porcentaje_de_logro_usach = out['porcentaje_de_logro_promedio'] - porcentaje_de_logro_usach 
    diferencia_promedio_dim_1_usach = out['porcentaje_promedio_dim_1'] - porcentaje_promedio_dim_1_usach
    diferencia_promedio_dim_2_usach = out['porcentaje_promedio_dim_2'] - porcentaje_promedio_dim_2_usach
    diferencia_promedio_dim_3_usach = out['porcentaje_promedio_dim_3'] - porcentaje_promedio_dim_3_usach
    diferencia_promedio_dim_4_usach = out['porcentaje_promedio_dim_4'] - porcentaje_promedio_dim_4_usach
    diferencia_promedio_dim_5_usach = out['porcentaje_promedio_dim_5'] - porcentaje_promedio_dim_5_usach

    # Se agregan las diferencias con los valores globales de la Universidad
    out = pd.merge(out, diferencia_puntaje_total_usach.rename('DIFERENCIA_PUNTAJE_TOTAL_USACH'), how='left', on='CARRERA')
    out = pd.merge(out, diferencia_porcentaje_de_logro_usach.rename('DIFERENCIA_PORCENTAJE_DE_LOGRO_USACH'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_1_usach.rename('diferencia_promedio_dim_1_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_2_usach.rename('diferencia_promedio_dim_2_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_3_usach.rename('diferencia_promedio_dim_3_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_4_usach.rename('diferencia_promedio_dim_4_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_5_usach.rename('diferencia_promedio_dim_5_usach'), how='left', on='CARRERA')

    # Se realiza el merge solo con las carreras a las que les interesa la información
    out = pd.merge(carreras_diagnostico, out, how='left', on='CARRERA')
    out.reset_index(inplace=True)
   
    out = pd.merge(out, calculos_x_facultad, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # Calcular diferencia con FACULTADES
    out['diferencia_puntaje_total_fac'] = out['puntaje_total_promedio'] - out['puntaje_total_promedio_fac']
    out['diferencia_porcentaje_de_logro_fac'] = out['porcentaje_de_logro_promedio'] - out['porcentaje_de_logro_promedio_fac']

    out['diferencia_promedio_dim_1_fac'] = out['porcentaje_promedio_dim_1'] - out['porcentaje_promedio_dim_1_fac']
    out['diferencia_promedio_dim_2_fac'] = out['porcentaje_promedio_dim_2'] - out['porcentaje_promedio_dim_2_fac']
    out['diferencia_promedio_dim_3_fac'] = out['porcentaje_promedio_dim_3'] - out['porcentaje_promedio_dim_3_fac']
    out['diferencia_promedio_dim_4_fac'] = out['porcentaje_promedio_dim_4'] - out['porcentaje_promedio_dim_4_fac']
    out['diferencia_promedio_dim_5_fac'] = out['porcentaje_promedio_dim_5'] - out['porcentaje_promedio_dim_5_fac']

    # CALCULAR CANTIDAD DE ESTUDIANTES DE CADA CATEGORÍA DE PENSAMIENTO CIENTÍFICO
    # Concretos
    new_aux_data = aux_data[aux_data['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'] == 'Concreto']
    # CARRERA
    concretos = new_aux_data.groupby('CARRERA')['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()
    out = pd.merge(out, concretos.rename('concreto'), how='left', on='CARRERA')
     
    # FACULTAD
    concretos_fac = new_aux_data.groupby('FACULTAD')['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()
    out.reset_index(inplace=True)
   
    out = pd.merge(out, concretos_fac.rename('concreto_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['concreto_usach'] = new_aux_data['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()

    # Transicional
    new_aux_data = aux_data[aux_data['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'] == 'Transicional']
    # CARRERA
    transicionales = new_aux_data.groupby('CARRERA')['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()
    out = pd.merge(out, transicionales.rename('transicional'), how='left', on='CARRERA')
     
    # FACULTAD
    transicionales_fac = new_aux_data.groupby('FACULTAD')['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()
    out.reset_index(inplace=True)
   
    out = pd.merge(out, transicionales_fac.rename('transicional_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['transicional_usach'] = new_aux_data['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()

    # Formal
    new_aux_data = aux_data[aux_data['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'] == 'Formal']
    # CARRERA
    formales = new_aux_data.groupby('CARRERA')['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()
    out = pd.merge(out, formales.rename('formal'), how='left', on='CARRERA')
     
    # FACULTAD
    formales_fac = new_aux_data.groupby('FACULTAD')['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()
    out.reset_index(inplace=True)
   
    out = pd.merge(out, formales_fac.rename('formal_fac'), how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # USACH
    out['formal_usach'] = new_aux_data['PENSAMIENTO_CIENTÍFICO_CATEGORÍA'].count()

    # CALCULAR CANTIDAD DE CASOS CRITICOS
    
    new_aux_data = aux_data[aux_data['PORCENTAJE_DE_LOGRO_(PC)'] < 0.6]
    
    estudiantes_con_puntaje_bajo = new_aux_data.groupby('CARRERA')['PORCENTAJE_DE_LOGRO_(PC)'].count()
    
    out = pd.merge(out,estudiantes_con_puntaje_bajo.rename('estudiantes_con_puntaje_bajo'), how='left', on='CARRERA')
    out['porcentaje_estudiantes_con_puntaje_bajo'] = out['estudiantes_con_puntaje_bajo'] / out['INSCRITOS']
    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = [c.upper() for c in out.columns]
    out = _formatear_data_set(out)
    return out


def crear_resumen_escritura_academica(data, resumen):

    # Los calculos resumidos se hacen para todos, pero solo se agregan 
    # a los que alcancen esta tasa mínima
    condicion = resumen['SI_EA'] > resumen['INSCRITOS'] * TASA_DE_TOLERANCIA
    
    carreras_diagnostico = resumen[condicion]
    # TODO EN RESUMEN CALCULAR LOS CUPOS CON VALUES COUNT Y AGREGARLOS AL REPORTE 
    carreras_diagnostico = carreras_diagnostico.filter(['CARRERA',
                                                        'FACULTAD',
                                                        'INSCRITOS',
                                                        'SI_EA',
                                                        'NO_EA']
                                                        )
    

    aux_data = data.filter(['CARRERA',
                            'FACULTAD',
                            'PUNTAJE_TOTAL_(EA)',
                            'PORCENTAJE_DE_LOGRO_(EA)',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_1_EA',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_2_EA',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_3_EA',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_4_EA',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_5_EA',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_6_EA',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_7_EA',
                            'PORCENTAJE_DE_LOGRO_DIMENSIÓN_8_EA'
                            ])

    calculos_x_facultad = aux_data.groupby('FACULTAD').agg(
        # Puntaje promedio de la facultad
        puntaje_total_promedio_fac = ('PUNTAJE_TOTAL_(EA)', 'mean'),
        # Porcentaje de logro promedio de la facultad
        porcentaje_de_logro_promedio_fac = ('PORCENTAJE_DE_LOGRO_(EA)', 'mean'),
        
        # Porcentaje de logro x dimensión temático por facultad 
        porcentaje_promedio_dim_1_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_1_EA', 'mean'),
        porcentaje_promedio_dim_2_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_2_EA', 'mean'),
        porcentaje_promedio_dim_3_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_3_EA', 'mean'),
        porcentaje_promedio_dim_4_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_4_EA', 'mean'),
        porcentaje_promedio_dim_5_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_5_EA', 'mean'),
        porcentaje_promedio_dim_6_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_6_EA', 'mean'),
        porcentaje_promedio_dim_7_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_7_EA', 'mean'),
        porcentaje_promedio_dim_8_fac = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_8_EA', 'mean')
    )

    out = aux_data.groupby('CARRERA').agg(
        # Puntaje promedio de la carrera
        puntaje_total_promedio = ('PUNTAJE_TOTAL_(EA)', 'mean'),
        # Porcentaje de logro promedio de la carrera
        porcentaje_de_logro_promedio = ('PORCENTAJE_DE_LOGRO_(EA)', 'mean'),
        
        # Porcentaje de logro x dimensión de la carrera 
        
        porcentaje_promedio_dim_1 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_1_EA', 'mean'),
        porcentaje_promedio_dim_2 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_2_EA', 'mean'),
        porcentaje_promedio_dim_3 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_3_EA', 'mean'),
        porcentaje_promedio_dim_4 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_4_EA', 'mean'),
        porcentaje_promedio_dim_5 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_5_EA', 'mean'),
        porcentaje_promedio_dim_6 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_6_EA', 'mean'),
        porcentaje_promedio_dim_7 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_7_EA', 'mean'),
        porcentaje_promedio_dim_8 = ('PORCENTAJE_DE_LOGRO_DIMENSIÓN_8_EA', 'mean')
    )

    # Se calculan los valores para todos los datos del conjunto
    puntaje_total_promedio_usach = aux_data['PUNTAJE_TOTAL_(EA)'].mean()
    porcentaje_de_logro_usach = aux_data['PORCENTAJE_DE_LOGRO_(EA)'].mean()
    # Porcentaje de logro x eje temático total 
    porcentaje_promedio_dim_1_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_1_EA'].mean()
    porcentaje_promedio_dim_2_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_2_EA'].mean()
    porcentaje_promedio_dim_3_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_3_EA'].mean()
    porcentaje_promedio_dim_4_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_4_EA'].mean()
    porcentaje_promedio_dim_5_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_5_EA'].mean()
    porcentaje_promedio_dim_6_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_6_EA'].mean()
    porcentaje_promedio_dim_7_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_7_EA'].mean()
    porcentaje_promedio_dim_8_usach = aux_data['PORCENTAJE_DE_LOGRO_DIMENSIÓN_8_EA'].mean()

    # Se calculan los valores de diferencia con la usach
    diferencia_puntaje_total_usach = out['puntaje_total_promedio'] - puntaje_total_promedio_usach
    diferencia_porcentaje_de_logro_usach = out['porcentaje_de_logro_promedio'] - porcentaje_de_logro_usach 
    diferencia_promedio_dim_1_usach = out['porcentaje_promedio_dim_1'] - porcentaje_promedio_dim_1_usach
    diferencia_promedio_dim_2_usach = out['porcentaje_promedio_dim_2'] - porcentaje_promedio_dim_2_usach
    diferencia_promedio_dim_3_usach = out['porcentaje_promedio_dim_3'] - porcentaje_promedio_dim_3_usach
    diferencia_promedio_dim_4_usach = out['porcentaje_promedio_dim_4'] - porcentaje_promedio_dim_4_usach
    diferencia_promedio_dim_5_usach = out['porcentaje_promedio_dim_5'] - porcentaje_promedio_dim_5_usach
    diferencia_promedio_dim_6_usach = out['porcentaje_promedio_dim_6'] - porcentaje_promedio_dim_6_usach
    diferencia_promedio_dim_7_usach = out['porcentaje_promedio_dim_7'] - porcentaje_promedio_dim_7_usach
    diferencia_promedio_dim_8_usach = out['porcentaje_promedio_dim_8'] - porcentaje_promedio_dim_8_usach


    # Se agregan las diferencias con los valores globales de la Universidad
    out = pd.merge(out, diferencia_puntaje_total_usach.rename('DIFERENCIA_PUNTAJE_TOTAL_USACH'), how='left', on='CARRERA')
    out = pd.merge(out, diferencia_porcentaje_de_logro_usach.rename('DIFERENCIA_PORCENTAJE_DE_LOGRO_USACH'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_1_usach.rename('diferencia_promedio_dim_1_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_2_usach.rename('diferencia_promedio_dim_2_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_3_usach.rename('diferencia_promedio_dim_3_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_4_usach.rename('diferencia_promedio_dim_4_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_5_usach.rename('diferencia_promedio_dim_5_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_6_usach.rename('diferencia_promedio_dim_6_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_7_usach.rename('diferencia_promedio_dim_7_usach'), how='left', on='CARRERA')
    out = pd.merge(out,diferencia_promedio_dim_8_usach.rename('diferencia_promedio_dim_8_usach'), how='left', on='CARRERA')

    # Se realiza el merge solo con las carreras a las que les interesa la información
    out = pd.merge(carreras_diagnostico, out, how='left', on='CARRERA')
    out.reset_index(inplace=True)
   
    out = pd.merge(out, calculos_x_facultad, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # Calcular diferencia con FACULTADES
    out['diferencia_puntaje_total_fac'] = out['puntaje_total_promedio'] - out['puntaje_total_promedio_fac']
    out['diferencia_porcentaje_de_logro_fac'] = out['porcentaje_de_logro_promedio'] - out['porcentaje_de_logro_promedio_fac']

    out['diferencia_promedio_dim_1_fac'] = out['porcentaje_promedio_dim_1'] - out['porcentaje_promedio_dim_1_fac']
    out['diferencia_promedio_dim_2_fac'] = out['porcentaje_promedio_dim_2'] - out['porcentaje_promedio_dim_2_fac']
    out['diferencia_promedio_dim_3_fac'] = out['porcentaje_promedio_dim_3'] - out['porcentaje_promedio_dim_3_fac']
    out['diferencia_promedio_dim_4_fac'] = out['porcentaje_promedio_dim_4'] - out['porcentaje_promedio_dim_4_fac']
    out['diferencia_promedio_dim_5_fac'] = out['porcentaje_promedio_dim_5'] - out['porcentaje_promedio_dim_5_fac']
    out['diferencia_promedio_dim_6_fac'] = out['porcentaje_promedio_dim_6'] - out['porcentaje_promedio_dim_6_fac']
    out['diferencia_promedio_dim_7_fac'] = out['porcentaje_promedio_dim_7'] - out['porcentaje_promedio_dim_7_fac']
    out['diferencia_promedio_dim_8_fac'] = out['porcentaje_promedio_dim_8'] - out['porcentaje_promedio_dim_8_fac']
    
    # CALCULAR CANTIDAD DE CASOS CRITICOS
    
    new_aux_data = aux_data[aux_data['PORCENTAJE_DE_LOGRO_(EA)'] < 0.6]
    
    estudiantes_con_puntaje_bajo = new_aux_data.groupby('CARRERA')['PORCENTAJE_DE_LOGRO_(EA)'].count()
    
    out = pd.merge(out,estudiantes_con_puntaje_bajo.rename('estudiantes_con_puntaje_bajo'), how='left', on='CARRERA')
    out['porcentaje_estudiantes_con_puntaje_bajo'] = out['estudiantes_con_puntaje_bajo'] / out['INSCRITOS']
    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = [c.upper() for c in out.columns]
    out = _formatear_data_set(out)
    return out
