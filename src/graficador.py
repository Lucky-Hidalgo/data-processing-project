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
    nombre_salida = 'grafico-1-' + carrera.strip().lower().replace(' ','-')
    etiquetas = ["CARRERA", "FACULTAD", "USACH"]
    dimensiones = ["NÚMEROS", "ÁLGEBRA", "FUNCIONES", "GEOMETRÍA"]
    g = gr.crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=True)
    gr.agregar_leyenda(g)
    gr.agregar_titulo(g, "Comparación % de logro según ejes temáticos")
    gr.guardar_grafico(g, nombre_salida, ruta)
    return True
    
def _obtener_datos_radar_matematica_a(data,carrera):
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
    return [datos_carrera, datos_facultad, datos_usach]


def _crear_graficos_matematica_a(data, ruta):
    
    lista_carreras = list(data.index.values)
    for carrera in lista_carreras :
        datos_graph1 = _obtener_datos_radar_matematica_a(data,carrera)
        _crear_grafico_radar_matematica_a(datos_graph1, carrera, ruta)
    return True



def ejecutar_proceso_graficos_matematica_a(data, directorio_salida ):
    path = _crear_carpeta_salida(directorio_salida, 'graficos-ma')
    _crear_graficos_matematica_a(data, path)
    return True
