"""Módulo para preprocesar información"""
import pandas as pd
import os





# Funciones de uso interno del módulo

def _obtener_carreras(base):
    # Función que obtiene todas las carreras de la base de datos
    carreras = list(set(base.CARRERA))
    carreras = [c.strip().upper() for c in carreras]
    return carreras 

def _obtener_facultades(base):
    # Función que obtiene todas las facultades de la base de datos
    facultades = list(set(base.FACULTAD))
    facultades = [f.strip().upper() for f in facultades]
    return facultades


def _crear_diccionario_facultades(data, facultades, carreras):
    # Función que crea un diccionario generando las dependencias entre carrera y facultad
    dict_facultades = dict()
    # Se agrega cada Facultad como una entrada al diccionario
    for e in facultades :
        dict_facultades[e.upper()] = []
    # Se agrega cada carrera a su facultad respectiva
    while len(carreras) > 0 :
        carrera = carreras[0]
        aux = data.loc[data['CARRERA'] == carrera]
        facultad = aux.iloc[0].FACULTAD
        dict_facultades[facultad.upper()].append(carrera.upper())
        carreras.pop(0)
    return dict_facultades



def _crear_carpeta_salida(directorio_salida, nombre_salida):
    # Función que crea la carpeta de salida
    path = directorio_salida + '/' + nombre_salida
    if not os.path.exists(path):
            os.mkdir(path)      
    else:    
            print("Carpeta:" , path , "ya existe")
    return path


def _crear_carpetas_facultades(facultades, directorio_salida):
    # Función que crea la carpetas por facultad
    i = 0 
    carpetas = 0
    while i < len(facultades):
        path = directorio_salida + '/' + facultades[i]
        
        if not os.path.exists(path):
            os.mkdir(path)
            carpetas += 1
        else:    
            print("Carpeta:" , path , "ya existe")
        i += 1
    
    
    return carpetas


def _crear_carpetas_carreras(diccionario_facultades, directorio_salida):
    # Función que crea las carpetas por carrera
    carpetas = 0
    for facultad in diccionario_facultades :
        carreras_facultad = diccionario_facultades[facultad]
        for carrera in carreras_facultad :
            path = directorio_salida + '/' + facultad + '/' + carrera
            if not os.path.exists(path):
                os.mkdir(path)
                carpetas += 1
            else:    
                print("Carpeta:" , path , "ya existe")
            
    return carpetas


def _limpiar_data_frame(base):
    # Función que realiza limpieza de algunos valores del dataframe
    # Eliminar los espacios en los nombres de las columnas 
    # Cambia todos los nombres de las columnas directamente a mayúsculas
    # Elimina espacios al inicio y al final
    # para acceder directamente a los nombres
    base.columns = [c.strip().upper().replace(' ', '_') 
                            for c in base.columns]
    base.columns = [c.strip().upper().replace('__', '_') 
                            for c in base.columns]
    return base



def _limpiar_columnas_string(base, nombre_columna):
    # Función para procesar columnas que sean de tipo string
    # Elimina caracteres especiales al inicio y al final
    # Cambia todo a mayúsculas
    # Reemplaza caracteres especiales
    base[nombre_columna] = base[nombre_columna].apply(lambda x: x.strip())
    base[nombre_columna] = base[nombre_columna].apply(lambda x: x.upper())
    base[nombre_columna] = base[nombre_columna].apply(lambda x: x.replace('/', ' - '))
    return base


def _escribir_resultados_parciales(data, facultad, carrera, path_salida):
    path = path_salida + '/' + facultad + '/' + carrera + '/' 
    nombre_archivo = 'detalle-' + carrera.lower() + '.xlsx'  
    nuevo_data_frame = data.loc[data['CARRERA'] == carrera]
    nuevo_data_frame.to_excel(path + nombre_archivo, 
                                sheet_name='ESTUDIANTES', 
                                index=True)
    return True

def escribir_resultados_filtrados(data, diccionario_facultades, path):
    archivos = 0 
    for facultad in diccionario_facultades :
        carreras_facultad = diccionario_facultades[facultad]
        for carrera in carreras_facultad : 
            archivos += _escribir_resultados_parciales(data, facultad, carrera, path)
    return archivos


def leer_data_frame(ruta):
    # Función que lee el dataframe
    data = pd.read_excel(ruta, index_col=0)
    data = _limpiar_data_frame(data)
    data = _limpiar_columnas_string(data, 'FACULTAD')
    data = _limpiar_columnas_string(data, 'CARRERA')
    return data



def ejecutar_proceso(archivo_entrada, path_salida, path_out):
    df = leer_data_frame(archivo_entrada)
    lista_carreras = _obtener_carreras(df)
    lista_facultades = _obtener_facultades(df)
    diccionario_facultades = _crear_diccionario_facultades(df, lista_facultades, lista_carreras)
    #path = _crear_carpeta_salida(path_salida,path_out)
    #_crear_carpetas_facultades(lista_facultades, path)
    #_crear_carpetas_carreras(diccionario_facultades, path)
    #escribir_resultados_filtrados(df, diccionario_facultades, path)
    return df, diccionario_facultades
