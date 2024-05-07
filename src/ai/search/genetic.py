import random
from main import *
from environment.simple_simulation import SimpleSimulation
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

    if indice == (len(hijo)-1):
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
    answer = 0
    for value in caracterisisticas:
        answer+=value
    return answer/len(caracterisisticas)

def seleccionar_mejor_población(id_ADN, result, top_k):
    poblacion_ordenada = []
    for i in range(0,result):
        valor = función_ponderación(result[i][1])
        poblacion_ordenada.append((result[i][0], valor))
    poblacion_ordenada.sort()
    return poblacion_ordenada[top_k:]

# Función principal
def algoritmo_genético(tamaño_población, generaciones):
    adn_poblacion = crear_poblacion_inicial(tamaño_población,6)  
    adn_optimo = []
    for _ in range(generaciones):
        agents, id_ADN = create_agents_ADN(adn_poblacion) #TODO Como asocio ADN con agente?
        simulation = create_simulation(50,50,tamaño_población)
        while not simulation.__has_ended__():
            simulation.step(
            sleep_time=0.0001
        ) # Necesito Turnos que sobrevivio, Recursos que recolecto, combates en los que participo
        result = simulation.returnResult

        mejor_poblacion = seleccionar_mejor_población(id_ADN, result, tamaño_población) # Selecciona los K mejores

        adn_optimo = mejor_poblacion[0] # Guarda el agente optimo de está generación

        adn_poblacion = reproducir(mejor_poblacion, tamaño_población) # Devuelve solo el ADN

    with open("SuperAgente.joblib", "wb") as a:
        dump(adn_optimo, a)

def create_agents_ADN(adn_poblacion):
    pass
def Sensor():

    #parámetro A
    if():
        pass
    elif():
        pass
    else:
        pass


