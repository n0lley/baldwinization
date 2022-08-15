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
for i in populations:
    synapse_values = populations[i][0].synaptic_activity
    synapse_variances.append(numpy.var(synapse_values))

plt.scatter(populations.keys(), synapse_variances)
plt.show()