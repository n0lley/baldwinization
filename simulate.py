import sys

from simulation import SIMULATION

simulation = SIMULATION(sys.argv[1], sys.argv[2])
simulation.run(int(sys.argv[2]), sys.argv[3])
