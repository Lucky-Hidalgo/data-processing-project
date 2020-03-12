import graficos as gr
import os

def _crear_carpeta_salida(directorio_salida, nombre_salida):
    # Función que crea la carpeta de salida
    path = directorio_salida + '/' + nombre_salida
    if not os.path.exists(path):
            os.mkdir(path)      
    return path



def _crear_grafico_radar_matematica_a(valores,carrera, ruta):
    '''
    # Radar escala no porcentual
    etiquetas = ["Perro", "Gato", "Hamster"]
    valores = [[10, 20, 30, 40], [52, 23, 37, 90], [87, 97, 51, 21]]
    dimensiones = ["Dim 1", "Dim 2", "Dim 3", "Dim 4"]

    '''
    
    # Radar escala no porcentual
    nombre_salida = carrera.strip().lower().replace(' ','-') + '-grafico-1' 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["NÚMEROS", "ÁLGEBRA", "FUNCIONES", "GEOMETRÍA"]
    g = gr.crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=True)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro según ejes temáticos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True
    
def _obtener_datos_radar_matematica_a(data,carrera):
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


# El segundo gráfico que aparece es de barras agrupadas
def _obtener_datos_barras_matematica_a(data, carrera):
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


def _crear_grafico_barras_matematica_a(valores, carrera, ruta):
    # Radar escala no porcentual
    nombre_salida = carrera.strip().lower().replace(" ","-") + "-grafico-2" 
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["OBJETIVO 1", "OBJETIVO 2", "OBJETIVO 3",
                     "OBJETIVO 4", "OBJETIVO 5", "OBJETIVO 6", "OBJETIVO 7", 
                    "OBJETIVO 8", "OBJETIVO 9"]
    g = gr.crear_grafico_barras_verticales(valores, dimensiones, etiquetas, porcentaje=True)
    g.set_size_inches(30, 5)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro Pensamiento Matemático por objetivos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True


def _crear_graficos_matematica_a(data, ruta):
    lista_carreras = list(data.index.values)
    for carrera in lista_carreras :
        datos_graph1 = _obtener_datos_radar_matematica_a(data,carrera)
        _crear_grafico_radar_matematica_a(datos_graph1, carrera, ruta)
        datos_graph2 = _obtener_datos_barras_matematica_a(data, carrera)
        _crear_grafico_barras_matematica_a(datos_graph2, carrera, ruta)
    return True


def ejecutar_proceso_graficos_matematica_a(data, directorio_salida ):
    path = _crear_carpeta_salida(directorio_salida, 'graficos-ma')
    _crear_graficos_matematica_a(data, path)
    return True
