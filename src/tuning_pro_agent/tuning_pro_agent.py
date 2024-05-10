import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + 'src/Interfaces')
sys.path.insert(0, current_dir + '/src/agents')
import random
import sqlite3
from typing import List
from Interfaces.IGenetic_SugarScape import IGenetic_SugarScape
from agents.ProAgent.pro_agent import ProAgent

conn = sqlite3.connect(":memory:")

def valley_shaped_distribution_random_number(a : int, b : int):
    """Un numero aleatorio entre a y b, cuya distribucion tiene forma de V"""
    x = random.random()/2
    y = random.random()/2
    if x + y < 0.5:
        z = x + y + 0.5
    else:
        z = x + y - 0.5
    return (b - a)*z + a

class Tuning_Pro_Agent(IGenetic_SugarScape):

    def __generate_initial_population__(self, population_size: int) -> List[ProAgent]:
        self.iteration = 1
        population : List[ProAgent] = self.get_agents_with_predefined_values()
        for id in range(5, population_size + 1):
            population.append(ProAgent(id, 1, None, conn))
            population[-1].alfa = random.random()
            population[-1].beta = random.random()
            population[-1].appeal_recquired_to_associate = random.random()
            population[-1].minimun_free_portion = random.random()
            population[-1].security_umbral = random.random()
        return population

    def crossover(self, agent_a: ProAgent, agent_b: ProAgent) -> ProAgent:
        """Para mezclar cada uno de los parametros tomamos un punto intermedio entre el valor
        del parametro de los dos padres. Ese punto intermedio es determinado al azar, con mayor
        distribucion cerca de los valores que tienen los padres (o sea una campana de Gauss in
        vertida)"""
        child = ProAgent(self.ids_to_replace[-1], 1, None, conn)
        self.ids_to_replace.pop()
        child.alfa = valley_shaped_distribution_random_number(agent_a.alfa, agent_b.alfa)
        child.appeal_recquired_to_associate = valley_shaped_distribution_random_number(agent_a.appeal_recquired_to_associate, agent_b.appeal_recquired_to_associate)
        child.beta = valley_shaped_distribution_random_number(agent_a.beta, agent_b.beta)
        child.security_umbral = valley_shaped_distribution_random_number(agent_a.security_umbral, agent_b.security_umbral)
        child.minimun_free_portion = valley_shaped_distribution_random_number(agent_a.minimun_free_portion, agent_b.minimun_free_portion)
        return child
    
    def mutate(self, agent: ProAgent) -> ProAgent:
        """Cada parametro tiene una probabilidad de 10 porciento de modificarse"""
        self.first_free_id = 6
        if random.random() < 0.1:
            agent.alfa = random.random()
        if random.random() < 0.1:
            agent.beta = random.random()
        if random.random() < 0.1:
            agent.minimun_free_portion = random.random()
        if random.random() < 0.1:
            agent.security_umbral += (random.random() - 0.5)
        if random.random() < 0.1:
            agent.appeal_recquired_to_associate += (random.random() - 0.5)
        return agent
    
    def duplicate(self, agent : ProAgent) -> ProAgent:
        answer = ProAgent(agent.id, agent.consume, None, conn)
        answer.alfa = agent.alfa
        answer.appeal_recquired_to_associate = agent.appeal_recquired_to_associate
        answer.beta = agent.beta
        answer.minimun_free_portion = agent.minimun_free_portion
        answer.security_umbral = agent.security_umbral
        return answer
    
    def stop_criterium(self, generation: List[ProAgent]) -> bool:
        print(self.fitness(generation[0]))
        print("alfa: " + str(generation[0].alfa))
        print("beta: " + str(generation[0].beta))
        print("apeal_recquired_to_associate: " + str(generation[0].appeal_recquired_to_associate))
        print("minimun_free_portion: " + str(generation[0].minimun_free_portion))
        print("security_umbral: " + str(generation[0].security_umbral))
        self.rankings_calculated = False
        ended = self.iteration > 1000
        self.iteration += 1
        print("Comenzando la iteracion " + str(self.iteration))
        return ended
    
    def get_agents_with_predefined_values(self):
        population = [ProAgent(i, 1, None, conn) for i in range(1, 5)]
        #Nunca ataca, se asocia, prioriza ganancias sin importarle el riesgo
        population[0].alfa = 1
        population[0].beta = 1
        population[0].minimun_free_portion = 0
        population[0].appeal_recquired_to_associate = 0
        population[0].security_umbral = 2

        #Pendejo, se asocia, no ataca
        population[1].alfa = 0
        population[1].beta = 0
        population[1].minimun_free_portion = 1
        population[1].appeal_recquired_to_associate = 0
        population[1].security_umbral = 2

        #Violento, prioriza ganancias, no se asocia
        population[2].alfa = 1
        population[2].beta = 0.5
        population[2].minimun_free_portion = 1
        population[2].appeal_recquired_to_associate = 2
        population[2].security_umbral = 0.3

        #El otro es el predefinido
        return population

a = Tuning_Pro_Agent()
a.simple_run(0.6, 20)