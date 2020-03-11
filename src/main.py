'''MAIN DE PRUEBA'''
import preprocesamiento as pp
import calculos as ci 
import graficador as gr


# TODO: CAMBIAR POR SELECCIÓN DE CONFIGURACIÓN

ARCHIVO_ENTRADA = 'C:/Users/LuHid/Documents/Github/data-processing-project/salida-big-2-output.xlsx'
PATH_SALIDA = 'C:/Users/LuHid/Documents/Github/data-processing-project'
PATH_OUT = 'OUT'


data, diccionario_facultades = pp.ejecutar_proceso(ARCHIVO_ENTRADA, PATH_SALIDA, PATH_OUT)



df_carreras = ci.crear_df_carreras(data)
estadisticas_generales = ci.crear_df_estadisticas_generales(data, df_carreras)
'''
resultados_matematica_a  = ci.crear_resumen_matematica_a(data, df_carreras)
resultados_matematica_b  = ci.crear_resumen_matematica_b(data, df_carreras)
resultados_pensamiento_cientifico = ci.crear_resumen_pensamiento_cientifico(data, df_carreras)
resultados_escritura_academica = ci.crear_resumen_escritura_academica(data, df_carreras)'''
resultados_se = ci.crear_resumen_socioeducativo(data, df_carreras)
print('PASO')
resultados_se.to_excel('resultados_socioeducativo.xlsx', sheet_name='RESULTADOS_SE', index=True)
# gr.ejecutar_proceso_graficos_matematica_a(resultados_matematica_a, PATH_SALIDA)