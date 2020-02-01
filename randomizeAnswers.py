import pandas as pd
import random

import populateSmall

NOMBRE_ARCHIVO_ENTRADA = 'salida.xlsx'

base = pd.read_excel(NOMBRE_ARCHIVO_ENTRADA, index_col=0)

lista_facultades = populateSmall.obtener_facultades(base)

lista_diagnosticos = populateSmall.definir_diagnosticos(lista_facultades)

print(lista_facultades)
print(lista_diagnosticos)