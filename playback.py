import pickle
import sys

def fitness_sort(i):
    return i.fitness

seed = sys.argv[1]
gen = sys.argv[2]

f = open("data/"+seed+"/"+gen+".p", "rb")

if gen == '0':
    pop = pickle.load(f)
    pop = sorted(pop, key=fitness_sort, reverse=True)
    bestIndividual = pop[0]
else:
    bestIndividual = pickle.load(f)
f.close()
bestIndividual.start_simulation("playback", "0")