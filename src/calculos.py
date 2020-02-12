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
        # Se crea una serie con la gente que respondió el socioeducativo
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
        

    
    return out


def resumen_matematica_a(data, resumen):

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
        porcentaje_promedio_obj_8_fac = ('PORCENTAJE_DE_LOGRO_OBJETIVO_8_(MA)', 'mean')
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
        porcentaje_promedio_obj_8 = ('PORCENTAJE_DE_LOGRO_OBJETIVO_8_(MA)', 'mean')
               
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

    # Se agregan los valores globales de la usach como columna en cada caso
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

    # CALCULAR CANTIDAD DE CASOS CRITICOS
    
    new_aux_data = aux_data[aux_data['PORCENTAJE_DE_LOGRO_(MA)'] < 0.6]
    
    estudiantes_con_puntaje_bajo = new_aux_data.groupby('CARRERA')['PORCENTAJE_DE_LOGRO_(MA)'].count()
    
    out = pd.merge(out,estudiantes_con_puntaje_bajo.rename('estudiantes_con_puntaje_bajo'), how='left', on='CARRERA')
    out['porcentaje_estudiantes_con_puntaje_bajo'] = out['estudiantes_con_puntaje_bajo'] / out['INSCRITOS']
    # FORMATEAR COLUMNAS PARA SALIDA
    out.columns = _formatear_columnas(out.columns)
    return out


