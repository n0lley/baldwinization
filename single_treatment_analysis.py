import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import experiment_parameters as ep
import scikits.bootstrap as bootstrap

treatment = input("treatment: ")
run = input("robot type to analyse: ")

type = "UNASSIGNED"

if run == '0':
    type = "Snake"
elif run == '1':
    type = "Quadruped"
elif run == '2':
    type = "Hexapod"

runs = []
for d in os.listdir("data/"+treatment):
    if d[0] == run:
        runs.append(d)

variance_means = {}
fitnesses = {}

for i in range(ep.total_gens):
    variance_means[i] = []
    fitnesses[i] = []
    for r in runs:
        f = open("data/"+treatment+"/"+r+"/"+str(i)+".p", 'rb')
        if i == 0:
            fullpop = pickle.load(f)
            fullpop = sorted(fullpop, key=ep.fitness_sort, reverse=True)
            pop = fullpop[0]

        else:
            pop = pickle.load(f)
        f.close()

        fitnesses[i].append(pop.fitness)

        variances = []
        for s in pop.synaptic_activity:
            variances.append(np.var(pop.synaptic_activity[s]))
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
if type == 'Snake':
    body_length = 4*ep.length
elif type == 'Quadruped':
    body_length = 2*ep.length
elif type == "Hexapod":
    body_length = 2*ep.length

for i in range(len(fitnesses)):
    fitness_means.append(np.mean(fitnesses[i])/body_length)
    ci = bootstrap.ci(fitnesses[i])
    fit_lows.append(ci[0]/body_length)
    fit_highs.append(ci[1]/body_length)

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
plt.ylabel("Displacement at t=1000 in Body Lengths")
plt.show()