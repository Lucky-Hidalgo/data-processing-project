import pandas as pd



def crear_df_carreras(data):
    # Crea dataframe para almacenar resultados, con columnas
    # CARRERA (Index)
    # FACULTAD
    # TOTAL DE ESTUDIANTES
    # Conteo de cada diagnóstico
    diagnosticos = ['RESPONDIÓ CUESTIONARIO SOCIOEDUCATIVO',
                    'RESPONDIÓ MATEMÁTICA "A"',
                    'RESPONDIÓ MATEMÁTICA "B"',
                    'RESPONDIÓ PENSAMIENTO CIENTÍFICO',
                    'RESPONDIÓ ESCRITURA ACADÉMICA']
    new_df = data.filter(['FACULTAD',
                    'CARRERA',
                    'RESPONDIÓ CUESTIONARIO SOCIOEDUCATIVO',
                    'RESPONDIÓ MATEMÁTICA "A"',
                    'RESPONDIÓ MATEMÁTICA "B"',
                    'RESPONDIÓ PENSAMIENTO CIENTÍFICO',
                    'RESPONDIÓ ESCRITURA ACADÉMICA'])

    
    another_df = data.filter(['FACULTAD','CARRERA'])
    
    another_df.drop_duplicates(inplace=True)
    another_df.set_index('CARRERA', drop=True, inplace=True)
    # Se agrega el conteo por carrera
    out = new_df.groupby('CARRERA').agg(
        INSCRITOS = ('CARRERA', 'count'),
        
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

ex = pd.read_excel('salida-big-1-output.xlsx')
yx = crear_df_carreras(ex)
