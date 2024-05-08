import random
#from main import create_simulation
from environment.simple_simulation import SimpleSimulation
from dill import dump, load

def generar_f(k,q):
    """
    Genera una función de transición f para un autómata finito.

    Args:
        k (int): Número de estados (tipos) en el autómata.
        q (int): Número de símbolos en cada secuencia de transición.

    Returns:
        list: Una lista de tuplas que representa la función de transición f.
              Cada tupla contiene ((estado, adn), estado_destino), donde:
              - estado: El estado actual del autómata.
              - adn: Una secuencia de q símbolos generados aleatoriamente entre 1 y 3.
              - estado_destino: El estado de destino al que transicionar.
    """
    f = []
    for i in range(k): # Por cada estado (Tipo) salen k-1 aristas (Hay una via para ir a los restantes k-1 tipos)  
        for j in range(k-1):              
            adn = [random.randint(1, 3) for _ in range(q)] # Genera q elementos aleatorios entre 1 y 3
            transitionij = ((i,adn),j) # Desde i leyendo adn voy hacia j
            f.append(transitionij) # 
    return f

def crear_f_poblacion_inicial(N, K):
    """
    Crea una población inicial de tamaño N, donde cada individuo tiene K estados iniciales posibles.

    Args:
    - N (int): Total de funciones de transicción a devolver.
    - K (int): Número de estados iniciales de cada función de transicción.

    Returns:
    - list: Lista de funciones iniciales.
    """
    fs_iniciales = []
    for _ in range(N):
        f = generar_f(K,6) #
        fs_iniciales.append(f)
    return fs_iniciales

def reproducir(padres, tamaño_población):
    """
    Genera una nueva lista de funciones de transicción mediante la reproducción de los padres.

    Args:
    - padres (list): Lista de funciones padres disponibles para la reproducción.
    - tamaño_población (int): Cantidad de funciones a devolver.

    Returns:
    - list: Lista de nuevas funciones (hijas) generadas a partir de los funciones padres.
    """
    hijos = []
    for _ in range(tamaño_población):
        padre1 = random.choice(padres)
        padre2 = random.choice(padres)
        hijo = cruzar_Y_mutar(padre1,padre2)
        hijos.append(hijo)
    return hijos

def mutar(adn):
    """
    Realiza una mutación de un trozo de adn.

    Args:
    - adn (list): array que representa un fragmento de adn.

    Returns:
    - list: array con una posición alterada.
    """
    indice = random.randint(0, len(adn)-1)

    mutación = random.randint(1,3)
    
    adn[indice] = mutación

    return adn

#TODO En la versión, el cruze debe cambiar
def cruzar_Y_mutar(padre1, padre2):
    """
    Realiza el cruce y la mutación de los fragmentos de adn entre dos funciones padres para generar una función hijo.

    Args:
    - padre1 list[ ((int,list), int) ]: Primer padre para la reproducción.
    - padre2 list[ ((int,list), int) ]: Segundo padre para la reproducción.

    Returns:
    - list[ ((int,list), int) ]: Nuevo individuo (hijo) resultado del cruce y la mutación.
    """
    f_hijo = []
    for k in range(len(padre1)): 
        par1 = padre1[k]
        par2 = padre2[k]
        comp1_padre1 = par1[0]
        comp1_padre2 = par2[0]
        adn_K_padre1 = comp1_padre1[1]
        adn_K_padre2 = comp1_padre2[1]
        adn_K_hijo = mezclar_Adn(adn_K_padre1,adn_K_padre2)
        adn_K_hijo = mutar(adn_K_hijo)
        new_estado_adn = (comp1_padre1[0], adn_K_hijo)
        if new_estado_adn not in f_hijo:
            nueva_transiccion = ((comp1_padre1[0], adn_K_hijo), par1[1])
            f_hijo.append(nueva_transiccion)
            
        else:
            # Realizar alguna acción para manejar la colisión de claves, como ignorarla o modificarla
            adn_k_hijo_extra = mutar(adn_K_hijo)
            nueva_transiccion = ((comp1_padre1[0], adn_k_hijo_extra), par1[1])
            f_hijo.append(nueva_transiccion)
    return f_hijo

