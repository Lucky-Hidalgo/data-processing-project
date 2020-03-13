import graficos as gr
import os

def _crear_carpeta_salida(directorio_salida, nombre_salida):
    # Función que crea la carpeta de salida
    path = directorio_salida + '/' + nombre_salida
    if not os.path.exists(path):
            os.mkdir(path)      
    return path

def _capitalizar_lista(lista):
    return list(map(lambda x:x.capitalize(), lista)) 

####################################################################################
# 
# GRAFICOS MATEMÁTICA A
#
####################################################################################
def _obtener_datos_grafico_1_matematica_a(data,carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_1'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_2'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_3'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_4'],
        ]
    datos_facultad = [
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_1_FAC'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_2_FAC'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_3_FAC'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_4_FAC'],
        ]
    datos_usach = [
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_1_USACH'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_2_USACH'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_3_USACH'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_4_USACH'],
        ]
    # Multiplico x 100
    valores = [datos_carrera, datos_facultad, datos_usach]
    valores = [list(map(lambda x : x * 100, row)) for row in valores]
    return valores


def _crear_grafico_1_matematica_a(valores,carrera, ruta):
    '''
    # Radar escala no porcentual
    etiquetas = ["Perro", "Gato", "Hamster"]
    valores = [[10, 20, 30, 40], [52, 23, 37, 90], [87, 97, 51, 21]]
    dimensiones = ["Dim 1", "Dim 2", "Dim 3", "Dim 4"]

    '''
    
    # Radar escala no porcentual
    nombre_salida = "grafico-1-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["NÚMEROS", "ÁLGEBRA", "FUNCIONES", "GEOMETRÍA"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=True)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro según ejes temáticos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True
    


# El segundo gráfico que aparece es de barras agrupadas
def _obtener_datos_grafico_2_matematica_a(data, carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_1"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_2"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_3"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_4"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_5"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_6"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_7"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_8"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_9"]
        ]
    datos_facultad = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_1_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_2_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_3_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_4_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_5_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_6_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_7_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_8_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_9_FAC"]
        ]
    datos_usach = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_1_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_2_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_3_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_4_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_5_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_6_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_7_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_8_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_9_USACH"]
        ]
    # Multiplico x 100
    valores = [datos_carrera, datos_facultad, datos_usach]
    valores = [list(map(lambda x : x * 100, row)) for row in valores]
    return valores


def _crear_grafico_2_matematica_a(valores, carrera, ruta):
    # Radar escala no porcentual
    nombre_salida = "grafico-2-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["OBJETIVO 1", "OBJETIVO 2", "OBJETIVO 3",
                     "OBJETIVO 4", "OBJETIVO 5", "OBJETIVO 6", "OBJETIVO 7", 
                    "OBJETIVO 8", "OBJETIVO 9"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_barras_verticales(valores, dimensiones, etiquetas, porcentaje=True)
    g.set_size_inches(30, 5)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro Pensamiento Matemático por objetivos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True


def _crear_graficos_matematica_a(data, ruta):
    lista_carreras = list(data.index.values)
    for carrera in lista_carreras :
        datos_graph1 = _obtener_datos_grafico_1_matematica_a(data,carrera)
        _crear_grafico_1_matematica_a(datos_graph1, carrera, ruta)
        datos_graph2 = _obtener_datos_grafico_2_matematica_a(data, carrera)
        _crear_grafico_2_matematica_a(datos_graph2, carrera, ruta)
    return True


def ejecutar_proceso_graficos_matematica_a(data, directorio_salida ):
    path = _crear_carpeta_salida(directorio_salida, 'graficos-ma')
    _crear_graficos_matematica_a(data, path)
    return True

####################################################################################
# 
# GRAFICOS MATEMÁTICA B
#
####################################################################################
def _obtener_datos_grafico_1_matematica_b(data,carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_1'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_2'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_3'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_4'],
        ]
    datos_facultad = [
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_1_FAC'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_2_FAC'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_3_FAC'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_4_FAC'],
        ]
    datos_usach = [
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_1_USACH'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_2_USACH'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_3_USACH'],
            data.loc[carrera, 'PORCENTAJE_PROMEDIO_EJE_4_USACH'],
        ]
    # Multiplico x 100
    valores = [datos_carrera, datos_facultad, datos_usach]
    valores = [list(map(lambda x : x * 100, row)) for row in valores]
    return valores


