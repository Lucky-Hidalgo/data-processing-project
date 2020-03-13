import pandas as pd
import random
import numpy as np


NOMBRE_ARCHIVO_ENTRADA = 'salida-big-1.xlsx'
NOMBRE_ARCHIVO_SALIDA = 'salida-big-1-output.xlsx'

columnas_socioeducativo = [
        "RESPONDIÓ CUESTIONARIO SOCIOEDUCATIVO",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 1",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 2",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 3",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 4",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 5",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 6",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 7",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 8",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 9",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 10",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 11",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 12",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 13",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 14",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 15",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 16",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 17",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 18",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 19",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 20",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 21",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 22",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 23",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 24",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 25",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 26",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 27",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 28",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 29",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 30",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 31",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 32",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 33",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 34",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 35",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 36",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 37",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 38",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 39",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 40",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 41",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 42",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 43",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 44",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 45",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 46",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 47",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 48",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 49",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 50",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 51",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 52",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 53",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 54",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 55",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 56",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 57",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 58",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 59",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 60",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 61",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 62",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 63",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 64",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 65",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 66",
        "CUESTIONARIO SOCIOEDUCATIVO Pregunta 67",
        "PUNTAJE ESCALA CONFLICTOS TRANSICIÓN",
        "PUNTAJE ESCALA MOTIVACIONES ACADÉMICAS",
        "PUNTAJE ESCALA EXPECTATIVAS ACADÉMICAS",
        "PUNTAJE ESCALA DESIGUALDAD PERCIBIDA",
        "PUNTAJE ESCALA PERCEPCIÓN DE LA DOCENCIA",
        "PUNTAJE ESCALA DISTRACCIÓN Y PROCASTINACIÓN",
        "PUNTAJE ESCALA ANSIEDAD ACADÉMICA",
        "PUNTAJE ESCALA SELECCIÓN DE IDEAS PRINCIPALES",
        "PUNTAJE ESCALA USO ACADÉMICO DE TECNOLOGÍA",
        "MEDIA ESCALA CONFLICTO TRANSICIÓN",
        "MEDIA ESCALA MOTIVACIONES ACADÉMICAS",
        "MEDIA  ESCALA EXPECTATIVAS ACADÉMICAS",
        "MEDIA ESCALA DESIGUALDAD PERCIBIDA",
        "MEDIA ESCALA PERCEPCIÓN DE LA DOCENCIA",
        "MEDIA ESCALA DISTRACCIÓN Y PROCASTINACIÓN",
        "MEDIA ESCALA ANSIEDAD ACADÉMICA",
        "MEDIA ESCALA SELECCIÓN DE IDEAS PRINCIPALES",
        "MEDIA ESCALA USO ACADÉMICO DE TECNOLOGÍA",
        "PUNTAJE ESTANDARIZADO ESCALA CONFLICTO TRANSICIÓN",
        "PUNTAJE ESTANDARIZADO ESCALA MOTIVACIONES ACADÉMICAS",
        "PUNTAJE ESTANDARIZADO ESCALA EXPECTATIVAS ACADÉMICAS",
        "PUNTAJE ESTANDARIZADO ESCALA DESIGUALDAD PERCIBIDA",
        "PUNTAJE ESTANDARIZADO ESCALA PERCEPCIÓN DE LA DOCENCIA",
        "PUNTAJE ESTANDARIZADO ESCALA DISTRACCIÓN Y PROCASTINACIÓN",
        "PUNTAJE ESTANDARIZADO ESCALA ANSIEDAD ACADÉMICA",
        "PUNTAJE ESTANDARIZADO ESCALA SELECCIÓN DE IDEAS PRINCIPALES",
        "PUNTAJE ESTANDARIZADO ESCALA USO ACADÉMICO DE TECNOLOGÍA",
        "NIVEL ESCALA CONFLICTO TRANSICIÓN",
        "NIVEL ESCALA MOTIVACIONES ACADÉMICAS",
        "NIVEL ESCALA EXPECTATIVAS ACADÉMICAS",
        "NIVEL ESCALA DESIGUALDAD PERCIBIDA",
        "NIVEL ESCALA PERCEPCIÓN DE LA DOCENCIA",
        "NIVEL ESCALA DISTRACCIÓN Y PROCASTINACIÓN",
        "NIVEL ESCALA ANSIEDAD ACADÉMICA",
        "NIVEL ESCALA SELECCIÓN DE IDEAS PRINCIPALES",
        "NIVEL ESCALA USO ACADÉMICO DE TECNOLOGÍA"]

