#SIMULATION METAPARAMETERS
import math

sim_time = 1000
dt = .001
gravity = -9.8

#ROBOT PHYSICAL PARAMETERS
length = .5
radius = length/10
offset = radius/10

joint_range = .3

permitted_robot_types = ["snake", "quad", "hex"]

#NETWORK PARAMETERS

hebbian_alpha = .2
hebbian_sigma = .1

#EVOLUTION PARAMETERS
mutation_prob = .05
total_gens = 200
pop_size = 30
num_children = 30
tournament_size = 3
tournament_winners = 1

#HELPER FUNCTIONS
def fitness_sort(i):
    return i.fitness
