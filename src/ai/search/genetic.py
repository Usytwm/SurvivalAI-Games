import random
from dill import dump, load
def generar_adn(K):
    arrays = []
    for _ in range(K):
        array = [random.randint(1, 3) for _ in range(6)] # Genera 6 elementos aleatorios entre 1 y 3
        array.append(random.randint(1, 4)) # Genera el séptimo elemento aleatorio entre 1 y 4
        arrays.append(array)
    return arrays

def crear_poblacion_inicial(n, K):
    poblacion_inicial = []
    for _ in range(n):
        diccionario = {i+1: random.choice(generar_adn(K)) for i in range(K)}
        poblacion_inicial.append(diccionario)
    return poblacion_inicial

def seleccionar_padres(mejor_población, tamaño_población):
    padres = random.choices(mejor_población)
    return padres

def reproducir(padres, tamaño_población):
    hijos = []
    for _ in range(tamaño_población):
        padre1 = random.choice(padres)
        padre2 = random.choice(padres)
        hijo = cruzar(padre1,padre2)
        hijo = mutar(hijo)
        hijos.append(hijo)
    return hijos

def mutar(hijo):
    indice = random.randint(0, len(hijo)-1)

    if indice == 6:
        mutación = random.randint(1,4)
    else:
        mutación = random.randint(1,3)

    hijo[indice] = mutación

    return hijo
 
def cruzar(padre1, padre2):
    hijo = [0]*len(padre1)
    punto_de_cruce = random.randint(1, len(padre1) - 2)
    for i in range(0, punto_de_cruce):
        hijo[i] = padre1[i]
    for i in range(punto_de_cruce+1, len(padre2)):
        hijo[i] = padre2[i]
    return hijo


def función_ponderación(caracterisisticas):
    pass

def seleccionar_mejor_población(población, tamaño_población):
    for _ in range():
        
class simulacion:
    a = 3
# Función principal
def algoritmo_genético(poblacion, tamaño_población, generaciones):
    poblacion
    for _ in range(generaciones):
        resultado = simulacion
        mejor_poblacion = seleccionar_mejor_población
        nueva_generacion = reproducir
        poblacion
    with open("SuperAgente.joblib", "wb") as a:
        dump(resultado, a)
    




