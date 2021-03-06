#SIMULATION METAPARAMETERS
import math

sim_time = 1000
dt = .001
gravity = -9.8

monitor_percent = .1

#ROBOT PHYSICAL PARAMETERS
length = .5
radius = length/10
offset = radius/10

#NETWORK PARAMETERS

hebbian_alpha = .2
hebbian_sigma = .1

#EVOLUTION PARAMETERS
mutation_prob = .1
total_gens = 100
pop_size = 5
num_children = 50
tournament_size = 10
tournament_winners = 3

#HELPER FUNCTIONS
def fitness_sort(i):
    return i.fitness
