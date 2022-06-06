import os
import copy
import numpy as np

import experiment_parameters as ep
from controller import CONTROLLER

##########  HEBBIAN ALGORITHM MANAGEMENT   ##############

def create_new_hebbian_parameters(parent_set):
    """
    From the parent hebbian parameter set, create a child parameter set, deviated by random noise.
    Return the child parameter set.
    """
    child_set = copy.deepcopy(parent_set)
    parameter_noise = {} #initialize noise set

    for synapse_name in child_set.keys(): #for each synapse we have params for, generate noise
        parameter_noise[synapse_name] = [np.random.normal(0, 1) for p in child_set[synapse_name]]

        for i in range(5): #add the corresponding noise to all parameters, round decimal place.
            child_set[synapse_name][i] += parameter_noise[synapse_name][i] * ep.hebbian_sigma
            child_set[synapse_name][i] = round(child_set[synapse_name][i], 6)

    return child_set, parameter_noise

def step_hebbian(population, current_hebb):
    """
    Perform weighted sum of population's hebbian parameters to determine the new weights
    Returns a dictionary of hebbian parameters corresponding to each synaptic connection
    """
    #Extract fitness scores and hebbian parameters from each controller in the population
    hebbs_to_add = []
    next_hebb = {}
    for p in population:
        hebbs_to_add.append({"fitness":p.get_fitness(), "params":p.get_hebbian_parameters(), "noise":p.get_hebbian_noise()})

    for key in hebbs_to_add[0]["params"].keys(): #for each synapse, create a sum of all parameter noise

        sums = [0]*5 #accumulator
        for hebb in hebbs_to_add:
            noise = hebb["noise"][key]
            weighted_noise = [n * hebb["fitness"] for n in noise] #weight noise by the fitness it produced
            sums = np.add(sums, weighted_noise) #add weighted noises to total

        #calculate weighted average noise, apply learning rate modifiers
        sums *= ep.hebbian_alpha
        sums /= (ep.hebbian_sigma * len(population))
        next_hebb[key] = np.add(current_hebb[key], sums)

    return next_hebb

##########  POPULATION-LEVEL METHODS  ###################

def expand_population(population):
    while len(population) < ep.pop_size + ep.num_children:
        child = copy.deepcopy(np.random.choice(population[:ep.pop_size]))
        child.mutate()
        child.evaluate()
        population.append(child)
        
def select(population):
    population = sorted(population, key=ep.fitness_sort, reverse=True)
    new_pop = [population[0]]
    
    while len(new_pop) < ep.pop_size:
        tournament = np.random.choice(population, size = ep.tournament_size)
        winners = sorted(tournament, key=ep.fitness_sort, reverse=True)[:ep.tournament_winners]
        new_pop.extend(winners)
    
    population = new_pop[:ep.pop_size]
        

########################################################

#generate initial robot and variables
population = []
robot_type = "snake"

population.append(CONTROLLER(robot_type, 0))

parent_hebb = population[0].get_hebbian_parameters()
id_iterator = 1

#generate the rest of the population, base their hebbian parameters on the parent set
for i in range(1, ep.pop_size):
    new_hebb, hebb_noise = create_new_hebbian_parameters(parent_hebb)
    population.append(CONTROLLER(robot_type, id_iterator, input_parameters=[new_hebb, hebb_noise]))
    id_iterator += 1

print(population)
#evaluate all these robots
for p in population:
    p.evaluate()

#gradient the hebbian
parent_hebb = step_hebbian(population, parent_hebb)