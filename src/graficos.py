"""Módulo para generar gráficos"""
from math import pi
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np


# TODO: REEMPLAZAR POR VALORES DE ARCHIVO DE CONFIGURACIÓN
COLORES = ["purple", "red", "blue", "green", "orange", "yellow"]


# Constantes
FORMATO_IMAGEN = ".png"
TAMANO_IMAGEN = (10, 10)


# Funciones de uso interno del módulo

def _cerrar_figura(figura):
    # Libera la memoria de la figura para evitar problemas de rendimiento en loops masivos

    figura.clf()
    del figura
    return True


def _generar_angulos(cantidad_dimensiones):
    # Genera ángulos para cada dimensión en gráficos de radar
    angulos = []
    for i in range(cantidad_dimensiones):
        angulos.append(i/float(cantidad_dimensiones)*2*pi)
    angulos += angulos[:1]
    return angulos


def _etiquetar_barras(eje, barras, formato_texto, **kwargs):
    # Agrega una etiqueta a cada barra de un gráfico
    posiciones_verticales = [barra.get_y() for barra in barras]
    constante_y = all(y == posiciones_verticales[0] \
                      for y in posiciones_verticales)

    if constante_y: # Gráfico de barras verticales
        _etiquetar_barras_verticales(eje, barras, formato_texto, **kwargs)
    else:
        _etiquetar_barras_horizontales(eje, barras, formato_texto, **kwargs)


def _etiquetar_barras_verticales(eje, barras, formato_texto, **kwargs):
    # Agrega una etiqueta a cada barra de un gráfico vertical
    y_maximo = eje.get_ylim()[1]
    distancia_externa = y_maximo * 0.01

    for barra in barras:
        texto = formato_texto.format(float(barra.get_height()))
        texto_x = barra.get_x() + barra.get_width() / 2
        texto_y = barra.get_height() + distancia_externa
        eje.text(texto_x, texto_y, texto, ha='center', va='bottom', **kwargs)


def _etiquetar_barras_horizontales(eje, barras, formato_texto, **kwargs):
    # Agrega una etiqueta a cada barra de un gráfico horizontal
    x_maximo = eje.get_xlim()[1]
    distancia = x_maximo * 0.0025

    for barra in barras:
        texto = formato_texto.format(float(barra.get_width()))
        texto_x = barra.get_width() + distancia
        texto_y = barra.get_y() + barra.get_height() / 2
        eje.text(texto_x, texto_y, texto, va='center', **kwargs)


# Funciones de generación de gráficos
def guardar_grafico(figura, nombre, ruta=None):
    """
    Guarda una figura de matplotlib en un archivo.
    Entrada:
    - Figura a gruardar
    - Nombre del archivo (sin extensión)
    - Ruta donde se debe guardar el archivo (por defecto None)
    Salida: ninguna
    """
    if ruta is None:
        figura.savefig(nombre + FORMATO_IMAGEN, bbox_inches='tight')
        
    else:
        figura.savefig(ruta + "//" + nombre + FORMATO_IMAGEN,
                       bbox_inches='tight')
    plt.close(figura)
        


def agregar_leyenda(figura):
    """
    Agrega la leyenda a un gráfico. Este debe estar contenido en una
    figura con un único subgráfico.
    Entrada:
    - Figura que contiene al gráfico
    - Etiquetas de la leyenda
    Salida: ninguna
    """
    eje = figura.get_axes()[0]
    caja = eje.get_position()
    eje.set_position([caja.x0, caja.y0, caja.width*0.6, caja.height])
    eje.legend(title="Leyenda:", loc='upper center',
               bbox_to_anchor=(0.5, -0.1), ncol=2)


def agregar_titulo(figura, titulo):
    """
    Agrega el título a un gráfico. Este debe estar contenido en una
    figura con un único subgráfico.
    Entrada:
    - Figura que contiene al gráfico
    - Título del gráfico
    Salida: ninguna
    """
    eje = figura.get_axes()[0]
    eje.set_title(titulo)


def agregar_nombres_ejes(figura, eje_x, eje_y):
    """
    Agrega el título a un gráfico. Este debe estar contenido en una
    figura con un único subgráfico.
    Entrada:
    - Figura que contiene al gráfico
    - Nombre del eje X
    - Nombre del eje Y
    Salida: ninguna
    """
    eje = figura.get_axes()[0]
    eje.set_xlabel(eje_x)
    eje.set_ylabel(eje_y)


def crear_grafico_torta(valores, etiquetas):
    """
    Crea una figura que contenga un gráfico de torta.
    Entrada:
    - Lista de valores
    - Lista de etiquetas (en el mismo orden que los valores)
    Salida:
    - Figura que contiene el gráfico
    """
    figura = plt.figure(figsize=TAMANO_IMAGEN)
    eje = figura.add_subplot(1, 1, 1)
    eje.pie(valores, labels=etiquetas, shadow=True, colors=COLORES,
            autopct='%1.1f%%')
    return figura