columnas_matematica_a = [
                        'RESPONDIÓ MATEMÁTICA "A"',
                        'MATEMÁTICA "A" Pregunta 1',
                        'MATEMÁTICA "A" Pregunta 2',
                        'MATEMÁTICA "A" Pregunta 3',
                        'MATEMÁTICA "A" Pregunta 4',
                        'MATEMÁTICA "A" Pregunta 5',
                        'MATEMÁTICA "A" Pregunta 6',
                        'MATEMÁTICA "A" Pregunta 7',
                        'MATEMÁTICA "A" Pregunta 8',
                        'MATEMÁTICA "A" Pregunta 9',
                        'MATEMÁTICA "A" Pregunta 10',
                        'MATEMÁTICA "A" Pregunta 11',
                        'MATEMÁTICA "A" Pregunta 12',
                        'MATEMÁTICA "A" Pregunta 13',
                        'MATEMÁTICA "A" Pregunta 14',
                        'MATEMÁTICA "A" Pregunta 15',
                        'MATEMÁTICA "A" Pregunta 16',
                        'MATEMÁTICA "A" Pregunta 17',
                        'MATEMÁTICA "A" Pregunta 18',
                        'MATEMÁTICA "A" Pregunta 19',
                        'MATEMÁTICA "A" Pregunta 20',
                        'MATEMÁTICA "A" Pregunta 21',
                        'MATEMÁTICA "A" Pregunta 22',
                        'MATEMÁTICA "A" Pregunta 23',
                        'MATEMÁTICA "A" Pregunta 24',
                        'MATEMÁTICA "A" Pregunta 25',
                        'MATEMÁTICA "A" Pregunta 26',
                        'MATEMÁTICA "A" Pregunta 27',
                        'MATEMÁTICA "A" Pregunta 28',
                        'MATEMÁTICA "A" Pregunta 29',
                        'PUNTAJE TOTAL (MA)',
                        'PORCENTAJE DE LOGRO  (MA)',
                        'OBJETIVO 1  (MA)',
                        'OBJETIVO 2  (MA)',
                        'OBJETIVO 3  (MA)',
                        'OBJETIVO 4  (MA)',
                        'OBJETIVO 5  (MA)',
                        'OBJETIVO 6  (MA)',
                        'OBJETIVO 7  (MA)',
                        'OBJETIVO 8  (MA)',
                        'OBJETIVO 9  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 1  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 2  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 3  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 4  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 5  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 6  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 7  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 8  (MA)',
                        'PORCENTAJE DE LOGRO OBJETIVO 9  (MA)',
                        'EJE TEMÁTICO 1  (MA)',
                        'EJE TEMÁTICO 2  (MA)',
                        'EJE TEMÁTICO 3  (MA)',
                        'EJE TEMÁTICO 4  (MA)',
                        'PORCENTAJE DE LOGRO EJE 1  (MA)',
                        'PORCENTAJE DE LOGRO EJE 2  (MA)',
                        'PORCENTAJE DE LOGRO EJE 3  (MA)',
                        'PORCENTAJE DE LOGRO EJE 4  (MA)'
                        ]

columnas_matematica_b = [
                        'RESPONDIÓ MATEMÁTICA "B"',
                        'MATEMÁTICA "B" Pregunta 1',
                        'MATEMÁTICA "B" Pregunta 2',
                        'MATEMÁTICA "B" Pregunta 3',
                        'MATEMÁTICA "B" Pregunta 4',
                        'MATEMÁTICA "B" Pregunta 5',
                        'MATEMÁTICA "B" Pregunta 6',
                        'MATEMÁTICA "B" Pregunta 7',
                        'MATEMÁTICA "B" Pregunta 8',
                        'MATEMÁTICA "B" Pregunta 9',
                        'MATEMÁTICA "B" Pregunta 10',
                        'MATEMÁTICA "B" Pregunta 11',
                        'MATEMÁTICA "B" Pregunta 12',
                        'MATEMÁTICA "B" Pregunta 13',
                        'MATEMÁTICA "B" Pregunta 14',
                        'MATEMÁTICA "B" Pregunta 15',
                        'MATEMÁTICA "B" Pregunta 16',
                        'MATEMÁTICA "B" Pregunta 17',
                        'MATEMÁTICA "B" Pregunta 18',
                        'MATEMÁTICA "B" Pregunta 19',
                        'PUNTAJE TOTAL  (MB)',
                        'PORCENTAJE DE LOGRO (MB)',
                        'OBJETIVO 1 (MB)',
                        'OBJETIVO 2 (MB)',
                        'OBJETIVO 3 (MB)',
                        'OBJETIVO 4 (MB)',
                        'OBJETIVO 5 (MB)',
                        'PORCENTAJE DE LOGRO OBJETIVO 1  (MB)',
                        'PORCENTAJE DE LOGRO OBJETIVO 2  (MB)',
                        'PORCENTAJE DE LOGRO OBJETIVO 3  (MB)',
                        'PORCENTAJE DE LOGRO OBJETIVO 4  (MB)',
                        'PORCENTAJE DE LOGRO OBJETIVO 5  (MB)',
                        'EJE TEMÁTICO 1  (MB)',
                        'EJE TEMÁTICO 2  (MB)',
                        'EJE TEMÁTICO 3  (MB)',
                        'EJE TEMÁTICO 4  (MB)',
                        'PORCENTAJE DE LOGRO EJE 1  (MB)',
                        'PORCENTAJE DE LOGRO EJE 2  (MB)',
                        'PORCENTAJE DE LOGRO EJE 3  (MB)',
                        'PORCENTAJE DE LOGRO EJE 4  (MB)' 
                        ]

