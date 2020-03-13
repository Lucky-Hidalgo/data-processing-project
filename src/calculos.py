"""Módulo para realizar el cálculo de los indicadores """
import pandas as pd

# Se considera que una carrera desea recibir el resultado de sus estudiantes #
# si el porcentaje de respuesta es mayor al 5%
TASA_DE_TOLERANCIA  = 0.05

def _formatear_columnas(lista):
    lista = [c.strip().lower() for c in lista]
    # Se cambia el fac por facultad
    lista = [c.replace('_fac','_facultad') for c in lista]
    # Se eliminan los espacios vacíos
    lista = [c.strip().upper().replace('_', ' ') for c in lista]
    return lista

def _formatear_data_set(data):
    data.fillna(0, inplace=True)
    data.drop_duplicates(inplace=True)
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


def procesar_socioeducativo_preguntas_1_20(data, resumen):
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
    columnas =  ['CARRERA', 'FACULTAD', 'VIA_DE_INGRESO', 'PROMEDIO_PSU', 'PUNTAJE_RANKING'] + columnas[columnas.index('RESPONDIÓ_CUESTIONARIO_SOCIOEDUCATIVO'):columnas.index('CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20') + 1]
    aux_data  = data.filter(columnas)

    ###########################################################################
    # ASPECTOS SOCIODEMOGRÁFICOS
    ###########################################################################

    # SEXO
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2')
    out = pd.merge(carreras_diagnostico, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2')
    aux = aux.rename(columns={'FEMENINO': 'FEMENINO_FAC', 'MASCULINO':'MASCULINO_FAC', 'OTRO': 'OTRO_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']=='FEMENINO']
    out['FEMENINO_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']=='MASCULINO']
    out['MASCULINO_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2']=='OTRO']
    out['OTRO_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_2'].count() / aux_total

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

    # REGION DE ORIGEN
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5')
    aux = aux.rename(columns={'SÍ': 'VIVIA_EN_RM', 'NO': 'NO_VIVIA_EN_RM'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5')
    aux = aux.rename(columns={'SÍ': 'VIVIA_EN_RM_FAC', 'NO':'NO_VIVIA_EN_RN_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5']=='SÍ']
    out['VIVIA_EN_RM_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5']=='NO']
    out['NO_VIVIA_EN_RM_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5'].count() / aux_total

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

    # PERTENECE A PUEBLO ORIGINARIO
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6')
    aux = aux.rename(columns={'SÍ': 'SI_CERTIFICADO_CONADI', 
                            'NO, PERO PERTENEZCO A UN PUEBLO ORIGINARIO.': 'NO_CERTIFICADO_CONADI',
                            'NO POSEO CERTIFICADO, NI PERTENEZCO A UN PUEBLO ORIGINARIO.': 'NO_PUEBLO_ORIGINARIO'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6')
    aux = aux.rename(columns={'SÍ': 'SI_CERTIFICADO_CONADI_FAC', 
                            'NO, PERO PERTENEZCO A UN PUEBLO ORIGINARIO.': 'NO_CERTIFICADO_CONADI_FAC',
                            'NO POSEO CERTIFICADO, NI PERTENEZCO A UN PUEBLO ORIGINARIO.': 'NO_PUEBLO_ORIGINARIO_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_5']=='SÍ']
    out['SI_CERTIFICADO_CONADI_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6']=='NO, PERO PERTENEZCO A UN PUEBLO ORIGINARIO.']
    out['NO_CERTIFICADO_CONADI_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6']=='NO POSEO CERTIFICADO, NI PERTENEZCO A UN PUEBLO ORIGINARIO.']
    out['NO_PUEBLO_ORIGINARIO_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_6'].count() / aux_total

    # REGISTRO DE DISCAPACIDAD
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7')
    aux = aux.rename(columns={'SÍ': 'TIENE_REGISTRO_DISCAPACIDAD', 'NO': 'NO_TIENE_REGISTRO_DISCAPACIDAD'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7')
    aux = aux.rename(columns={'SÍ': 'TIENE_REGISTRO_DISCAPACIDAD_FAC', 'NO': 'NO_TIENE_REGISTRO_DISCAPACIDAD_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7']=='SÍ']
    out['TIENE_REGISTRO_DISCAPACIDAD_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7']=='NO']
    out['NO_TIENE_REGISTRO_DISCAPACIDAD_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_7'].count() / aux_total

    # DIFICULTADES DE AUTONOMÍA
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8')
    aux = aux.rename(columns={'SÍ': 'INFORMA_DIFICULTADES_DE_AUTONOMÍA', 'NO': 'NO_INFORMA_DIFICULTADES_DE_AUTONOMÍA'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8')
    aux = aux.rename(columns={'SÍ': 'INFORMA_DIFICULTADES_DE_AUTONOMÍA_FAC', 'NO': 'NO_INFORMA_DIFICULTADES_DE_AUTONOMÍA_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8']=='SÍ']
    out['INFORMA_DIFICULTADES_DE_AUTONOMÍA_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8']=='NO']
    out['NO_INFORMA_DIFICULTADES_DE_AUTONOMÍA_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_8'].count() / aux_total

    #############################################################
    #   SITUACIÓN FAMILIAR Y ECONÓMICA DEL ESTUDIANTE
    #############################################################
    # TIENE HIJOS
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9')
    aux = aux.rename(columns={'SÍ': 'TIENE_HIJOS', 'NO': 'NO_TIENE_HIJOS'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9')
    aux = aux.rename(columns={'SÍ': 'TIENE_HIJOS_FAC', 'NO':'NO_TIENE_HIJOS_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9']=='SÍ']
    out['TIENE_HIJOS_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9']=='NO']
    out['NO_TIENE_HIJOS_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_9'].count() / aux_total

    # TIENE FAMILIARES QUE DEMANDEN ASISTENCIA
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10')
    aux = aux.rename(columns={'SÍ': 'TIENE_FAMILIARES_DEPENDIENTES', 
                                'NO': 'NO_TIENE_FAMILIARES_DEPENDIENTES'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10')
    aux = aux.rename(columns={'SÍ': 'TIENE_FAMILIARES_DEPENDIENTES_FAC', 
                                'NO':'NO_TIENE_FAMILIARES_DEPENDIENTES_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10']=='SÍ']
    out['TIENE_FAMILIARES_DEPENDIENTES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10']=='NO']
    out['NO_TIENE_FAMILIARES_DEPENDIENTES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_10'].count() / aux_total

    # TIENE ESTUDIOS SUPERIORES
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11')
    aux = aux.rename(columns={'SÍ': 'TIENE_ESTUDIOS_SUPERIORES', 
                                'NO': 'NO_TIENE_ESTUDIOS_SUPERIORES'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11')
    aux = aux.rename(columns={'SÍ': 'TIENE_ESTUDIOS_SUPERIORES_FAC', 
                                'NO':'NO_TIENE_ESTUDIOS_SUPERIORES_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='SÍ']
    out['TIENE_ESTUDIOS_SUPERIORES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='NO']
    out['NO_TIENE_ESTUDIOS_SUPERIORES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11'].count() / aux_total

    # DONDE TIENE ESTUDIOS SUPERIORES
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='SÍ']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12')
    aux = aux.rename(columns={'EN ESTA MISMA UNIVERSIDAD': 'ESTUDIO_EN_LA_USACH', 
                                'EN OTRA UNIVERSIDAD': 'ESTUDIÓ_EN_OTRA_UNIVERSIDAD',
                                'EN UN CENTRO DE FORMACIÓN TÉCNICA (CFT) O INSTITUTO PROFESIONAL (IP)': 'ESTUDIÓ_EN_IP_O_CFT',
                                'EN OTRA INSTITUCIÓN DE EDUCACIÓN SUPERIOR': 'ESTUDIÓ_EN_OTRO'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='SÍ']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12')
    aux = aux.rename(columns={'EN ESTA MISMA UNIVERSIDAD': 'ESTUDIO_EN_LA_USACH_FAC', 
                                'EN OTRA UNIVERSIDAD': 'ESTUDIÓ_EN_OTRA_UNIVERSIDAD_FAC',
                                'EN UN CENTRO DE FORMACIÓN TÉCNICA (CFT) O INSTITUTO PROFESIONAL (IP)': 'ESTUDIÓ_EN_IP_O_CFT_FAC',
                                'EN OTRA INSTITUCIÓN DE EDUCACIÓN SUPERIOR': 'ESTUDIÓ_EN_OTRO_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='SÍ']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12']=='EN ESTA MISMA UNIVERSIDAD']
    out['ESTUDIO_EN_LA_USACH_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='SÍ']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12']=='EN OTRA UNIVERSIDAD']
    out['ESTUDIÓ_EN_OTRA_UNIVERSIDAD_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='SÍ']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12']=='EN UN CENTRO DE FORMACIÓN TÉCNICA (CFT) O INSTITUTO PROFESIONAL (IP)']
    out['ESTUDIÓ_EN_IP_O_CFT_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_11']=='SÍ']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12']=='EN OTRA INSTITUCIÓN DE EDUCACIÓN SUPERIOR']
    out['ESTUDIÓ_EN_OTRO_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_12'].count() / aux_total

    # PADRES CON EDUCACIÓN SUPERIOR
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13')
    aux = aux.rename(columns={'SÍ': 'PADRES_TIENEN_ESTUDIOS_SUPERIORES', 
                                'NO': 'PADRES_NO_TIENEN_ESTUDIOS_SUPERIORES'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13')
    aux = aux.rename(columns={'SÍ': 'PADRES_TIENEN_ESTUDIOS_SUPERIORES_FAC', 
                                'NO':'PADRES_NO_TIENEN_ESTUDIOS_SUPERIORES_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13']=='SÍ']
    out['PADRES_TIENEN_ESTUDIOS_SUPERIORES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13']=='NO']
    out['PADRES_NO_TIENEN_ESTUDIOS_SUPERIORES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_13'].count() / aux_total

    # CON QUIÉN VIVIRÁS DURANTE EL AÑO ACADÉMICO
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15')
    aux = aux.rename(columns={'CON MI MADRE Y - O MI PADRE': 'VIVIRA_CON_SUS_PADRES', 
                               'CON OTRO FAMILIAR CERCANO (POR EJ. ABUELOS - AS, HERMANOS - AS, TÍOS - AS)' : 'VIVIRA_CON_FAMILIARES',
                               'CON MI PAREJA O AMIGOS - AS' : 'VIVIRA_CON_PAREJA_O_AMIGOS',
                               'SOLO - A' : 'VIVIRA_SOLO',
                               'CON OTRAS PERSONAS NO CERCANAS (POR EJ. PENSIÓN)': 'VIVIRA_SIN_PERSONAS_CERCANAS'})

    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15')
    aux = aux.rename(columns={'CON MI MADRE Y - O MI PADRE': 'VIVIRA_CON_SUS_PADRES_FAC', 
                               'CON OTRO FAMILIAR CERCANO (POR EJ. ABUELOS - AS, HERMANOS - AS, TÍOS - AS)' : 'VIVIRA_CON_FAMILIARES_FAC',
                               'CON MI PAREJA O AMIGOS - AS' : 'VIVIRA_CON_PAREJA_O_AMIGOS_FAC',
                               'SOLO - A' : 'VIVIRA_SOLO_FAC',
                               'CON OTRAS PERSONAS NO CERCANAS (POR EJ. PENSIÓN)': 'VIVIRA_SIN_PERSONAS_CERCANAS_FAC'})

    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']=='CON MI MADRE Y - O MI PADRE']
    out['VIVIRA_CON_SUS_PADRES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']=='CON OTRO FAMILIAR CERCANO (POR EJ. ABUELOS - AS, HERMANOS - AS, TÍOS - AS)']
    out['VIVIRA_CON_FAMILIARES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].count() / aux_total


    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']=='CON MI PAREJA O AMIGOS - AS']
    out['VIVIRA_CON_PAREJA_O_AMIGOS_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].count() / aux_total


    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']=='SOLO - A']
    out['VIVIRA_SOLO_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].count() / aux_total


    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15']=='CON OTRAS PERSONAS NO CERCANAS (POR EJ. PENSIÓN)']
    out['VIVIRA_SIN_PERSONAS_CERCANAS_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].count() / aux_total


    # SOSTÉN ECONÓMICO DEL HOGAR
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14')
    aux = aux.rename(columns={'MI MADRE Y - O MI PADRE': 'SUS_PADRES_SOSTIENEN_EL_HOGAR', 
                               'UN FAMILIAR CERCANO (POR EJ. ABUELOS - AS, HERMANOS - AS, TÍOS - AS)' : 'FAMILIARES_SOSTIENEN_EL_HOGAR',
                               'YO' : 'EL_SOSTIENE_EL_HOGAR',
                               'OTRO' : 'OTRO_SOSTIENE_EL_HOGAR'})

    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14')
    aux = aux.rename(columns={'MI MADRE Y - O MI PADRE': 'SUS_PADRES_SOSTIENEN_EL_HOGAR_FAC', 
                               'UN FAMILIAR CERCANO (POR EJ. ABUELOS - AS, HERMANOS - AS, TÍOS - AS)' : 'FAMILIARES_SOSTIENEN_EL_HOGAR_FAC',
                               'YO' : 'EL_SOSTIENE_EL_HOGAR_FAC',
                               'OTRO' : 'OTRO_SOSTIENE_EL_HOGAR_FAC'})

    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']=='MI MADRE Y - O MI PADRE']
    out['SUS_PADRES_SOSTIENEN_EL_HOGAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']=='UN FAMILIAR CERCANO (POR EJ. ABUELOS - AS, HERMANOS - AS, TÍOS - AS)']
    out['FAMILIARES_SOSTIENEN_EL_HOGAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14'].count() / aux_total


    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']=='YO']
    out['EL_SOSTIENE_EL_HOGAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14'].count() / aux_total


    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_14']=='OTRO']
    out['OTRO_SOSTIENE_EL_HOGAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_15'].count() / aux_total

    # TIENES PENSADO TRABAJAR
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18')
    aux = aux.rename(columns={'SÍ': 'TIENE_PENSADO_TRABAJAR', 
                                'NO': 'NO_TIENE_PENSADO_TRABAJAR'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18')
    aux = aux.rename(columns={'SÍ': 'TIENE_PENSADO_TRABAJAR_FAC', 
                                'NO': 'NO_TIENE_PENSADO_TRABAJAR_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    out['TIENE_PENSADO_TRABAJAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='NO']
    out['NO_TIENE_PENSADO_TRABAJAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18'].count() / aux_total


    # MOTIVOS PARA TRABAJAR
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19')
    aux = aux.rename(columns={'NECESITO SOSTENER ECONÓMICAMENTE A MI FAMILIA O HIJO(A)': 'SOSTENER_ECONOMICAMENTE_FAMILIA', 
                                'NECESITO FINANCIAR MIS ESTUDIOS': 'FINANCIAR_MIS_ESTUDIOS',
                                'NECESITO APORTAR ECONÓMICAMENTE A MI HOGAR' : 'APORTAR_AL_HOGAR',
                                'NECESITO COSTEAR GASTOS PERSONALES (TRANSPORTE, VESTIMENTA, ALIMENTACIÓN, ESPARCIMIENTO)': 'COSTEAR_GASTOS_PERSONALES',
                                'OTRO MOTIVO' : 'OTRO_MOTIVO'})
    out = pd.merge(out, aux, how='left', on='CARRERA')




    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19')
    aux = aux.rename(columns={'NECESITO SOSTENER ECONÓMICAMENTE A MI FAMILIA O HIJO(A)': 'SOSTENER_ECONOMICAMENTE_FAMILIA_FAC', 
                                'NECESITO FINANCIAR MIS ESTUDIOS': 'FINANCIAR_MIS_ESTUDIOS_FAC',
                                'NECESITO APORTAR ECONÓMICAMENTE A MI HOGAR' : 'APORTAR_AL_HOGAR_FAC',
                                'NECESITO COSTEAR GASTOS PERSONALES (TRANSPORTE, VESTIMENTA, ALIMENTACIÓN, ESPARCIMIENTO)': 'COSTEAR_GASTOS_PERSONALES_FAC',
                                'OTRO MOTIVO' : 'OTRO_MOTIVO_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']=='NECESITO SOSTENER ECONÓMICAMENTE A MI FAMILIA O HIJO(A)']
    out['SOSTENER_ECONOMICAMENTE_FAMILIA_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']=='NECESITO FINANCIAR MIS ESTUDIOS']
    out['FINANCIAR_MIS_ESTUDIOS_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']=='NECESITO APORTAR ECONÓMICAMENTE A MI HOGAR']
    out['APORTAR_AL_HOGAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']=='NECESITO COSTEAR GASTOS PERSONALES (TRANSPORTE, VESTIMENTA, ALIMENTACIÓN, ESPARCIMIENTO)']
    out['COSTEAR_GASTOS_PERSONALES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].count() / aux_total


    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_18']=='SÍ']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']=='OTRO MOTIVO']
    out['OTRO_MOTIVO_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].count() / aux_total

    # MOTIVO MÁS COMÚN
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].agg(lambda x:x.value_counts().index[0])
    aux = pd.DataFrame(aux)
    
    aux = aux.rename(columns={'CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19': 'MOTIVO_MAS_COMUN'})

    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].agg(lambda x:x.value_counts().index[0])
    aux = pd.DataFrame(aux)
    
    aux = aux.rename(columns={'CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19': 'MOTIVO_MAS_COMUN_FAC'})
    out.reset_index(inplace=True)
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19']!='']
    out['MOTIVO_MAS_COMUN_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_19'].value_counts().idxmax()
    

    ######################################################################################
    # RENDIMIENTO ACADÉMICO PREVIO, CONDICIONES PARA EL ESTUDIO Y VINCULACIÓN SOCIAL
    ######################################################################################
    # VIA DE INGRESO 
    

    # PUNTAJE_PSU Y RANKING
    # CARRERA
    aux_data = data.filter(columnas)
    aux_data = aux_data.groupby('CARRERA').agg(
        # Puntaje promedio de la carrera
        puntaje_promedio_psu = ('PROMEDIO_PSU', 'mean'),
        puntaje_promedio_ranking = ('PUNTAJE_RANKING', 'mean')
        )
    out = pd.merge(out, aux_data, how='left', on='CARRERA')
    
    
    # FACULTAD
    aux_data = data.filter(columnas)
    aux_data = aux_data.groupby('FACULTAD').agg(
        # Puntaje promedio de la carrera
        puntaje_promedio_psu_fac = ('PROMEDIO_PSU', 'mean'),
        puntaje_promedio_ranking_fac = ('PUNTAJE_RANKING', 'mean')
        )
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux_data, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)

    # USACH
    out['PROMEDIO_PSU_USACH'] = data['PROMEDIO_PSU'].mean()
    out['PUNTAJE_RANKING_USACH'] = data['PUNTAJE_RANKING'].mean()

    # ESPACIO DE ESTUDIO
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16')
    aux = aux.rename(columns={'SÍ': 'TIENE_ESPACIO_PARA_ESTUDIAR', 
                                'NO': 'NO_TIENE_ESPACIO_PARA_ESTUDIAR'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16')
    aux = aux.rename(columns={'SÍ': 'TIENE_ESPACIO_PARA_ESTUDIAR_FAC', 
                                'NO': 'NO_TIENE_ESPACIO_PARA_ESTUDIAR_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16']=='SÍ']
    out['TIENE_ESPACIO_PARA_ESTUDIAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16']=='NO']
    out['NO_TIENE_ESPACIO_PARA_ESTUDIAR_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_16'].count() / aux_total

    # ACCESO A INTERNET
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17')
    aux = aux.rename(columns={'SÍ': 'TIENE_ACCESO_A_INTERNET', 
                                'NO': 'NO_TIENE_ACCESO_A_INTERNET'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17')
    aux = aux.rename(columns={'SÍ': 'TIENE_ACCESO_A_INTERNET_FAC', 
                                'NO': 'NO_TIENE_ACCESO_A_INTERNET_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17']=='SÍ']
    out['TIENE_ACCESO_A_INTERNET_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17']=='NO']
    out['NO_TIENE_ACCESO_A_INTERNET_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_17'].count() / aux_total

    
    # PARTICIPA EN ORGANIZACIONES
    # CARRERA
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20']!='']
    aux = aux.groupby('CARRERA')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='CARRERA', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20')
    aux = aux.rename(columns={'SÍ': 'PARTICIPA_EN_ORGANIZACIONES', 
                                'NO': 'NO_PARTICIPA_EN_ORGANIZACIONES'})
    out = pd.merge(out, aux, how='left', on='CARRERA')

    # FACULTAD
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20']!='']
    aux = aux.groupby('FACULTAD')['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20'].value_counts(normalize=True)
    aux = pd.DataFrame(aux)
    aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
    aux.reset_index(inplace=True)
    aux = aux.pivot(index='FACULTAD', 
                    columns='RESPUESTA', 
                    values='CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20')
    aux = aux.rename(columns={'SÍ': 'PARTICIPA_EN_ORGANIZACIONES_FAC', 
                                'NO': 'NO_PARTICIPA_EN_ORGANIZACIONES_FAC'})
    out.reset_index(inplace=True)
    
    out = pd.merge(out, aux, how='left', on='FACULTAD', left_index=True)

    out.set_index('CARRERA', inplace=True)

    # USACH 
    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20']!='']
    aux_total = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20'].count()
    
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20']=='SÍ']
    out['PARTICIPA_EN_ORGANIZACIONES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20'].count() / aux_total

    aux = data[data['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20']!='']
    aux = aux[aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20']=='NO']
    out['NO_PARTICIPA_EN_ORGANIZACIONES_USACH'] = aux['CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20'].count() / aux_total


    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = _formatear_columnas(out.columns)
    out = _formatear_data_set(out)
    return out

def procesar_socioeducativo_preguntas_21_67(data, resumen):
    # Los cálculos resumidos se hacen para todos, pero solo se agregan
    # a los que alcancen esta tasa mínima
    condicion = resumen['SI_SE'] > resumen['INSCRITOS'] * TASA_DE_TOLERANCIA
    
    carreras_diagnostico = resumen[condicion]

    carreras_diagnostico = carreras_diagnostico.filter(['CARRERA',
                                                        'FACULTAD'])
    columnas = list(data.columns)
    
    columnas =  ['CARRERA', 'FACULTAD'] \
        + columnas[columnas.index('CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_21'):columnas.index('CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_67') + 1]
    aux_data = data.filter(columnas)
    out = carreras_diagnostico
    i = 21
    while i <= 67 :
        pregunta = 'CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_' + str(i)
        nombre_columna = 'MEDIA_PREGUNTA_' + str(i)
        # Elimino los nulos
        aux = aux_data[aux_data[pregunta]!='']
        # Calculo el promedio para las carreras
        promedio = aux.groupby('CARRERA')[pregunta].mean()
        out = pd.merge(out, promedio.rename(nombre_columna), how='left', on='CARRERA')
        i = i + 1
    aux_facultades = carreras_diagnostico
    
    i = 21
    while i <= 67 :
        pregunta = 'CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_' + str(i)
        nombre_columna = 'MEDIA_PREGUNTA_' + str(i) + '_FAC'
        # Elimino los nulos
        aux = aux_data[aux_data[pregunta]!='']
        # Calculo el promedio para las carreras
        promedio = aux.groupby('FACULTAD')[pregunta].mean()
        aux_facultades = pd.merge(aux_facultades, promedio.rename(nombre_columna), how='left', on='FACULTAD')
        i = i + 1

    out.reset_index(inplace=True)
    out = pd.merge(out, aux_facultades, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)

    i = 21
    while i <= 67 :
        pregunta = 'CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_' + str(i)
        nombre_columna = 'MEDIA_PREGUNTA_' + str(i) + '_USACH'
        # Elimino los nulos
        aux = aux_data[aux_data[pregunta]!='']
        # Calculo el promedio para las carreras
        out[nombre_columna] = aux[pregunta].mean()
        
        i = i + 1
    out.drop_duplicates(inplace=True)

    # ENCONTRAR MÁXIMOS POR CATEGORÍA
    # PROBLEMAS EN LA TRANSICION
    columnas = list(out.columns)
    inicio_categoria = columnas.index('MEDIA_PREGUNTA_21')
    fin_categoria = columnas.index('MEDIA_PREGUNTA_30')
    columnas = ['CARRERA'] + columnas[inicio_categoria: fin_categoria + 1]
    filtrado = out.filter(columnas)
    out['MAXIMO_PROBLEMAS_EN_LA_TRANSICION'] = filtrado.idxmax(axis=1)

    # PREFERENCIAS DE ESTRATEGIAS DE ENSEÑANZA
    columnas = list(out.columns)
    inicio_categoria = columnas.index('MEDIA_PREGUNTA_48')
    fin_categoria = columnas.index('MEDIA_PREGUNTA_51')
    columnas = ['CARRERA'] + columnas[inicio_categoria: fin_categoria + 1]
    filtrado = out.filter(columnas)
    out['MAXIMO_ESTRATEGIAS_DE_ENSEÑANZA'] = filtrado.idxmax(axis=1)

    # PREPARACIÓN TICS
    columnas = list(out.columns)
    inicio_categoria = columnas.index('MEDIA_PREGUNTA_64')
    fin_categoria = columnas.index('MEDIA_PREGUNTA_67')
    columnas = ['CARRERA'] + columnas[inicio_categoria: fin_categoria + 1]
    filtrado = out.filter(columnas)
    out['MAXIMO_PREPARACION_TICS'] = filtrado.idxmax(axis=1)

    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = _formatear_columnas(out.columns)
    out = _formatear_data_set(out)

    return out

def procesar_socioeducativo_escalas_autorreporte(data, resumen):
    # Los cálculos resumidos se hacen para todos, pero solo se agregan
    # a los que alcancen esta tasa mínima
    condicion = resumen['SI_SE'] > resumen['INSCRITOS'] * TASA_DE_TOLERANCIA
    
    carreras_diagnostico = resumen[condicion]

    carreras_diagnostico = carreras_diagnostico.filter(['CARRERA',
                                                        'FACULTAD'])

    columnas = list(data.columns)
    
    columnas =  ['CARRERA', 'FACULTAD', 'VIA_DE_INGRESO', 'PROMEDIO_PSU', 'PUNTAJE_RANKING'] + columnas[columnas.index('CUESTIONARIO_SOCIOEDUCATIVO_PREGUNTA_20'):columnas.index('NIVEL_ESCALA_USO_ACADÉMICO_DE_TECNOLOGÍA') + 1]
    aux_data  = data.filter(columnas)

    puntajes_de_escala = ['PUNTAJE_ESCALA_CONFLICTOS_TRANSICIÓN',
                'PUNTAJE_ESCALA_MOTIVACIONES_ACADÉMICAS',
                'PUNTAJE_ESCALA_EXPECTATIVAS_ACADÉMICAS',
                'PUNTAJE_ESCALA_DESIGUALDAD_PERCIBIDA',
                'PUNTAJE_ESCALA_PERCEPCIÓN_DE_LA_DOCENCIA',
                'PUNTAJE_ESCALA_DISTRACCIÓN_Y_PROCASTINACIÓN',
                'PUNTAJE_ESCALA_ANSIEDAD_ACADÉMICA',
                'PUNTAJE_ESCALA_SELECCIÓN_DE_IDEAS_PRINCIPALES',
                'PUNTAJE_ESCALA_USO_ACADÉMICO_DE_TECNOLOGÍA']

    # PUNTAJES DE ESCALAS
    # CARRERA
    out_puntajes = carreras_diagnostico 
    i = 0
    
    while i < len(puntajes_de_escala) :
        
        escala = puntajes_de_escala[i]
        nombre_escala = escala.replace('PUNTAJE_ESCALA_','')
        aux = aux_data[aux_data[escala]!='']

        columna = 'MEDIA_' + nombre_escala
        promedio = aux.groupby('CARRERA')[escala].mean()
        out_puntajes = pd.merge(out_puntajes, promedio.rename(columna), how='left', on='CARRERA')

        columna = 'PUNTAJE_MINIMO_' + nombre_escala
        minimo = aux.groupby('CARRERA')[escala].min()
        out_puntajes = pd.merge(out_puntajes, minimo.rename(columna), how='left', on='CARRERA')

        columna = 'PUNTAJE_MAXIMO_' + nombre_escala
        maximo = aux.groupby('CARRERA')[escala].max()
        out_puntajes = pd.merge(out_puntajes, maximo.rename(columna), how='left', on='CARRERA')


        i = i + 1
    # FACULTAD
    i = 0
    aux_facultades = carreras_diagnostico
    while i < len(puntajes_de_escala) :
        
        escala = puntajes_de_escala[i]
        nombre_escala = escala.replace('PUNTAJE_ESCALA_','')
        aux = aux_data[aux_data[escala]!='']

        columna = 'MEDIA_' + nombre_escala + '_FAC'
        promedio = aux.groupby('FACULTAD')[escala].mean()
        aux_facultades = pd.merge(aux_facultades, promedio.rename(columna), how='left', on='FACULTAD')

        columna = 'PUNTAJE_MINIMO_' + nombre_escala + '_FAC'
        minimo = aux.groupby('FACULTAD')[escala].min()
        aux_facultades = pd.merge(aux_facultades, minimo.rename(columna), how='left', on='FACULTAD')

        columna = 'PUNTAJE_MAXIMO_' + nombre_escala + '_FAC'
        maximo = aux.groupby('FACULTAD')[escala].max()
        aux_facultades = pd.merge(aux_facultades, maximo.rename(columna), how='left', on='FACULTAD')


        i = i + 1

    out_puntajes.reset_index(inplace=True)
    out_puntajes = pd.merge(out_puntajes, aux_facultades, how='left', on='FACULTAD', left_index=True)
    out_puntajes.set_index('CARRERA', inplace=True)

    i = 0
    while i < len(puntajes_de_escala) :
        
        escala = puntajes_de_escala[i]
        nombre_escala = escala.replace('PUNTAJE_ESCALA_','')
        aux = aux_data[aux_data[escala]!='']

        columna = 'MEDIA_' + nombre_escala + '_USACH'
        out_puntajes[columna] = aux[escala].mean()

        columna = 'PUNTAJE_MINIMO_' + nombre_escala + '_USACH'
        out_puntajes[columna] = aux[escala].min()

        columna = 'PUNTAJE_MAXIMO_' + nombre_escala + '_USACH'
        out_puntajes[columna] = aux[escala].max()
        i = i + 1
    
    aux_data  = data.filter(columnas)

    niveles_de_escala = ['NIVEL_ESCALA_CONFLICTO_TRANSICIÓN',
                         'NIVEL_ESCALA_MOTIVACIONES_ACADÉMICAS',
                         'NIVEL_ESCALA_EXPECTATIVAS_ACADÉMICAS',
                         'NIVEL_ESCALA_DESIGUALDAD_PERCIBIDA',
                         'NIVEL_ESCALA_PERCEPCIÓN_DE_LA_DOCENCIA',
                         'NIVEL_ESCALA_DISTRACCIÓN_Y_PROCASTINACIÓN',
                         'NIVEL_ESCALA_ANSIEDAD_ACADÉMICA',
                         'NIVEL_ESCALA_SELECCIÓN_DE_IDEAS_PRINCIPALES',
                         'NIVEL_ESCALA_USO_ACADÉMICO_DE_TECNOLOGÍA'
                        ]
    out = carreras_diagnostico
    ###################################################
    # ESCALAS DE AUTOREPORTE ACADÉMICO							
    ###################################################
    # NIVELES DE ESCALA
    i = 0
    while i < len(niveles_de_escala):
        escala_actual = niveles_de_escala[i]
        nombre_escala = escala_actual.replace('NIVEL_ESCALA_','')
        columnas = { 'ALTO' : nombre_escala + '_ALTO',
                     'MEDIO': nombre_escala + '_MEDIO',
                     'BAJO': nombre_escala + '_BAJO',

            }
        aux = aux_data[aux_data[escala_actual]!='']
        aux = aux.groupby('CARRERA')[escala_actual].value_counts(normalize=True)
        aux = pd.DataFrame(aux)
        aux.index = aux.index.set_names(['CARRERA', 'RESPUESTA'])
        aux.reset_index(inplace=True)
        aux = aux.pivot(index='CARRERA', 
                        columns='RESPUESTA', 
                        values=escala_actual)
        aux = aux.rename(columns=columnas)
        for e in columnas.values():
            if e in aux.columns :
                aux[e] = aux[e].fillna(0)
            else :
                aux[e] = 0

        out = pd.merge(out, aux, how='left', on='CARRERA')
        i = i + 1
        
    # NIVELES DE ESCALA FACULTAD
    i = 0
    aux_facultades = carreras_diagnostico
    while i < len(niveles_de_escala):
        escala_actual = niveles_de_escala[i]
        nombre_escala = escala_actual.replace('NIVEL_ESCALA_','')
        columnas = { 'ALTO' : nombre_escala + '_ALTO_FAC',
                     'MEDIO': nombre_escala + '_MEDIO_FAC',
                     'BAJO': nombre_escala + '_BAJO_FAC'
                    }
        aux = aux_data[aux_data[escala_actual]!='']
        aux = aux.groupby('FACULTAD')[escala_actual].value_counts(normalize=True)
        aux = pd.DataFrame(aux)
        aux.index = aux.index.set_names(['FACULTAD', 'RESPUESTA'])
        aux.reset_index(inplace=True)
        aux = aux.pivot(index='FACULTAD', 
                        columns='RESPUESTA', 
                        values=escala_actual)

        aux = aux.rename(columns=columnas)
        for e in columnas.values():
            if e in aux :
                aux[e] = aux[e].fillna(0)
            else :
                aux[e] = 0

        aux_facultades = pd.merge(aux_facultades, aux, how='left', on='FACULTAD')
        i = i + 1


    out.reset_index(inplace=True)  
    out = pd.merge(out, aux_facultades, how='left', on='FACULTAD', left_index=True)
    out.set_index('CARRERA', inplace=True)

    i = 0
    while i < len(niveles_de_escala):
        escala_actual = niveles_de_escala[i]
        nombre_escala = escala_actual.replace('NIVEL_ESCALA_','')
        columnas = { 'ALTO' : nombre_escala + '_ALTO_USACH',
                     'MEDIO': nombre_escala + '_MEDIO_USACH',
                     'BAJO': nombre_escala + '_BAJO_USACH'}
        
        aux = aux_data[aux_data[escala_actual]!='']
        aux_total = aux[escala_actual].count()
        
        for key in columnas :
            aux = aux[aux[escala_actual]==key]
            total = aux[escala_actual].count()
            out[columnas[key]] = total / aux_total
            aux = aux_data[aux_data[escala_actual]!='']
        
        i = i + 1
    #########################################################################
    # PROBLEMAS EN LA TRANSICIÓN ACADÉMICA
    #########################################################################
    
    out = pd.merge(out, out_puntajes, how='left', on='CARRERA')
    
    # TERMINAR CON TODAS LAS COLUMNAS EN MAYÚSCULA
    out.columns = _formatear_columnas(out.columns)
    out = _formatear_data_set(out)
   
    return out


def crear_resumen_socioeducativo(data,resumen):
    #data_frame = procesar_socioeducativo_preguntas_1_20(data, resumen)
    #data_frame.to_excel('resultados_socioeducativo-1.xlsx', sheet_name='RESULTADOS_SE', index=True)
    data_frame = procesar_socioeducativo_preguntas_21_67(data,resumen)
    data_frame.to_excel('resultados_socioeducativo-2.xlsx', sheet_name='RESULTADOS_SE', index=True)
    #data_frame = procesar_socioeducativo_escalas_autorreporte(data, resumen)  
    #data_frame.to_excel('resultados_socioeducativo-3.xlsx', sheet_name='RESULTADOS_SE', index=True)
    return True

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
