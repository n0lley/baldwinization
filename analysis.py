import pickle
import os
import matplotlib.pyplot as plt
import numpy

run = input("run to analyse: ")
assert run in os.listdir("./data/"), "Run " + run + " not found."
path = "data/"+run

populations = {}
for i in range(len(os.listdir(path))):
    gen = str(i)+".p"
    f = open(path+"/"+gen, "rb")
    populations[i] = pickle.load(f)
    f.close()

synapse_variances = []
keys_to_variances = {}
for i in populations:
    synapse_values = populations[i][0].synaptic_activity
    for key in synapse_values:
        if key not in keys_to_variances.keys():
            keys_to_variances[key] = [numpy.var(synapse_values[key])]
        else:
            keys_to_variances[key].append(numpy.var(synapse_values[key]))

for key in keys_to_variances.keys():
    plt.scatter(populations.keys(), keys_to_variances[key], label=key)
plt.legend()
plt.show()

fitnesses = []
for i in populations:
    fitnesses.append(populations[i][0].fitness)

plt.plot(populations.keys(), fitnesses)
plt.show()