columnas_pensamiento_cientifico = [
                        'RESPONDIÓ PENSAMIENTO CIENTÍFICO',
                        'PENSAMIENTO CIENTÍFICO Pregunta 1',
                        'PENSAMIENTO CIENTÍFICO Pregunta 2',
                        'PENSAMIENTO CIENTÍFICO Pregunta 3',
                        'PENSAMIENTO CIENTÍFICO Pregunta 4',
                        'PENSAMIENTO CIENTÍFICO Pregunta 5',
                        'PENSAMIENTO CIENTÍFICO Pregunta 6',
                        'PENSAMIENTO CIENTÍFICO Pregunta 7',
                        'PENSAMIENTO CIENTÍFICO Pregunta 8',
                        'PENSAMIENTO CIENTÍFICO Pregunta 9',
                        'PENSAMIENTO CIENTÍFICO Pregunta 10',
                        'PENSAMIENTO CIENTÍFICO Pregunta 11',
                        'PENSAMIENTO CIENTÍFICO Pregunta 12',
                        'PENSAMIENTO CIENTÍFICO Pregunta 13',
                        'PENSAMIENTO CIENTÍFICO Pregunta 14',
                        'PENSAMIENTO CIENTÍFICO Pregunta 15',
                        'PENSAMIENTO CIENTÍFICO Pregunta 16',
                        'PENSAMIENTO CIENTÍFICO Pregunta 17',
                        'PENSAMIENTO CIENTÍFICO Pregunta 18',
                        'PENSAMIENTO CIENTÍFICO Pregunta 19',
                        'PENSAMIENTO CIENTÍFICO Pregunta 20',
                        'PENSAMIENTO CIENTÍFICO Pregunta 21',
                        'PENSAMIENTO CIENTÍFICO Pregunta 22',
                        'PENSAMIENTO CIENTÍFICO Pregunta 23',
                        'PENSAMIENTO CIENTÍFICO Pregunta 24',
                        'PUNTAJE TOTAL  (PC)', 
                        'PORCENTAJE DE LOGRO (PC)',
                        'PENSAMIENTO CIENTÍFICO Dimensión 1',
                        'PENSAMIENTO CIENTÍFICO Dimensión 2',
                        'PENSAMIENTO CIENTÍFICO Dimensión 3',
                        'PENSAMIENTO CIENTÍFICO Dimensión 4',
                        'PENSAMIENTO CIENTÍFICO Dimensión 5',
                        'PORCENTAJE LOGRO Dimensión 1',
                        'PORCENTAJE LOGRO Dimensión 2',
                        'PORCENTAJE LOGRO Dimensión 3',
                        'PORCENTAJE LOGRO Dimensión 4',
                        'PORCENTAJE LOGRO Dimensión 5',
                        'PAR 1',
                        'PAR 2',
                        'PAR 3',
                        'PAR 4',
                        'PAR 5',
                        'PAR 6',
                        'PAR 7',
                        'PAR 8',
                        'PAR 9',
                        'PAR 10',
                        'PAR 11',
                        'PAR 12',
                        'NÚMERO DE PARES',
                        'PENSAMIENTO CIENTÍFICO CATEGORÍA '

                        ]

columnas_escritura_academica = [
		'RESPONDIÓ ESCRITURA ACADÉMICA',
		'ESCRITURA ACADÉMICA Pauta 1',
		'ESCRITURA ACADÉMICA Pauta 2',
		'ESCRITURA ACADÉMICA Pauta 3',
		'ESCRITURA ACADÉMICA Pauta 4',
		'ESCRITURA ACADÉMICA Pauta 5',
		'ESCRITURA ACADÉMICA Pauta 6',
		'ESCRITURA ACADÉMICA Pauta 7',
		'ESCRITURA ACADÉMICA Pauta 8',
		'PUNTAJE TOTAL  (EA)',
		'PORCENTAJE DE LOGRO (EA)',
		'PORCENTAJE DE LOGRO Dimensión 1',
		'PORCENTAJE DE LOGRO Dimensión 2',
		'PORCENTAJE DE LOGRO Dimensión 3',
		'PORCENTAJE DE LOGRO Dimensión 4',
		'PORCENTAJE DE LOGRO Dimensión 5',
		'PORCENTAJE DE LOGRO Dimensión 6',
		'PORCENTAJE DE LOGRO Dimensión 7',
		'PORCENTAJE DE LOGRO Dimensión 8'
]