def _crear_grafico_1_matematica_b(valores,carrera, ruta):
        
    # Radar escala no porcentual
    nombre_salida = "grafico-1-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["RELACIONES Y PATRONES", "RAZONAMIENTO PROBABILÍSTICO Y ESTADÍSTICO", 
                    "RAZONAMIENTO NUMÉRICO", "RAZONAMIENTO GEOMÉTRICO"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=True)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro según ejes temáticos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True
    


# El segundo gráfico que aparece es de barras agrupadas
def _obtener_datos_grafico_2_matematica_b(data, carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_1"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_2"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_3"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_4"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_5"]
        ]
    datos_facultad = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_1_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_2_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_3_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_4_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_5_FAC"]
        ]
    datos_usach = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_1_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_2_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_3_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_4_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_OBJ_5_USACH"]
        ]
    # Multiplico x 100
    valores = [datos_carrera, datos_facultad, datos_usach]
    valores = [list(map(lambda x : x * 100, row)) for row in valores]
    return valores


def _crear_grafico_2_matematica_a(valores, carrera, ruta):
    # Radar escala no porcentual
    nombre_salida =  "grafico-2-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["OBJETIVO 1", "OBJETIVO 2", "OBJETIVO 3",
                     "OBJETIVO 4", "OBJETIVO 5"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_barras_verticales(valores, dimensiones, etiquetas, porcentaje=True)
    g.set_size_inches(30, 5)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro Pensamiento Matemático según objetivos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True


def _crear_graficos_matematica_b(data, ruta):
    lista_carreras = list(data.index.values)
    for carrera in lista_carreras :
        datos_graph1 = _obtener_datos_grafico_1_matematica_b(data,carrera)
        _crear_grafico_1_matematica_a(datos_graph1, carrera, ruta)
        datos_graph2 = _obtener_datos_grafico_2_matematica_b(data, carrera)
        _crear_grafico_2_matematica_a(datos_graph2, carrera, ruta)
    return True


def ejecutar_proceso_graficos_matematica_b(data, directorio_salida ):
    path = _crear_carpeta_salida(directorio_salida, 'graficos-mb')
    _crear_graficos_matematica_b(data, path)
    return True

####################################################################################
# 
# GRAFICOS PENSAMIENTO CIENTÍFICO
#
####################################################################################
def _obtener_datos_grafico_1_pensamiento_cientifico(data,carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, 'CONCRETO'],
            data.loc[carrera, 'TRANSICIONAL'],
            data.loc[carrera, 'FORMAL']

        ]
    datos_facultad = [
            data.loc[carrera, 'CONCRETO_FAC'],
            data.loc[carrera, 'TRANSICIONAL_FAC'],
            data.loc[carrera, 'FORMAL_FAC']

        ]
    datos_usach = [
            data.loc[carrera, 'CONCRETO_USACH'],
            data.loc[carrera, 'TRANSICIONAL_USACH'],
            data.loc[carrera, 'FORMAL_USACH']
        ]
    
    valores = [datos_carrera, datos_facultad, datos_usach]
    valores = [list(map(lambda x : x / 100, row)) for row in valores]
    return valores


def _crear_grafico_1_pensamiento_cientifico(valores,carrera, ruta):
    
    
    # Radar escala no porcentual
    nombre_salida = "grafico-1-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["CONCRETO", "TRANSICIONAL", "FORMAL"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=True)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro según ejes temáticos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True
    


# El segundo gráfico que aparece es de barras agrupadas
def _obtener_datos_grafico_2_pensamiento_cientifico(data, carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_1"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_2"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_3"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_4"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_5"]
        ]
    datos_facultad = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_1_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_2_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_3_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_4_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_5_FAC"]
        ]
    datos_usach = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_1_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_2_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_3_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_4_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_5_USACH"]
        ]
    # Multiplico x 100
    valores = [datos_carrera, datos_facultad, datos_usach]
    valores = [list(map(lambda x : x * 100, row)) for row in valores]
    return valores


