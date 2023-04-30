import pickle
import os
import sys

def fitness_sort(i):
    return i.fitness

def full_sim(type, generation):
    paths = []
    for seed in os.listdir("data/10% Mutation/"):
        if seed.startswith(type):
            paths.append("data/10% Mutation/"+seed+"/"+generation+".p")

    group_to_sim = []

    for path in paths:
        print(path)
        f = open(path, 'rb')

        if generation == '0':
            pop = pickle.load(f)
            pop = sorted(pop, key=fitness_sort, reverse=True)
            group_to_sim.append(pop[0])
        else:
            individual = pickle.load(f)
            group_to_sim.append(individual)
        f.close()

        group_to_sim[-1].start_simulation("playback")
        group_to_sim[-1].wait_to_finish("playback")

    f = open("playback/data/"+type+generation+".p",'wb')
    pickle.dump(group_to_sim, f)
    f.close()

def one_sim(seed, gen):

    f = open("data/10% Mutation/"+seed+"/"+gen+".p", "rb")

    if gen == '0':
        pop = pickle.load(f)
        pop = sorted(pop, key=fitness_sort, reverse=True)
        bestIndividual = pop[0]
    else:
        bestIndividual = pickle.load(f)
    f.close()

    print(bestIndividual.fitness)
    bestIndividual.start_simulation("playback", play_blind=0)
    bestIndividual.wait_to_finish("playback")

full_sim(sys.argv[1], sys.argv[2])