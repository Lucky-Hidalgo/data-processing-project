'''MAIN DE PRUEBA'''
import preprocesamiento as pp
import calculos as ci 
import graficador as gr


# TODO: CAMBIAR POR SELECCIÓN DE CONFIGURACIÓN

#ARCHIVO_ENTRADA = 'C:/Users/LuHid/Documents/Github/data-processing-project/salida-big-2-output.xlsx'
ARCHIVO_ENTRADA = 'C:/Users/LuHid/Documents/GitHub/data-processing-project/salida-big-2-output.xlsx'
PATH_SALIDA = 'C:/Users/LuHid/Documents/Github/data-processing-project'
PATH_OUT = 'OUT'


data, diccionario_facultades = pp.ejecutar_proceso(ARCHIVO_ENTRADA, PATH_SALIDA, PATH_OUT)



df_carreras = ci.crear_df_carreras(data)
estadisticas_generales = ci.crear_df_estadisticas_generales(data, df_carreras)

resultados_matematica_a  = ci.crear_resumen_matematica_a(data, df_carreras)
resultados_matematica_b  = ci.crear_resumen_matematica_b(data, df_carreras)
resultados_pensamiento_cientifico = ci.crear_resumen_pensamiento_cientifico(data, df_carreras)
resultados_escritura_academica = ci.crear_resumen_escritura_academica(data, df_carreras)
resultados_se = ci.crear_resumen_socioeducativo(data, df_carreras)
print('PASO')


gr.ejecutar_proceso_graficos_matematica_a(resultados_matematica_a, PATH_SALIDA)
gr.ejecutar_proceso_graficos_matematica_b(resultados_matematica_b, PATH_SALIDA)
gr.ejecutar_proceso_graficos_pensamiento_cientifico(resultados_pensamiento_cientifico, PATH_SALIDA)
gr.ejecutar_proceso_graficos_escritura_academica(resultados_escritura_academica, PATH_SALIDA)