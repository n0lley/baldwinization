import pickle
import os
import matplotlib.pyplot as plt
import experiment_parameters as ep
import numpy as np
import scikits.bootstrap as bootstrap

run = input("robot type to analyse: ")
path = "data/"+run

type = "UNASSIGNED"

if run == '0':
    type = "Snake"
elif run == '1':
    type = "Quadruped"
elif run == '2':
    type = "Hexapod"

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

mean_var_means = []
var_lows = []
var_highs = []
for i in range(len(variance_means)):
    mean_var_means.append(np.mean(variance_means[i]))
    ci = bootstrap.ci(variance_means[i])
    var_lows.append(ci[0])
    var_highs.append(ci[1])

fitness_means = []
fit_lows = []
fit_highs = []
body_length = 0
if type == 'snake':
    body_length = 4
elif type == 'quad':
    body_length = 2
elif type == "hex":
    body_length = 2

for i in range(len(fitnesses)):
    fitness_means.append(np.mean(fitnesses[i]))
    ci = bootstrap.ci(fitnesses[i])
    fit_lows.append(ci[0])
    fit_highs.append(ci[1])

plt.title(type+" mean synaptic variance")
plt.plot(mean_var_means)
plt.fill_between(range(ep.total_gens), var_lows, var_highs, alpha=.3)
plt.xlabel("Generation")
plt.ylabel("Highest-Fitness Robot's Average Synaptic Variance")
plt.show()

plt.title(type+" mean fitness")
plt.plot(range(ep.total_gens), fitness_means)
plt.fill_between(range(ep.total_gens), fit_lows, fit_highs, alpha = .3)
plt.xlabel("Generation")
plt.ylabel("Displacement at t=1000")
plt.show()