def _crear_grafico_2_pensamiento_cientifico(valores, carrera, ruta):
    # Radar escala no porcentual
    nombre_salida =  "grafico-2-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["CONSERVACIÓN DE MAGNITUDES FÍSICAS", "PENSAMIENTO DE PROPORCIONALIDAD",
                     "IDENTIFICACIÓN Y CONTROL DE VARIABLES", "PENSAMIENTO PROBABILÍSTICO",
                     "PENSAMIENTO COMBINATORIO Y CORRELACIONAL"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_barras_verticales(valores, dimensiones, etiquetas, porcentaje=True)
    g.set_size_inches(30, 5)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro Pensamiento Científico según objetivos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True


def _crear_graficos_pensamiento_cientifico(data, ruta):
    lista_carreras = list(data.index.values)
    for carrera in lista_carreras :
        datos_graph1 = _obtener_datos_grafico_1_pensamiento_cientifico(data,carrera)
        _crear_grafico_1_pensamiento_cientifico(datos_graph1, carrera, ruta)
        datos_graph2 = _obtener_datos_grafico_2_pensamiento_cientifico(data, carrera)
        _crear_grafico_2_pensamiento_cientifico(datos_graph2, carrera, ruta)
    return True


def ejecutar_proceso_graficos_pensamiento_cientifico(data, directorio_salida ):
    path = _crear_carpeta_salida(directorio_salida, 'graficos-pc')
    _crear_graficos_pensamiento_cientifico(data, path)
    return True


####################################################################################
# 
# GRAFICOS ESCRITURA ACADÉMICA
#
####################################################################################

# El segundo gráfico que aparece es de barras agrupadas
def _obtener_datos_grafico_1_escritura_academica(data, carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_1"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_2"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_3"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_4"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_5"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_6"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_7"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_8"]
        ]
    datos_facultad = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_1_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_2_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_3_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_4_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_5_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_6_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_7_FAC"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_8_FAC"],
        ]
    datos_usach = [
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_1_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_2_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_3_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_4_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_5_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_6_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_7_USACH"],
            data.loc[carrera, "PORCENTAJE_PROMEDIO_DIM_8_USACH"],
        ]
    # Multiplico x 100
    valores = [datos_carrera, datos_facultad, datos_usach]
    valores = [list(map(lambda x : x * 100, row)) for row in valores]
    return valores

def _crear_grafico_1_escritura_academica(valores,carrera, ruta):
    
    
    # Radar escala no porcentual
    nombre_salida = "grafico-1-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["ESTRUCTURA", "COHERENCIA LOCAL",
                     "ORTOGRAFÍA ACENTUAL Y LITERAL", "ORTOGRAFÍA PUNTUAL",
                     "LÉXICO", "RECURSOS DE NIVEL GRAMATICAL", "ESTRUCTURA DE PÁRRAFOS",
                     "TRANSFORMACIÓN DEL CONOCIMIENTO"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=True)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro según ejes temáticos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True
    

def _crear_grafico_2_escritura_academica(valores, carrera, ruta):
    # Radar escala no porcentual
    nombre_salida =  "grafico-2-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["ESTRUCTURA", "COHERENCIA LOCAL",
                     "ORTOGRAFÍA ACENTUAL Y LITERAL", "ORTOGRAFÍA PUNTUAL",
                     "LÉXICO", "RECURSOS DE NIVEL GRAMATICAL", "ESTRUCTURA DE PÁRRAFOS",
                     "TRANSFORMACIÓN DEL CONOCIMIENTO"]
    etiquetas = _capitalizar_lista(etiquetas)
    dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_barras_verticales(valores, dimensiones, etiquetas, porcentaje=True)
    g.set_size_inches(30, 5)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro Escritura Académica según objetivos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True


def _crear_graficos_escritura_academica(data, ruta):
    lista_carreras = list(data.index.values)
    for carrera in lista_carreras :
        datos_graph1 = _obtener_datos_grafico_1_escritura_academica(data,carrera)
        _crear_grafico_1_escritura_academica(datos_graph1, carrera, ruta)
        _crear_grafico_2_escritura_academica(datos_graph1, carrera, ruta)
        
        
    return True


def ejecutar_proceso_graficos_escritura_academica(data, directorio_salida ):
    path = _crear_carpeta_salida(directorio_salida, 'graficos-ea')
    _crear_graficos_escritura_academica(data, path)
    return True

