import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import experiment_parameters as ep

treatment = input("Robot treatment: ")

assert os.path.exists("data/"+treatment), "Treatment file does not exist"
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
for seed in os.listdir("data/"+treatment):
    if seed[0] == run:
        seeds.append(seed)

x_var = {}
y_var = {}
#ALTER OBSERVED DATA HERE AS NECESSARY
robotfile = open("data/"+treatment+"/"+seeds[0]+"/199.p", 'rb')
robot = pickle.load(robotfile)
robotfile.close()

hebb_A = {}
hebb_B = {}
hebb_C = {}
hebb_D = {}
sum_hebb = {}
etas = {}
vars = {}

# for gene in robot.get_hebbian_parameters():
#     hebb_A[str(gene)] = [robot.get_hebbian_parameters()[gene][0]]
#     hebb_B[str(gene)] = [robot.get_hebbian_parameters()[gene][1]]
#     hebb_C[str(gene)] = [robot.get_hebbian_parameters()[gene][2]]
#     hebb_D[str(gene)] = [robot.get_hebbian_parameters()[gene][3]]
#     sum_hebb[str(gene)] = [sum(robot.get_hebbian_parameters()[gene])]
#     etas[str(gene)] = [robot.get_genome()[gene][1]]

for synapse in robot.get_genome():
    converted_synapse = (str(synapse[0]), str(synapse[1]))
    plt.scatter(
        robot.get_genome()[synapse][1]*sum(robot.get_hebbian_parameters()[synapse]),
        np.var(robot.synaptic_activity[converted_synapse]),
    )
    # vars[str(synapse).replace("'", "")] = [np.var(robot.synaptic_activity[synapse])]

for seed in seeds[1:]:
    robotfile = open("data/" + treatment + "/" + seed + "/199.p", 'rb')
    robot = pickle.load(robotfile)
    robotfile.close()
    for synapse in robot.get_genome():
        converted_synapse = (str(synapse[0]), str(synapse[1]))
        plt.scatter(
            robot.get_genome()[synapse][1]*sum(robot.get_hebbian_parameters()[synapse]),
            np.var(robot.synaptic_activity[converted_synapse]),
        )
    # for gene in robot.get_hebbian_parameters():
    #     hebb_A[str(gene)].append(robot.get_hebbian_parameters()[gene][0])
    #     hebb_B[str(gene)].append(robot.get_hebbian_parameters()[gene][1])
    #     hebb_C[str(gene)].append(robot.get_hebbian_parameters()[gene][2])
    #     hebb_D[str(gene)].append(robot.get_hebbian_parameters()[gene][3])
    #     sum_hebb[str(gene)].append(sum(robot.get_hebbian_parameters()[gene]))
    #     etas[str(gene)].append(robot.get_genome()[gene][1])

    # for synapse in robot.synaptic_activity:
        # vars[str(synapse).replace("'", "")].append(np.var(robot.synaptic_activity[synapse]))

# CHANGE AXIS LABELS AND PLOT TITLE AS NECESSARY
plt.xlabel("Synaptic Plasticity")
plt.ylabel("Synaptic Variance")
plt.title("Synaptic Plasticity and Variance in "+type+" Individuals")
plt.show()