def obtener_facultades(base):
    facultades = list(set(base.FACULTAD))
    i = 0
    while i < len(facultades):
        if isinstance(facultades[i],str) :
            i = i + 1
        else :
            facultades.pop(i)
    return facultades

def definir_diagnosticos(lista_facultades): 
    i = 0
    
    diagnosticos = []
    while i < len(lista_facultades) :
        lista_diagnosticos = ['SOCIOEDUCATIVO', 'MATEMÁTICA A', 'MATEMÁTICA B',
     'PENSAMIENTO CIENTÍFICO', 'ESCRITURA ACADÉMICA']
        diagnostico_facultad = []
        j = 0
        while j < 3 :
            instrumento = random.choice(lista_diagnosticos)
            diagnostico_facultad.append(instrumento)
            lista_diagnosticos.remove(instrumento)
            j = j + 1
        diagnosticos.append(diagnostico_facultad)
        i = i + 1
    return diagnosticos

#######################################################################
# SIMULAR RESPUESTAS SOCIOEDUCATIVO
#######################################################################

def responderSocioeducativo(index):
    lista = []
    sexos = ['Femenino','Masculino','Otro']
    nacionalidades = ['Peruano(a)', 'Argentino(a)', 'Colombiano(a)', 
                    'Venezolano(a)', 'Haitiano(a)', 'Español(a)', 
                    'Brasileño(a)', 'Ecuatoriano(a)'
                    ]
    binario = ['Sí','No']
    opc_pregunta12 = ['En esta misma universidad',
                       'En otra universidad',
                       'En un Centro de Formación Técnica (CFT) o Instituto Profesional (IP)',
                       'En otra institución de Educación Superior'
                     ]
    opc_pregunta14 = ['Mi madre y/o mi padre',
                    'Un familiar cercano (por ej. abuelos/as, hermanos/as, tíos/as)',
                    'Yo',
                    'Otro'
                    ]
    opc_pregunta15 = ['Con mi madre y/o mi padre',
                    'Con otro familiar cercano (por ej. abuelos/as, hermanos/as, tíos/as)',
                    'Con mi pareja o amigos/as',
                    'Solo/a',
                    'Con otras personas no cercanas (por ej. pensión)'
                    ]
    opc_pregunta19 = ['Necesito sostener económicamente a mi familia o hijo(a)',
                    'Necesito financiar mis estudios',
                    'Necesito aportar económicamente a mi hogar',
                    'Necesito costear gastos personales (transporte, vestimenta, alimentación, esparcimiento)',
                    'Otro motivo'
                    ]

    # Se genera un random para representar casos que no respondieron
    if random.random() < 0.05 :
        respondio = 'NO'
        return ['NO'] + [''] * 67
    else : 
        respondio = 'SI'
    lista.append(respondio)
    # Pregunta 1: Correo: Se usará el mismo correo por temas de rendimiento
    lista.append( base.loc[index].CORREO)
    # Pregunta 2: Sexo
    if random.random() < 0.09 :
        lista.append(random.choice(sexos))
    else :
        lista.append( base.loc[index].SEXO)
    # Pregunta 3: ¿Edad?
    edad = 2020 - int(base.loc[index].FECHA_NACIMIENTO.split('-')[2])
    lista.append(edad)
    # Pregunta 4: Nacionalidad
    if random.random() < 0.09 :
        lista.append(random.choice(nacionalidades))
    else: 
        lista.append( 'Chileno(a)' )
    # Pregunta 5: 
    lista.append(random.choice(binario))
    # Pregunta 6: 
    if random.random() < 0.09 :
        lista.append(random.choice(['Sí', 
                                'No, pero pertenezco a un pueblo originario.',
                                'No poseo certificado, ni pertenezco a un pueblo originario.']))
    else :
        lista.append('Sí')
    # Pregunta 7: 
    lista.append(random.choice(binario))
    # Pregunta 8: 
    lista.append(random.choice(binario))
    # Pregunta 9: 
    lista.append(random.choice(binario))
    # Pregunta 10: 
    lista.append(random.choice(binario))
    # Pregunta 11: 
    if random.random() < 0.35 : 
        lista.append('Sí')
    else :
        lista.append('No')
    # Pregunta 12:
    if lista[-1] == 'Sí' :
        lista.append(random.choice(opc_pregunta12))
    else :
        lista.append('')
    # Pregunta 13:
    lista.append(random.choice(binario))
    # Pregunta 14: ¿Con quien vivirás durante el año académico?
    var_preg14 = random.random()
    if var_preg14 > 0.4 :
       
        lista.append(opc_pregunta14[0])
    elif var_preg14 > 0.3 :
        lista.append(opc_pregunta14[1])
    elif var_preg14 > 0.15 :
        lista.append(opc_pregunta14[2])
    else :
        lista.append(opc_pregunta14[3])
    # Pregunta 15: 
    var_preg15 = random.random()
    if var_preg15 > 0.5 :
        lista.append(opc_pregunta15[0])
    elif var_preg15 > 0.4 :
        lista.append(opc_pregunta15[1])
    elif var_preg15 > 0.25 :
        lista.append(opc_pregunta15[2])
    elif var_preg15 > 0.15 :
        lista.append(opc_pregunta15[3])
    else :
        lista.append(opc_pregunta15[4])

    # Pregunta 16: 
    lista.append( random.choice(binario))
    # Pregunta 17: 
    lista.append( random.choice(binario))
    # Pregunta 18: 
    if random.random() < 0.45 :
        lista.append('Sí')
    else :
        lista.append('No')

    # Pregunta 19
    if lista[-1] == 'Sí' :
        lista.append( random.choice(opc_pregunta19))
    else :
        lista.append('')
    # Pregunta 20:
    lista.append(random.choice(binario))
    # Preguntas 21 a 67
    preguntasAdicionales = [random.randint(1, 5) for iter in range(10)]
    preguntasAdicionales += [random.randint(1, 4) for iter in range(4)]
    preguntasAdicionales += [random.randint(1, 4) for iter in range(9)]
    preguntasAdicionales += [random.randint(1, 4) for iter in range(4)]
    preguntasAdicionales += [random.randint(1, 4) for iter in range(4)]
    preguntasAdicionales += [random.randint(1, 5) for iter in range(12)]
    preguntasAdicionales += [random.randint(1, 4) for iter in range(4)]

    lista = lista + preguntasAdicionales

    return lista


