import pickle
import os
import matplotlib.pyplot as plt
import experiment_parameters as ep
import numpy as np

run = input("robot type to analyse: ")
path = "data/"+run

runs = []
for d in os.listdir("data"):
    if d[0] == run:
        runs.append(d)

variance_means = {}
fitnesses = {}
for i in range(ep.total_gens):
    variance_means[i] = []
    fitnesses[i] = []
    for r in runs:
        f = open("data/"+r+"/"+str(i)+".p", 'rb')
        pop = pickle.load(f)
        f.close()

        fitnesses[i].append(pop[0].fitness)

        variances = []
        for s in pop[0].synaptic_activity:
            variances.append(np.var(pop[0].synaptic_activity[s]))
        variance_means[i].append(np.mean(variances))

fitness_means = [np.mean(fitnesses[i]) for i in range(ep.total_gens)]
mean_variance_means = [np.mean(variance_means[i]) for i in range(ep.total_gens)]

lows = [min(variance_means[i]) for i in range(ep.total_gens)]
highs = [max(variance_means[i]) for i in range(ep.total_gens)]
plt.title(run+" mean synaptic variance")
plt.plot(mean_variance_means)
plt.fill_between(range(ep.total_gens), lows, highs, alpha=.3)
plt.show()

plt.title(run+" mean fitness")
plt.plot(range(ep.total_gens), fitness_means)
plt.show()
