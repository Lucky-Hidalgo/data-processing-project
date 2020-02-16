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
resultados_matematica_a  = ci.crear_resumen_matematica_a(data, df_carreras)
resultados_matematica_b  = ci.crear_resumen_matematica_b(data, df_carreras)
resultados_pensamiento_cientifico = ci.crear_resumen_pensamiento_cientifico(data, df_carreras)
resultados_escritura_academica = ci.crear_resumen_escritura_academica(data, df_carreras)

resultados_matematica_a.to_excel('resultados_matematica_a.xlsx', sheet_name='RESULTADOS_MA', index=True)
resultados_matematica_b.to_excel('resultados_matematica_b.xlsx', sheet_name='RESULTADOS_MB', index=True)
resultados_pensamiento_cientifico.to_excel('resultados_pensamiento_cientifico.xlsx', sheet_name='RESULTADOS_PC', index=True)
resultados_escritura_academica.to_excel('resultados_escritura_academica.xlsx', sheet_name='RESULTADOS_PC', index=True)