def calcularResultadosSocioeducativo(puntajes):
    resultados = []
    preguntas = [10,4,9,4,4,5,4,3,4]
    if puntajes[0] == 'NO':
        return  [''] * 36
    # PUNTAJE ESCALA CONFLICTOS TRANSICIÓN	
    resultados.append(sum(puntajes[21:32]))
    # PUNTAJE ESCALA  MOTIVACIONES ACADÉMICAS	
    resultados.append(sum(puntajes[31:36]))
    # PUNTAJE ESCALA  EXPECTATIVAS ACADÉMICAS	
    resultados.append(sum(puntajes[35:44]))
    # PUNTAJE ESCALA  DESIGUALDAD PERCIBIDA	
    resultados.append(sum(puntajes[43:49])) 
    # PUNTAJE ESCALA  PERCEPCIÓN DE LA DOCENCIA	
    resultados.append(sum(puntajes[48:52])) 
    # PUNTAJE ESCALA  DISTRACCIÓN Y PROCASTINACIÓN	
    resultados.append(puntajes[63]+puntajes[59]+puntajes[60]+puntajes[56]+puntajes[53])  
    # PUNTAJE ESCALA  ANSIEDAD ACADÉMICA	
    resultados.append(puntajes[52]+puntajes[58]+puntajes[54]+puntajes[62])   
    # PUNTAJE ESCALA  SELECCIÓN DE IDEAS PRINCIPALES	
    resultados.append(puntajes[61]+puntajes[55])  
    # PUNTAJE ESCALA  USO ACADÉMICO DE TECNOLOGÍA	
    resultados.append(sum(puntajes[64:69])) 
    # MEDIAS
    i = 0
    while i < 9 :
        resultados.append(round(resultados[i]/preguntas[i], 2))
        i = i + 1 
    # PUNTAJES ESTANDARIZADOS
    i = 0
    while i < 9 :
        puntaje_estandarizado = (resultados[i] * 100) /(preguntas[i] * 5)
        resultados.append(puntaje_estandarizado)
        i = i + 1
     
    # 	NIVELES DE ESCALA
    i = 0
    while i < 9 : 
        if resultados[18 + i] > 75 :
            resultados.append('ALTO')
        elif resultados[18 + i] > 30 :
            resultados.append('MEDIO')
        else :
            resultados.append('BAJO')
        i = i + 1
    return resultados