def crear_grafico_radar(valores, etiquetas, dimensiones, porcentaje=False):
    """
    Crea una figura que contenga un gráfico de radar (araña).
    Entrada:
    - Matriz de valores:
      - Filas: instancias
      - Columnas: dimensiones
    - Lista de etiquetas (en el mismo orden que los valores)
    - Lista con los nombres de las dimensiones
    - Bandera para indicar si la escala es porcentual (por defecto no)
    Salida:
    - Figura que contiene el gráfico
    """
    cantidad_dimensiones = len(dimensiones)
    angulos = _generar_angulos(cantidad_dimensiones)
    figura = plt.figure(figsize=TAMANO_IMAGEN)
    eje = figura.add_subplot(1, 1, 1, polar=True)
    plt.xticks(angulos[:-1], dimensiones)
    if porcentaje:
        eje.yaxis.set_major_formatter(mtick.PercentFormatter())

    instancias = len(valores)
    for i in range(instancias):
        valores_circular = valores[i] + valores[i][:1]
        eje.plot(angulos, valores_circular, color=COLORES[i],
                 label=etiquetas[i])

    return figura


def crear_grafico_barras_verticales(valores, dimensiones, etiquetas=None,
                                    porcentaje=False):
    """
    Crea una figura que contenga un gráfico de barras verticales
    simples o agrupadas.
    Entrada:
    - Lista o matriz de valores
    - Lista de dimensiones
    - Lista de etiquetas (barras múltiples)
    - Indicador de si los valores son porcentuales (por defecto no)
    Salida:
    - Figura que contiene el gráfico
    """
    if isinstance(valores[0], (int, float)):
        valores = [valores]
    cantidad_instancias = len(valores)
    figura = plt.figure()
    eje = figura.add_subplot(1, 1, 1)
    gap = 0.8 / cantidad_instancias
    for i, instancia in enumerate(valores):
        barras = np.arange(len(instancia))
        if etiquetas is None:
            grafico = eje.bar(barras + i*gap, instancia, width=gap,
                              color=COLORES[i])
        else:
            grafico = eje.bar(barras + i*gap, instancia, width=gap,
                              color=COLORES[i], label=etiquetas[i])
        if porcentaje:
            _etiquetar_barras(eje, grafico, "{0:.1f}%")
        else:
            _etiquetar_barras(eje, grafico, "{0:.1f}")
    indices = np.arange(len(valores[0]))
    plt.xticks(indices, dimensiones)
    plt.autoscale()
    return figura


def crear_grafico_barras_horizontales(valores, dimensiones, etiquetas=None,
                                      porcentaje=False):
    """
    Crea una figura que contenga un gráfico de barras horizontales
    simples o agrupadas.
    Entrada:
    - Lista o matriz de valores
    - Lista de dimensiones
    - Lista de etiquetas (barras múltiples)
    - Indicador de si los valores son porcentuales (por defecto no)
    Salida:
    - Figura que contiene el gráfico
    """
    if isinstance(valores[0], (int, float)):
        valores = [valores]
    cantidad_instancias = len(valores)
    figura = plt.figure(figsize=TAMANO_IMAGEN)
    eje = figura.add_subplot(1, 1, 1)
    gap = 0.8 / cantidad_instancias
    for i, instancia in enumerate(valores):
        barras = np.arange(len(instancia))
        if etiquetas is None:
            grafico = eje.barh(barras + i*gap, instancia, height=gap,
                               color=COLORES[i])
        else:
            grafico = eje.barh(barras + i*gap, instancia, height=gap,
                               color=COLORES[i], label=etiquetas[i])
        if porcentaje:
            _etiquetar_barras(eje, grafico, "{0:.1f}%")
        else:
            _etiquetar_barras(eje, grafico, "{0:.1f}")
    indices = np.arange(len(valores[0]))
    plt.yticks(indices, dimensiones)
    return figura


def crear_grafico_barras_apiladas_verticales(valores, dimensiones,
                                             etiquetas):
    """
    Crea una figura que contenga un gráfico barras apiladas verticales.
    Entrada:
    - Lista o matriz de valores
    - Lista de dimensiones
    - Lista de etiquetas
    Salida:
    - Figura que contiene el gráfico
    """
    figura = plt.figure(figsize=TAMANO_IMAGEN)
    eje = figura.add_subplot(1, 1, 1)
    valores = np.array(valores)
    forma = list(valores.shape)
    cantidad_dimensiones = np.arange(forma[1])
    for i in range(forma[0]):
        eje.bar(cantidad_dimensiones, valores[i],
                bottom=np.sum(valores[:i], axis=0),
                color=COLORES[i], label=etiquetas[i])
    plt.xticks(cantidad_dimensiones, dimensiones)
    return figura


def crear_grafico_barras_apiladas_horizontales(valores, dimensiones,
                                               etiquetas):
    """
    Crea una figura que contenga un gráfico barras apiladas
    horizontales.
    Entrada:
    - Lista o matriz de valores
    - Lista de dimensiones
    - Lista de etiquetas
    Salida:
    - Figura que contiene el gráfico
    """
    figura = plt.figure(figsize=TAMANO_IMAGEN)
    eje = figura.add_subplot(1, 1, 1)
    valores = np.array(valores)
    forma = list(valores.shape)
    cantidad_dimensiones = np.arange(forma[1])
    for i in np.arange(forma[0]):
        eje.barh(cantidad_dimensiones, valores[i],
                 left=np.sum(valores[:i], axis=0),
                 color=COLORES[i], label=etiquetas[i])
    plt.yticks(cantidad_dimensiones, dimensiones)
    return figura