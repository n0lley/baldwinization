import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import experiment_parameters as ep

type = input("Robot type: ")
if type == "Snake":
    run = '0'
elif type == "Quadruped":
    run = '1'
elif type == "Hexapod":
    run = '2'
else:
    print("type does not exist")
    exit(0)

seeds = []
for seed in os.listdir("data/10% Mutation/"):
    if seed[0] == run:
        seeds.append(seed)

zeros = {}
ones = {}
y_var = {}
#ALTER OBSERVED DATA HERE AS NECESSARY
for gen in range(200):
    zeros[gen] = []
    ones[gen] = []
    for seed in seeds:
        robotfile = open("data/10% Mutation/"+seed+"/"+str(gen)+".p", 'rb')
        robots = pickle.load(robotfile)
        if gen == 0:
            robot = sorted(robots, key=ep.fitness_sort(), reverse=True)[0]
        else:
            robot = robots
        robotfile.close()

        zero_etas = 0
        one_etas = 0

        for synapse in robot.get_genome():
            if robot.get_genome()[synapse][1] == 0:
                zero_etas += 1
            elif robot.get_genome()[synapse][1] == 1:
                one_etas += 1



# CHANGE AXIS LABELS AND PLOT TITLE AS NECESSARY
plt.xlabel("Synaptic Plasticity")
plt.ylabel("Synaptic Variance")
plt.title("Synaptic Plasticity and Variance in "+type+" Individuals")
plt.show()