def responderSocioeducativos(data, lista_facultades, lista_diagnosticos):
    total = []
    for index, rows in data.iterrows():
               
        fac = data.loc[index].FACULTAD
        
        indice = lista_facultades.index(fac) 
        if 'SOCIOEDUCATIVO' in lista_diagnosticos[indice] :
            respuesta = responderSocioeducativo(index)
            resultado = calcularResultadosSocioeducativo(respuesta)
            fila = respuesta + resultado
            
        else : 
            fila = ['NO'] + [''] * 103
        total.append(fila)
    return total


#######################################################################
# SIMULAR RESPUESTAS MATEMÁTICA A
#######################################################################

def responderMatematicaA(index):
    respuestas = []
    # Se genera un random para representar casos que no respondieron
    if random.random() < 0.05 :
        return ['NO'] + [''] * 29
    respuestas.append('SI')
    # Preguntas 1 a 26
    preguntasAdicionales = [random.randint(0, 1) for iter in range(26)]
    respuestas += preguntasAdicionales
    # Preguntas 27, 28 y 29
    preguntasAdicionales = [random.randint(0, 1) + random.randint(0,1)/2 for iter in range(3)]
    respuestas += preguntasAdicionales
    return respuestas

def calcularResultadosMatematicaA(respuestas):
    if respuestas[0] == 'NO' :
        return [''] * 28
    resultados = []
    puntajesXObjetivo = [3,4,3.5,4.5,3,4.5,3,2,3]
    puntajesXEjeTematico = [7,11,7.5,5]
    # Puntaje total
    resultados.append(round(sum(respuestas[1:len(respuestas)]),2))
    # Porcentaje de logro
    resultados.append(resultados[0] / 30.5) # PORCENTAJE
    # Puntaje Objetivo 1
    resultados.append(sum(respuestas[1:4]))
    # Puntaje Objetivo 2
    resultados.append(sum(respuestas[4:8]))
    # Puntaje Objetivo 3
    suma = respuestas[9] + respuestas[14] + respuestas[28]
    resultados.append(suma)
    # Puntaje Objetivo 4
    suma = respuestas[12] + respuestas[13] + respuestas[15]+respuestas[15]
    resultados.append(suma)
    # Puntaje Objetivo 5 
    suma = respuestas[10] + respuestas[11] + respuestas[16]
    resultados.append(suma)
    # Puntaje Objetivo 6 
    suma = respuestas[24] + respuestas[25] + respuestas[26]+respuestas[27]
    resultados.append(suma)
    # Puntaje Objetivo 7
    suma = respuestas[21] + respuestas[22] + respuestas[23]
    resultados.append(suma)
    # Puntaje Objetivo 8 
    suma = respuestas[19] + respuestas[20] 
    resultados.append(suma)
    # Puntaje Objetivo 9
    suma = respuestas[8] + respuestas[17] + respuestas[18]
    resultados.append(suma)
    # Porcentajes de logro
    i = 2
    while i < 11 :
        porcentajeDeLogro = resultados[i]  / puntajesXObjetivo[i - 2] # PORCENTAJE
        resultados.append(round(porcentajeDeLogro, 2))
        i = i + 1
    aux = []
    # EJE TEMÁTICO 1 
    suma = sum(respuestas[1:8])
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[0], 2)) # PORCENTAJE
    # EJE TEMÁTICO 2 
    suma = respuestas[8] + respuestas[16] + respuestas[28] + respuestas[29]
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[1] , 2)) # PORCENTAJE
    # EJE TEMÁTICO 3 
    suma = sum(respuestas[21:28])
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[2],2)) # PORCENTAJE
    # EJE TEMÁTICO 4
    suma = respuestas[8]+sum(respuestas[17:21])
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[3],2)) # PORCENTAJE

    resultados = resultados + aux
    return resultados

def responderMatematicasA(data, lista_facultades, lista_diagnosticos):
    total = []
    for index, rows in data.iterrows():
               
        fac = data.loc[index].FACULTAD
        
        indice = lista_facultades.index(fac) 
        if 'MATEMÁTICA A' in lista_diagnosticos[indice] :
            respuesta = responderMatematicaA(index)
            resultado = calcularResultadosMatematicaA(respuesta)
            fila = respuesta + resultado
        else : 
            fila = ['NO'] + [''] * (29 + 28)
        total.append(fila)
    return total


#######################################################################
# SIMULAR RESPUESTAS MATEMÁTICA B
#######################################################################
def responderMatematicaB(index):
    respuestas = []
    # Se genera un random para representar casos que no respondieron
    if random.random() < 0.05 :
        return ['NO'] + [''] * 19
    respuestas.append('SI')
    # Preguntas 1 a 17
    preguntasAdicionales = [random.randint(0, 1) for iter in range(17)]
    respuestas += preguntasAdicionales
    # Preguntas 18 y 19
    preguntasAdicionales = [random.randint(0, 1) + random.randint(0,1)/2 for iter in range(2)]
    respuestas += preguntasAdicionales
    return respuestas


