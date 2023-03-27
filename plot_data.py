import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import experiment_parameters as ep

treatment = input("Robot treatment: ")
assert os.path.exists("data/"+treatment), "Treatment file does not exist"
single = input("Whole-type analysis? (y/n): ")
if single == "y": single = False
else: single = True

if single:
    seed = input("Robot seed: ")
    robotfile = open("data/"+treatment+"/"+seed+"/199.p", 'rb')
    robot = pickle.load(robotfile)
    robotfile.close()

    #ALTER OBSERVED VARIABLES HERE AS NECESSARY
    x_var = {}
    y_var = {}

    for synapseName in robot.get_hebbian_parameters():
        x_var[str(synapseName)] = [np.sum(robot.get_hebbian_parameters()[synapseName])]
    for synapseName in robot.synaptic_activity:
        y_var[str(synapseName).replace("'", "")] = [np.var(robot.synaptic_activity[synapseName])]

    for key in x_var:
        plt.scatter(x_var[key], y_var[key])
    #CHANGE AXIS LABELS AND PLOT TITLE AS NECESSARY
    plt.xlabel("Sum of Attached Hebbian Coefficients")
    plt.ylabel("Average Variance Over 1000 Timesteps")
    plt.title("Synaptic Variance and Learning Rules of Robot Seed "+seed)
    plt.show()

else:
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

    for synapseName in robot.get_hebbian_parameters():
        x_var[str(synapseName)] = [np.sum(robot.get_hebbian_parameters()[synapseName])]
    for synapseName in robot.synaptic_activity:
        y_var[str(synapseName).replace("'", "")] = [np.var(robot.synaptic_activity[synapseName])]

    for seed in seeds[1:]:
        robotfile = open("data/"+treatment+"/"+seed+"/199.p", 'rb')
        robot = pickle.load(robotfile)
        robotfile.close()

        for synapseName in robot.get_genome():
            x_var[str(synapseName)].append(np.sum(robot.get_hebbian_parameters()[synapseName]))
        for synapseName in robot.synaptic_activity:
            y_var[str(synapseName).replace("'", "")].append(np.var(robot.synaptic_activity[synapseName]))

    keys = x_var.keys()
    for key in keys:
        for i in range(len(x_var[key])):
            plt.scatter(x_var[key][i], y_var[key][i], color='blue')

    plt.scatter([np.mean(x_var[key]) for key in keys], [np.mean(y_var[key]) for key in keys], color='red')
    # CHANGE AXIS LABELS AND PLOT TITLE AS NECESSARY
    plt.xlabel("Sum of Attached Hebbian Coefficients")
    plt.ylabel("Average Variance Over 1000 Timesteps")
    plt.title("Synaptic Variance and Learning Rules of Highest-Fitness "+type+" Individuals")
    plt.show()