'''MAIN DE PRUEBA'''
import preprocesamiento as pp
import calculos as ci 
import graficos as gr 


# TODO: CAMBIAR POR SELECCIÓN DE CONFIGURACIÓN

ARCHIVO_ENTRADA = 'C:/Users/LuHid/Documents/Github/data-processing-project/salida-big-1-output.xlsx'
PATH_SALIDA = 'C:/Users/LuHid/Documents/Github/data-processing-project'
PATH_OUT = 'OUT1'


data, diccionario_facultades = pp.ejecutar_proceso(ARCHIVO_ENTRADA, PATH_SALIDA, PATH_OUT)

df_carreras = ci.crear_df_carreras(data)
resultados_matematica_a  = ci.resumen_matematica_a(data, df_carreras)


a.to_excel('resultados_matematica_a.xlsx', sheet_name='RESULTADOS_MATEMATICA_A', index=True)