def calcularResultadosMatematicaB(respuestas):
    if respuestas[0] == 'NO' :
        return [''] * 20
    resultados = []
    puntajesXObjetivo = [6,3,3,5.5,2.5]
    puntajesXEjeTematico = [9,3,5.5,2.5]
    # Puntaje total
    resultados.append(round(sum(respuestas[1:len(respuestas)]),2))
    # Porcentaje de logro
    resultados.append(resultados[0] / 20) # PORCENTAJE
    # Objetivo 1 GD2:GI2
    resultados.append(sum(respuestas[1:7]))
    # Objetivo 2 GJ2;GK2;GO2
    suma = respuestas[7] + respuestas[8] + respuestas[12]
    resultados.append(suma)
    # Objetivo 3 GL2;GM2;GN2
    suma = respuestas[9] + respuestas[10] + respuestas[11]
    resultados.append(suma)
    # Objetivo 4 GQ2:GT2;GV2
    suma = sum(respuestas[14:18]) + respuestas[19]
    resultados.append(suma)
    # Objetivo 5 GP2;GU2
    suma = respuestas[13] + respuestas[18]
    resultados.append(suma)
    # PORCENTAJE DE LOGRO POR OBJETIVO
    i = 2
    while i < 7 :
        porcentajeDeLogro = resultados[i]  / puntajesXObjetivo[i - 2] # PORCENTAJE
        resultados.append(round(porcentajeDeLogro, 2))
        i = i + 1
    # EJES TEMÁTICOS
    aux = [] 
    # EJE TEMÁTICO 1 GD2:GK2;GO2
    suma = sum(respuestas[1:9]) + respuestas[12]
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[0], 2))
    # EJE TEMÁTICO 2 GL2:GN2  
    suma = sum(respuestas[9:13])
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[1], 2))
    # EJE TEMÁTICO 3 GQ2:GU2
    suma = sum(respuestas[14:19])
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[2], 2))
    # EJE TEMÁTICO 4 GP2;GV2
    suma = respuestas[13] + respuestas[19]
    resultados.append(suma)
    aux.append(round(suma / puntajesXEjeTematico[3], 2))
    resultados = resultados + aux
    return resultados

def responderMatematicasB(data, lista_facultades, lista_diagnosticos):
    total = []
    
    for index, rows in data.iterrows():
               
        fac = data.loc[index].FACULTAD
        
        indice = lista_facultades.index(fac) 
        if 'MATEMÁTICA B' in lista_diagnosticos[indice] :
            respuesta = responderMatematicaB(index)
            resultado = calcularResultadosMatematicaB(respuesta)
            fila = respuesta + resultado
        else : 
            fila = ['NO'] + [''] * (19 + 20)
        
        
        total.append(fila)
    
    return total



#######################################################################
# SIMULAR RESPUESTAS PENSAMIENTO CIENTÍFICO
#######################################################################
def responderPensamientoCientifico(index):
    respuestas = []
    # Se genera un random para representar casos que no respondieron
    if random.random() < 0.05 :
        return ['NO'] + [''] * 24
    respuestas.append('SI')
    # Preguntas 1 a 17
    preguntasAdicionales = [random.randint(0, 1) for iter in range(24)]
    respuestas += preguntasAdicionales
    return respuestas

def calcularResultadosPensamientoCientifico(respuestas):
    if respuestas[0] == 'NO' :
        return [''] * 26
    resultados = []
    puntajesXDimension = [4,4,6,4,6]
    # Puntaje total
    resultados.append(round(sum(respuestas[1:len(respuestas)]),2))
    # Porcentaje de logro
    resultados.append(resultados[0] / 24) # PORCENTAJE
    # Dimensión 1 HR:HU
    suma = sum(respuestas[1:5])
    resultados.append(suma)
    # Dimensión 2 HV:HY
    suma = sum(respuestas[5:9])
    resultados.append(suma)
    # Dimensión 3 HZ:IE
    suma = sum(respuestas[9:15])
    resultados.append(suma)
    # Dimensión 4 IF:II
    suma = sum(respuestas[15:19])
    resultados.append(suma)
    # Dimensión IJ:IO
    suma = sum(respuestas[19:25])
    resultados.append(suma)
    # PORCENTAJE DE LOGRO
    i = 2
    while i < 7 :
        porcentajeDeLogro = resultados[i]  / puntajesXDimension[i - 2] # PORCENTAJE
        resultados.append(round(porcentajeDeLogro, 2))
        i = i + 1
    # PARES
    pares = []
    i  = 1
    while i < len(respuestas):
        if respuestas[i] == 1 and respuestas [i+1] == 1 :
            pares.append(1)
        else :
            pares.append(0)
        i = i + 2
    resultados += pares 
    sumaDePares = sum(pares)
    resultados.append(sumaDePares)
    if sumaDePares < 5 :
        resultados.append('Concreto')
    elif sumaDePares < 10 :
        resultados.append('Transicional')
    else :
        resultados.append('Formal')
    return resultados


