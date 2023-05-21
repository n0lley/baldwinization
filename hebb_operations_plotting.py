import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import experiment_parameters as ep
import scikits.bootstrap as bootstrap

population = pickle.load(open("data/10% Mutation/summary/"+'2199.p', 'rb'))

for i in population:
    hebb_sums = {}

    for synapse in i.get_hebbian_parameters():
        hebb_sums[synapse] = []
        for t in range(1000):
            aij, bij, cij, dij = i.get_hebbian_parameters()[synapse]
            oi = i.neuron_activity[str(synapse[0])][t]
            oj = i.neuron_activity[str(synapse[1])][t]
            hebb_sums[synapse].append(np.abs(aij * oi * oj + bij * oi + cij * oj + dij))

    for synapse in hebb_sums:
        avg_hebb = np.mean(hebb_sums[synapse])
        synaptic_variance = np.var(i.synaptic_activity[(str(synapse[0]), str(synapse[1]))])
        eta = i.genome[synapse][1]
        plt.scatter(avg_hebb, synaptic_variance, c=[[.4, .2, .5]])

plt.ylim(-.2, 1)
plt.title("Individual Synaptic Variance and Hebbian Operations of 50 Individuals")
plt.xlabel("Average Magnitude of Hebbian Operation over 1000 Timesteps")
plt.ylabel("Synaptic Variance over 1000 Timesteps")
plt.show()