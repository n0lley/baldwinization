import sys
import time

from simulation import SIMULATION

t0 = time.time()
simulation = SIMULATION(sys.argv[1], sys.argv[2], sys.argv[3])
simulation.run(int(sys.argv[2]), sys.argv[3], sys.argv[4])
f = open(seed + "_individual_simtime.txt", "a")
f.write(str(time.time() - t0) + "\n")
f.close()