def responderPensamientoCientificos(data, lista_facultades, lista_diagnosticos):
    total = []
    
    for index, rows in data.iterrows():
               
        fac = data.loc[index].FACULTAD
        
        indice = lista_facultades.index(fac) 
        if 'PENSAMIENTO CIENTÍFICO' in lista_diagnosticos[indice] :
            respuesta = responderPensamientoCientifico(index)
            resultado = calcularResultadosPensamientoCientifico(respuesta)
            fila = respuesta + resultado
        else : 
            fila = ['NO'] + [''] * (24 + 26)
        
        
        total.append(fila)
    
    return total

#######################################################################
# SIMULAR RESPUESTAS ESCRITURA ACADÉMICA
#######################################################################
def responderEscrituraAcademica(index):
    respuestas = []
    # Se genera un random para representar casos que no respondieron
    if random.random() < 0.05 :
        return ['NO'] + [''] * 8
    respuestas.append('SI')
    # Preguntas 1 a 17
    preguntasAdicionales = [random.randint(0, 4) for iter in range(8)]
    respuestas += preguntasAdicionales
    return respuestas

def calcularResultadosEscrituraAcademica(respuestas):
    if respuestas[0] == 'NO' :
        return [''] * 10
    resultados = []
    # Puntaje total
    resultados.append(round(sum(respuestas[1:len(respuestas)]),2))
    # Porcentaje de logro
    resultados.append(resultados[0] / 32)
    # PORCENTAJE DE LOGRO FINAL
    i = 1
    while i < len(respuestas) :
        porcentaje = respuestas[i] / 4
        resultados.append(porcentaje)
        i = i + 1

    return resultados

def responderEscrituraAcademicas(data, lista_facultades, lista_diagnosticos):
    total = []
    
    for index, rows in data.iterrows():
               
        fac = data.loc[index].FACULTAD
        
        indice = lista_facultades.index(fac) 
        if 'ESCRITURA ACADÉMICA' in lista_diagnosticos[indice] :
            respuesta = responderEscrituraAcademica(index)
            resultado = calcularResultadosEscrituraAcademica(respuesta)
            fila = respuesta + resultado
        else : 
            fila = ['NO'] + [''] * (8 + 10)
        
        
        total.append(fila)
    
    return total



def agregarDataSimulada(total, columnas, data):
    
    total.insert(0, columnas)
    aux = np.matrix(total)
    aux = aux.transpose()
    filas, columnas = aux.shape
    
    aux = np.array(aux)
    i = 0
    while i < filas :
        
        vector = aux[i]
        columna = vector[0]
        
        datos = vector[1:columnas]
        data[columna] = datos 
        i = i + 1
    return data

base = pd.read_excel(NOMBRE_ARCHIVO_ENTRADA, index_col=0)

lista_facultades = obtener_facultades(base)

lista_diagnosticos = definir_diagnosticos(lista_facultades)

base.columns = [c.replace(' ', '_') for c in base.columns]

total = responderSocioeducativos(base, lista_facultades, lista_diagnosticos)
aux = agregarDataSimulada(total, columnas_socioeducativo, base)
print('Pasó socioeducativo')

total = responderMatematicasA(base, lista_facultades, lista_diagnosticos)
aux  = agregarDataSimulada (total, columnas_matematica_a, base)
print('Pasó mate A')

total = responderMatematicasB(base, lista_facultades, lista_diagnosticos)
aux  = agregarDataSimulada(total, columnas_matematica_b, base)
print('Pasó mate B')


total = responderPensamientoCientificos(base, lista_facultades, lista_diagnosticos)
aux  = agregarDataSimulada(total, columnas_pensamiento_cientifico, base)
print('Pasó cientifico')

total = responderEscrituraAcademicas(base, lista_facultades, lista_diagnosticos)
aux  = agregarDataSimulada(total, columnas_escritura_academica, base)
print('Pasó escritura')

aux.columns = [c.replace('_', ' ') for c in base.columns]
aux.to_excel(NOMBRE_ARCHIVO_SALIDA, sheet_name='ESTUDIANTES', index=True)

