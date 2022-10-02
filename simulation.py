import pybullet as p
import pybullet_data

from world import WORLD
from robot import ROBOT
import time
import experiment_parameters as ep

class SIMULATION:
    def __init__(self, type, play_blind, id_tag):
        play_blind = int(play_blind)
        if play_blind:
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, ep.gravity)
        self.world = WORLD()
        self.robot = ROBOT(type, id_tag)

    def run(self, play_blind, id_tag, seed):
        f = open("timedata/timesteptimes.txt", 'a')
        for timestep in range(ep.sim_time):
            t0 = time.time()
            p.stepSimulation()
            simstep = time.time() - t0
            t0 = time.time()
            self.robot.think()
            robotthink = time.time() - t0
            t0 = time.time()
            self.robot.act()
            robotact = time.time() - t0
            f.write(str(simstep) + "\t" + str(robotthink) + "\t" + str(robotact) + "\n")
            if not play_blind: time.sleep(ep.dt)
        f.close()
        self.robot.get_fitness(id_tag, seed)

    def __del__(self):
        p.disconnect()