def mezclar_Adn(adn_padre1, adn_padre2):
    adn_hijo = [0]*len(adn_padre1)
    punto_de_cruce = random.randint(1, len(adn_padre1) - 2)
    for i in range(0, punto_de_cruce):
        adn_hijo[i] = adn_padre1[i]
    for i in range(punto_de_cruce+1, len(adn_padre2)):
        adn_hijo[i] = adn_padre2[i]
    return adn_hijo


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
    adn_poblacion = crear_f_poblacion_inicial(tamaño_población,6)  
    adn_optimo = []
    for _ in range(generaciones):
        agents, id_ADN = create_agents_ADN(adn_poblacion) #TODO Como asocio ADN con agente?
        #simulation = create_simulation(50,50,tamaño_población)
        #while not simulation.__has_ended__():
        #    simulation.step(
        #    sleep_time=0.0001
        #) # Necesito Turnos que sobrevivio, Recursos que recolecto, combates en los que participo
        #result = simulation.returnResult
        
        result = {}

        mejor_poblacion = seleccionar_mejor_población(id_ADN, result, tamaño_población) # Selecciona los K mejores

        adn_optimo = mejor_poblacion[0] # Guarda el agente optimo de está generación

        adn_poblacion = reproducir(mejor_poblacion, tamaño_población) # Devuelve solo el ADN

    with open("SuperAgente.joblib", "wb") as a:
        dump(adn_optimo, a)

#algoritmo_genético(10, 10)

A = [((1,[1,2,3,1,2,3,1]),1), ((2,[3,2,1,1,1,3,1]),2)]
B = [((1,[1,1,1,1,1,3,1]),1), ((2,[1,2,3,3,3,3,1]),2)]

def create_agents_ADN(adn_poblacion):
    pass

def Sensor(aliados, enemigos, recursos, vitalidad, reserva, hostilidades, asociaciones):
    """
    Evalúa las características del entorno y devuelve una tupla con valores que representan la valoración de cada atributo.

    Args:
        aliados (int): Cantidad de aliados presentes en el entorno.
        enemigos (int): Cantidad de enemigos presentes en el entorno.
        recursos (int): Cantidad de recursos visibles en el entorno.
        vitalidad (int): Nivel de vitalidad del agente.
        reserva (int): Cantidad de reservas del agente.
        hostilidades (int): Cantidad de hostilidades ocurridas en el último turno.
        asociaciones (int): Cantidad de asociaciones realizadas en el último turno.

    Returns:
        tuple: Una tupla que representa la valoración de cada atributo en el siguiente orden:
               - Cantidad de aliados valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de enemigos valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de recursos valorada como bajo(1), medio(2) o alto(3).
               - Nivel de vitalidad valorado como bajo(1), medio(2) o alto(3).
               - Cantidad de reservas valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de hostilidades valorada como bajo(1), medio(2) o alto(3).
               - Cantidad de asociaciones valorada como bajo(1), medio(2) o alto(3).
    """
    cantEnemigos = 0
    cantAliados = 0
    cantRecursos = 0
    cantVitalidad = 0
    cantReserva = 0
    cantHostilidades = 0
    cantAsociaciones = 0

    #recursos
    if(recursos > 6):
        pass
    elif():
        pass
    else:
        pass
    #aliados 
    if(aliados >= 4):
        cantAliados = 3
    elif(aliados <= 3 and aliados > 1):
        cantAliados = 2
    else:
        cantAliados = 1
    #enemigos 
    if(enemigos >= 4 ):
        cantEnemigos = 3
    elif(enemigos <= 3 and enemigos >1):
        cantEnemigos = 2
    else:
        cantEnemigos = 1

    #Vitalidad
    if(vitalidad > 150):
        cantVitalidad = 3
    elif(vitalidad <= 150 and vitalidad > 40):
        cantVitalidad = 2
    else:
        cantVitalidad = 1
    #Reservas
    if(reserva > 150):
        cantReserva = 3
    elif(reserva <= 150 and reserva > 40):
        cantReserva = 2
    else:
        cantReserva = 1

    #Asociaciones
    if(asociaciones > 5):
        cantAsociaciones = 3
    elif(asociaciones <= 5 and asociaciones >= 3):
        cantAsociaciones = 3
    else:
        cantAsociaciones = 1



    #Hostilidades
    if(hostilidades > 5):
        cantHostilidades = 3
    elif(hostilidades <=4 and hostilidades > 0):
        cantHostilidades = 2
    else:
        cantHostilidades = 1

    return (cantAliados, cantEnemigos, cantRecursos, cantVitalidad, cantReserva, cantHostilidades, cantAsociaciones)