####################################################################################
# 
# GRAFICOS SOCIOEDUCATIVO
#
####################################################################################

# El segundo gráfico que aparece es de barras agrupadas
def _obtener_datos_grafico_1_socioeducativo(data, carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    datos_carrera = [
            data.loc[carrera, "FEMENINO"],
            data.loc[carrera, "MASCULINO"],
            data.loc[carrera, "OTRO"]
        ]
    
    # Multiplico x 100
    valores = datos_carrera
    valores = [x * 100 for x in valores]
    return valores

def _crear_grafico_1_socioeducativo(valores,carrera, ruta):
    # Torta

    nombre_salida = "grafico-1-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["FEMENINO", "MASCULINO", "OTRO"]
    etiquetas = _capitalizar_lista(etiquetas)
    #dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_torta(valores, etiquetas)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación según género")
    gr.guardar_grafico(g, nombre_salida, ruta)         
    return True

def _obtener_datos_grafico_2_socioeducativo(data, carrera):
    # Función que obtiene la matriz de valores que el gráfico necesita
    # y  que los multiplica por 100 para que representen porcentaje
    # Obtengo los datos
    columnas = ['VIVIRA_CON_SUS_PADRES', 'VIVIRA_CON_PAREJA_O_AMIGOS', 
                'VIVIRA_SIN_PERSONAS_CERCANAS', 'VIVIRA_CON_FAMILIARES', 
                'VIVIRA_SOLO']
    datos_carrera = []
    for e in columnas : 
        datos_carrera.append(data.loc[carrera, e])
    
    # Multiplico x 100
    valores = datos_carrera
    valores = [x * 100 for x in valores]
    return valores

def _crear_grafico_2_socioeducativo(valores,carrera, ruta):
    # Torta

    nombre_salida = "grafico-2-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CON MI MADRE Y/O MI PADRE", "CON MI PAREJA O AMIGOS/AS", 
                "CON OTRAS PERSONAS NO CERCANAS (POR EJ. PENSIÓN)",
                "CON OTRO FAMILIAR CERCANO (POR EJ. ABUELOS/AS, HERMANOS/AS,TÍOS/AS)", "SOLO/A"]
    etiquetas = _capitalizar_lista(etiquetas)
    #dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_torta(valores, etiquetas)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "¿Con quién vivirás durante el año académico?")
    gr.guardar_grafico(g, nombre_salida, ruta)         
    return True
'''
def _crear_grafico_2_socioeducativo(valores, carrera, ruta):
    # Radar escala no porcentual
    nombre_salida =  "grafico-2-" + carrera.strip().lower().replace(" ","-") 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["ESTRUCTURA", "COHERENCIA LOCAL",
                     "ORTOGRAFÍA ACENTUAL Y LITERAL", "ORTOGRAFÍA PUNTUAL",
                     "LÉXICO", "RECURSOS DE NIVEL GRAMATICAL", "ESTRUCTURA DE PÁRRAFOS",
                     "TRANSFORMACIÓN DEL CONOCIMIENTO"]
    #etiquetas = _capitalizar_lista(etiquetas)
    #dimensiones = _capitalizar_lista(dimensiones)
    g = gr.crear_grafico_barras_verticales(valores, dimensiones, etiquetas, porcentaje=True)
    g.set_size_inches(30, 5)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro Escritura Académica según objetivos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True

'''
def _crear_graficos_socioeducativo(data, ruta):
    lista_carreras = list(data.index.values)
    for carrera in lista_carreras :
        datos_graph1 = _obtener_datos_grafico_1_socioeducativo(data,carrera)
        _crear_grafico_1_socioeducativo(datos_graph1, carrera, ruta)
        datos_graph2 = _obtener_datos_grafico_2_socioeducativo(data,carrera)
        _crear_grafico_2_socioeducativo(datos_graph2, carrera, ruta)
        
        
    return True


def ejecutar_proceso_graficos_socioeducativo(data, directorio_salida ):
    path = _crear_carpeta_salida(directorio_salida, 'graficos-se')
    data.columns = [c.strip().upper().replace(' ', '_') for c in data.columns]
    _crear_graficos_socioeducativo(data, path)
    return True