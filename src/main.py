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
print('ARCHIVO LEÍDO CON ÉXITO')

resultados_generales = ci.crear_df_estadisticas_generales(data, df_carreras)
resultados_matematica_a  = ci.crear_resumen_matematica_a(data, df_carreras)
resultados_matematica_b  = ci.crear_resumen_matematica_b(data, df_carreras)
resultados_pensamiento_cientifico = ci.crear_resumen_pensamiento_cientifico(data, df_carreras)
resultados_escritura_academica = ci.crear_resumen_escritura_academica(data, df_carreras)
resultados_socioeducativo = ci.crear_resumen_socioeducativo(data, df_carreras)
print('RESUMENES CREADOS CON ÉXITO')

resultados_generales.to_excel('estadisticas_generales.xlsx', sheet_name='GENERALES', index=True)
resultados_matematica_a.to_excel('resultados_matematica_a.xlsx', sheet_name='RESULTADOS_MA', index=True)
resultados_matematica_b.to_excel('resultados_matematica_b.xlsx', sheet_name='RESULTADOS_MB', index=True)
resultados_pensamiento_cientifico.to_excel('resultados_pensamiento_cientifico.xlsx', sheet_name='RESULTADOS_PC', index=True)
resultados_escritura_academica.to_excel('resultados_escritura_academica.xlsx', sheet_name='RESULTADOS_EA', index=True)
resultados_socioeducativo.to_excel('resultados_socioeducativo.xlsx', sheet_name='RESULTADOS_SE', index=True)
print('RESUMENES ESCRITOS CORRECTAMENTE')


gr.ejecutar_proceso_graficos_matematica_a(resultados_matematica_a, PATH_SALIDA)
gr.ejecutar_proceso_graficos_matematica_b(resultados_matematica_b, PATH_SALIDA)
gr.ejecutar_proceso_graficos_pensamiento_cientifico(resultados_pensamiento_cientifico, PATH_SALIDA)
gr.ejecutar_proceso_graficos_escritura_academica(resultados_escritura_academica, PATH_SALIDA)

gr.ejecutar_proceso_graficos_socioeducativo(resultados_socioeducativo, PATH_SALIDA)

print('GRÁFICOS ESCRITOS CORRECTAMENTE')
