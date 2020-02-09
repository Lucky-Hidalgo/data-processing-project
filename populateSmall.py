import pandas as pd
import random
from faker import Faker
from itertools import cycle
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


NOMBRE_ARCHIVO_ENTRADA = 'carreras.xlsx'
NOMBRE_ARCHIVO_SALIDA = 'salida-big.xlsx'

RUTS = []

# Se necesitan 5 diagnósticos
    # SOCIOEDUCATIVO
    # MATEMÁTICA A
    # MATEMÁTICA B
    # PENSAMIENTO CIENTÍFICO
    # ESCRITURA ACADÉMICA

def obtener_facultades(base):
    facultades = list(set(base.FACULTAD))
    i = 0
    while i < len(facultades):
        if isinstance(facultades[i],str) :
            i = i + 1
        else :
            facultades.pop(i)
    return facultades

def crear_diccionario_facultades(data, facultades):
    
    dict_facultades = dict()
    for e in facultades :
        dict_facultades[e.upper()] = []
    
    for e in data.iterrows() :
        
        carr = e[1]
        if isinstance(carr.FACULTAD, str) :
            datos_carrera = [carr.CARRERA, int(carr.CUPOS), int(carr.SUPERNUM), int(carr.PACE)]
            dict_facultades[carr.FACULTAD].append(datos_carrera) 


    return dict_facultades


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


def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11

def crear_persona(facultad, carrera, via):
    fake = Faker(['es_MX','en_AU', 'en_US', 'es_ES', 'it_IT', 'pt_BR'])
    cod_sexo  = random.randint(0,1)
    if cod_sexo == 0 :
        sexo = 'FEMENINO'
        nom1 = fake.first_name_female()
        nom2 = fake.first_name_female()
        ape1 = fake.last_name()
        ape2 = fake.last_name()
    else :
        sexo = 'MASCULINO'
        nom1 = fake.first_name_male()
        nom2 = fake.first_name_male()
        ape1 = fake.last_name()
        ape2 = fake.last_name()

    run = random.randint(18000000,21000000)
    while run in RUTS :
        run = random.randint(18000000,21000000)    
    RUTS.append(run)
    dv = digito_verificador(run)
    if dv == 10 :
        
        dv = 'K'

    # nombre_usuario
    nombre_usuario = str(run)
    # clave
    clave = nombre_usuario[0:4]
    # nombres
    nombres = nom1.upper() + ' ' + nom2.upper()
    # apellidos
    apellidos = ape1.upper() + ' ' + ape2.upper() 
    # correo
    correo = nom1 + '.' + ape1 + '.' + ape2[0] + '@usach.cl'
    correo = correo.lower()
    # rut
    rut = nombre_usuario + '-' + str(dv)
    # proceso
    proceso = 2020
    # sexo
    #Ya está
    # fecha de nacimiento
    date = fake.date_between(start_date='-30y', end_date='-20y')
    fecha_nacimiento = str(date.day)+'-'+str(date.month)+'-'+str(date.year)
    # preferencia
    preferencia = random.choice([1,2,3])
    # anio_egreso
    anio_egreso = random.choice([2019,2019,2019,2019,2019,2018,2018,2018,2017])
    # nem
    nem = float(str(random.randint(4,6)) + '.' + str(random.randint(0,9)) + str(random.randint(0,9)))
    # puntaje_nem
    puntaje_nem = int(nem * 850 / 7.0)
    # puntaje_ranking
    puntaje_ranking = puntaje_nem + random.randint(-50,50)
    if puntaje_ranking > 850 :
        puntaje_ranking = 850 
    # puntaje psu lyc
    puntaje_psu_lyc = random.randint(550,850)
    # puntaje psu mat
    puntaje_psu_mat = random.randint(550,850)
    # promedio_psu 
    promedio_psu = sum((puntaje_nem,puntaje_ranking, puntaje_psu_lyc, puntaje_psu_mat))/4
    # via_ingreso
    if via == 0 :
        via_ingreso = 'CUPO P.S.U'
    if via == 1 :
        via_ingreso = random.choice(
            ['OTROS', 
            'CUPO R850', 
            'CUPO PROPEDEUTICO',
            'CUPO PARES',
            'CUPO DEPORTE',
            'CUPO BEA',
            'CUPO OFICIO DEMRE',
            'CUPO HIJO FUNC.'
            ])
    if via == 2 :
        via_ingreso = 'CUPO PACE'
    # Dependencia
    dependencia = random.choice(['MUNICIPAL','PARTICULAR', 'SUBVENCIONADO'])
    # Consentimiento informado
    cons_inf = random.random()
    if cons_inf < 0.05 :
        consentimiento_informado = 'NO'
    else :
        consentimiento_informado = 'SI'
    persona = [
        nombre_usuario, 
        clave,
        nombres,
        apellidos,
        correo,
        rut,
        proceso,
        sexo,
        fecha_nacimiento,
        facultad,
        carrera,
        preferencia,
        anio_egreso,
        nem,
        puntaje_nem,
        puntaje_ranking,
        puntaje_psu_lyc,
        puntaje_psu_mat,
        promedio_psu,
        via_ingreso,
        dependencia,
        consentimiento_informado
    ]
    return persona

# Recibe como entrada el diccionario facultades
def poblar_personas(facultades, nom_facultad) :
    global j

    facultad = facultades[nom_facultad]
    for e in facultad :
        
        carrera = e[0]
        i = 0
        while i < e[1]:
            persona = crear_persona(nom_facultad, carrera, 0)
            TODO.loc[j] = persona
            j = j + 1
            i = i + 1
        i = 0
        while i < e[2]:
            persona = crear_persona(nom_facultad, carrera, 1)
            TODO.loc[j] = persona
            j = j + 1
            i = i + 1
        i = 0
        while i < e[3] :
            persona = crear_persona(nom_facultad, carrera, 2)
            TODO.loc[j] = persona
            j = j + 1
            i = i + 1
    




base = pd.read_excel(NOMBRE_ARCHIVO_ENTRADA, index_col=0)

lista_facultades = obtener_facultades(base)

facultades = crear_diccionario_facultades(base,lista_facultades)

lista_diagnosticos = definir_diagnosticos(lista_facultades)


j = 0
TODO = pd.DataFrame(
        columns=(
            'NOMBRE_USUARIO', 
            'CLAVE',
            'NOMBRES',
            'APELLIDOS',
            'CORREO',
            'RUT',
            'PROCESO',
            'SEXO',
            'FECHA_NACIMIENTO',
            'FACULTAD',
            'CARRERA',
            'PREFERENCIA',
            'ANIO_EGRESO',
            'NEM',
            'PUNTAJE_NEM',
            'PUNTAJE_RANKING',
            'PUNTAJE_PSU_LYC',
            'PUNTAJE_PSU_MAT', 
            'PROMEDIO_PSU',
            'VIA_INGRESO',
            'DEPENDENCIA',
            'CONSENTIMIENTO_INFORMADO'
            )
        )
for facultad in facultades.keys() :
    nom_facultad = facultad
        
    poblar_personas(facultades, nom_facultad)
TODO.set_index('NOMBRE_USUARIO')
TODO.to_excel('salida-big.xlsx', sheet_name='ESTUDIANTES', index=False)




