from src.graficos import *


# Torta
etiquetas = ["Perro", "Gato", "Hamster", "Hurón", "Chancho", "Iguana"]
valores = [15, 30, 45, 10, 9, 51]
g = crear_grafico_torta(valores, etiquetas)
agregar_leyenda(g)
agregar_titulo(g, "Torta")
guardar_grafico(g, "torta")
'''
# Barras horizontales simples sin porcentaje
g = crear_grafico_barras_horizontales(valores, etiquetas)
agregar_titulo(g, "Barras horizontales")
agregar_nombres_ejes(g, "Valores", "Bichos")
guardar_grafico(g, "Barras_h")

# Barras horizontales simples con porcentaje
g = crear_grafico_barras_horizontales(valores, etiquetas, porcentaje=True)
agregar_titulo(g, "Barras horizontales")
agregar_nombres_ejes(g, "Valores", "Bichos")
guardar_grafico(g, "Barras_hp")

# Barras verticales simples sin porcentaje
g = crear_grafico_barras_verticales(valores, etiquetas)
agregar_titulo(g, "Barras verticales")
agregar_nombres_ejes(g, "Bichos", "Valores")
guardar_grafico(g, "Barras_v")

# Barras verticales simples con porcentaje
g = crear_grafico_barras_verticales(valores, etiquetas, porcentaje=True)
agregar_titulo(g, "Barras verticales")
agregar_nombres_ejes(g, "Bichos", "Valores")
guardar_grafico(g, "Barras_vp")

# Radar escala no porcentual
etiquetas = ["Perro", "Gato", "Hamster"]
valores = [[10, 20, 30, 40], [52, 23, 37, 90], [87, 97, 51, 21]]
dimensiones = ["Dim 1", "Dim 2", "Dim 3", "Dim 4"]
g = crear_grafico_radar(valores, etiquetas, dimensiones)
agregar_leyenda(g)
agregar_titulo(g, "Radar")
guardar_grafico(g, "radar")

# Radar escala porcentual
g = crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=True)
agregar_leyenda(g)
agregar_titulo(g, "Radar")
guardar_grafico(g, "radar_p")

# Barras horizontales múltiples sin porcentaje
g = crear_grafico_barras_horizontales(valores, dimensiones, etiquetas)
agregar_titulo(g, "Barras múltiples horizontales")
agregar_nombres_ejes(g, "Valores", "Bichos")
agregar_leyenda(g)
guardar_grafico(g, "Barras_multiples_h")

# Barras horizontales múltiples con porcentaje
g = crear_grafico_barras_horizontales(valores, dimensiones, etiquetas, porcentaje=True)
agregar_titulo(g, "Barras múltiples horizontales")
agregar_nombres_ejes(g, "Valores", "Bichos")
agregar_leyenda(g)
guardar_grafico(g, "Barras_multiples_hp")

# Barras verticales múltiples sin porcentaje
g = crear_grafico_barras_verticales(valores, dimensiones, etiquetas)
agregar_titulo(g, "Barras múltiples verticales")
agregar_nombres_ejes(g, "Bichos", "Valores")
agregar_leyenda(g)
guardar_grafico(g, "Barras_multiples_v")

# Barras verticales múltiples con porcentaje
g = crear_grafico_barras_verticales(valores, dimensiones, etiquetas, porcentaje=True)
agregar_titulo(g, "Barras múltiples verticales")
agregar_nombres_ejes(g, "Bichos", "Valores")
agregar_leyenda(g)
guardar_grafico(g, "Barras_multiples_vp")

# Barras apiladas verticales
g = crear_grafico_barras_apiladas_verticales(valores, dimensiones, etiquetas)
agregar_titulo(g, "Barras apiladas verticales")
agregar_nombres_ejes(g, "Dimensiones", "Valores")
agregar_leyenda(g)
guardar_grafico(g, "Barras_apiladas_v")

# Barras apiladas horizontales
g = crear_grafico_barras_apiladas_horizontales(valores, dimensiones, etiquetas)
agregar_titulo(g, "Barras apiladas horizontales")
agregar_nombres_ejes(g, "Valores", "Dimensiones")
agregar_leyenda(g)
guardar_grafico(g, "Barras_apiladas_h")
'''