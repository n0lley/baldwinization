import os
import copy
import numpy as np
import sys
import pickle
import time

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

        for i in range(4): #add the corresponding noise to all parameters, round decimal place.
            child_set[synapse_name][i] += parameter_noise[synapse_name][i] * ep.hebbian_sigma
            child_set[synapse_name][i] = round(child_set[synapse_name][i], 6)

    return child_set

def step_hebbian(population, current_hebb):
    """
    Perform weighted sum of population's hebbian parameters to determine the new weights
    Returns a dictionary of hebbian parameters corresponding to each synaptic connection
    """
    #Extract fitness scores and hebbian parameters from each controller in the population
    hebbs_to_add = []
    next_hebb = {}
    for p in population:
        hebbs_to_add.append({"fitness":p.get_fitness(), "params":p.get_hebbian_parameters()})

    for key in hebbs_to_add[0]["params"].keys(): #for each synapse, create a sum of all parameter noise

        sums = [0]*4 #accumulator
        for hebb in hebbs_to_add:
            noise = [current_hebb[key][i] - hebb["params"][key][i] for i in range(4)]
            weighted_noise = [n * hebb["fitness"] for n in noise] #weight noise by the fitness it produced
            sums = np.add(sums, weighted_noise) #add weighted noises to total

        #calculate weighted average noise, apply learning rate modifiers
        sums *= ep.hebbian_alpha
        sums /= (ep.hebbian_sigma * len(population))
        next_hebb[key] = np.add(current_hebb[key], sums)

    return next_hebb

##########  POPULATION-LEVEL METHODS  ###################
        
def select(population):
    population = sorted(population, key=ep.fitness_sort, reverse=True)
    new_pop = [population[0]]
    
    while len(new_pop) < ep.pop_size:
        tournament = np.random.choice(population, size = ep.tournament_size)
        winners = sorted(tournament, key=ep.fitness_sort, reverse=True)[:ep.tournament_winners]
        new_pop.extend(winners)
    
    return new_pop[:ep.pop_size]
        

########################################################
seed = sys.argv[2] #establish random seed
np.random.seed(int(seed))

#clear any old files
os.system("rm nnfiles/*")
os.system("rm "+seed+"/*")
os.system("mkdir "+seed)

#generate initial robot and variables
population = []
robot_type = sys.argv[1]
assert robot_type.lower() in ep.permitted_robot_types, "Robot type not recognized."

population.append(CONTROLLER(robot_type, 0))

parent_hebb = population[0].get_hebbian_parameters()
id_iterator = 1

#generate the rest of the population, base their hebbian parameters on the parent set
t0 = time.time()
for i in range(1, ep.pop_size):
    new_hebb = create_new_hebbian_parameters(parent_hebb)
    population.append(CONTROLLER(robot_type, id_iterator, input_parameters=new_hebb))
    id_iterator += 1

#evaluate all these robots
for p in population:
    p.start_simulation(seed, play_blind=1)

for p in population:
    p.wait_to_finish(seed)

#gradient the hebbian
parent_hebb = step_hebbian(population, parent_hebb)

os.system("mkdir data/"+sys.argv[2])
f = open("data/"+sys.argv[2]+"/0.p", "wb")
pickle.dump(population, f)
f.close()

print_string = "generation 0 fitness " + str(round(population[0].get_fitness(), 3)) + " in " + str(int(time.time() - t0)) + " seconds"
os.system("echo " + print_string)

#do that again a bunch of times
for i in range(1, ep.total_gens):
    t0 = time.time()
    #reproduce
    children = []
    while len(children) < ep.num_children:
        #clone a parent, set a new ID
        parent = np.random.choice(population)
        child = copy.deepcopy(parent)
        child.set_ID(id_iterator)
        id_iterator += 1

        child.mutate() #mutate genome

        #generate a new set of hebbian parameters from the parent set
        new_hebb = create_new_hebbian_parameters(parent_hebb)
        child.set_hebbian_parameters(new_hebb)

        children.append(child)

    #test the children
    for c in children:
        c.start_simulation(seed, play_blind=1)
    for c in children:
        c.wait_to_finish(seed)

    population.extend(children)  #combine populations
    population = select(population) #cull extras

    parent_hebb = step_hebbian(population, parent_hebb) #step hebbian

    print_string = "generation " + str(i) + " fitness " + str(round(population[0].get_fitness(), 3)) + " in " + str(int(time.time() - t0)) + " seconds"
    os.system("echo "+print_string)

    f = open("data/"+sys.argv[2]+"/"+str(i)+".p", "wb")
    pickle.dump(population, f)
    f.close()

os.system("rmdir "+seed)
