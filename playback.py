import pickle
import matplotlib.pyplot as plt
import sys

def fitness_sort(i):
    return i.fitness

treatment = sys.argv[1]
seed = sys.argv[2]
gen = sys.argv[3]

f = open("data/"+treatment+"/"+seed+"/"+gen+".p", "rb")

if gen == '0':
    pop = pickle.load(f)
    pop = sorted(pop, key=fitness_sort, reverse=True)
    bestIndividual = pop[0]
else:
    bestIndividual = pickle.load(f)
f.close()

print(bestIndividual.fitness)
bestIndividual.start_simulation("playback")
bestIndividual.wait_to_finish("playback")

plt.show()