from typing import List
import numpy 
import random
import math

from solucion import Solucion

D                       = 10
PRECISION               = 3
ALFA                    = 0.8
PROBABILIDAD_MUTACION   = 0.3
POTENCIA_MUTACION       = 0.8
GENERACIONES            = 100
ELITES                  = 1
HIJOS                   = 99
POBLACION               = ELITES + HIJOS             

poblacion: List[Solucion] = []


def driver() -> Solucion:
    
    generar_poblacion_inicial()

    mejor_solucion = None
    for generacion in range(GENERACIONES):

        poblacion.sort(key=lambda solucion: solucion.aptitud, reverse=False)

        mejor_solucion = poblacion[0]
        print(f"Mejor aptitud: {mejor_solucion.aptitud}, Generación: {generacion}", end='\r')
        
        
        hijos = cruzar()
        reemplazar(hijos=hijos)
    return mejor_solucion

def generar_poblacion_inicial():
    for _ in range(POBLACION):
        poblacion.append(generarSolucion())

def generarSolucion() -> Solucion:
    numeros = [round(random.uniform(-5.12, 5.12), PRECISION) for _ in range(D)]
    aptitud = calcular_aptitud(numeros)
    return Solucion(numeros, aptitud)

def calcular_aptitud(numeros: List[float]) -> float:
    numeros_procesados = [aplicar_formula(x) for x in numeros]
    aptitud = round(10 * D + sum(numeros_procesados), PRECISION)
    return aptitud

def aplicar_formula(x: float) -> float:
    return x**2 - 10 * math.cos(2 * math.pi * x)


def cruzar() -> List[Solucion]:
    hijos = []
    for _ in range(HIJOS):

        # por cada HIJO, obtener 2 PADRES:
        padres = seleccionar_ruleta()
        hijo = cruzar_blxalfa(padre1=padres[0], padre2=padres[1])

        hijoMutado = mutar_uniforme(solucion=hijo)
        hijos.append(hijoMutado)
        
    return hijos


def seleccionar_ruleta():
    aptitudes = [solucion.aptitud for solucion in poblacion]
    aptitud_maxima = max(aptitudes)

    '''
    La ruleta favorece aptitudes más grandes, pero la meta es minimizarla,
    entonces se normalizan las aptitudes. 
    '''
    aptitudes_ajustadas = [aptitud_maxima - aptitud + 1 for aptitud in aptitudes]    
    aptitud_total = sum(aptitudes_ajustadas)
    probabilidades = [aptitud / aptitud_total for aptitud in aptitudes_ajustadas]

    padres = set()
    while len(padres) < 2:
        solucion = random.choices(poblacion, weights=probabilidades, k=1)[0]
        padres.add(solucion)
        if len(padres) == 2:
            break

    return list(padres)

def cruzar_blxalfa(
        padre1: Solucion = generarSolucion(), 
        padre2: Solucion = generarSolucion(), 
        alfa = random.uniform(0, 1) # deberia ser siempre el mismo alfa
        ) -> Solucion:

    numeros_hijo = []

    for gen_P1, gen_P2 in zip(padre1.numeros, padre2.numeros):
        '''
        Se recorren ambos padres, comparando cada indice respectivo:
        padre1: [ *1* ,2,3]
        padre2: [ *4* ,5,6]
        '''
        min_gen = min(gen_P1, gen_P2)
        max_gen = max(gen_P1, gen_P2)
        rango_genetico = max_gen - min_gen

        '''
        Se explora el rango. El `límite_inferior` es menor al `min_gen` y
        `limite_superior` es mayor a `max_gen`.
        '''
        limite_inferior = min_gen - rango_genetico * alfa
        limite_superior = max_gen + rango_genetico * alfa


        '''
        Se genera un número aleatorio dentro de esos límites.
        '''
        nuevo_gen = round(random.uniform(limite_inferior, limite_superior), PRECISION)
        numeros_hijo.append(nuevo_gen)

    aptitud_hijo = calcular_aptitud(numeros_hijo)

    return Solucion(numeros = numeros_hijo, 
                    aptitud = aptitud_hijo)

def mutar_uniforme(
        solucion: Solucion = generarSolucion(), 
        probabilidad_mutacion=PROBABILIDAD_MUTACION, 
        potencia_mutacion=POTENCIA_MUTACION
        ) -> Solucion:

    '''
    A cada número de la solución, se le aplica la misma probabilidad de mutar.
    Si muta, se genera una `mutacion`: flotante aleatorio dentro de un rango específico.
    La `mutacion` se suma al número de la solución que se decidió sí mutaría.
    '''
    for i in range(len(solucion.numeros)):
        if numpy.random.rand() < probabilidad_mutacion:
            mutacion = numpy.random.uniform(-potencia_mutacion, potencia_mutacion)
            solucion.numeros[i] += mutacion

    return solucion

def reemplazar(hijos: List[Solucion]):
    del poblacion[ELITES:]
    poblacion.extend(hijos)


mejor_solucion = driver()
print(f"\nMejor aptitud: {mejor_solucion.aptitud}, números: {mejor_solucion.numeros}", end='\n')

#mutar_uniforme()

