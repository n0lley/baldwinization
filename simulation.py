import pybullet as p
import pybullet_data
import time

from world import WORLD
from robot import ROBOT
import experiment_parameters as ep

class SIMULATION:
    def __init__(self, type, play_blind, id_tag, seed):
        t0 = time.time()
        play_blind = int(play_blind)
        if play_blind:
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, ep.gravity)
        self.world = WORLD()
        self.robot = ROBOT(type, id_tag)
        f = open(seed+"_simulation_init.txt", "a")
        f.write(str(time.time() - t0)+"\n")
        f.close()

    def run(self, play_blind, id_tag, seed):
        for timestep in range(ep.sim_time):
            t0 = time.time()
            p.stepSimulation()
            f = open(seed + "_simulation_step.txt", "a")
            f.write(str(time.time() - t0) + "\n")
            f.close()
            t0 = time.time()
            self.robot.think()
            f = open(seed + "_robot_think.txt", "a")
            f.write(str(time.time() - t0) + "\n")
            f.close()
            t0 = time.time()
            self.robot.act()
            f = open(seed + "_robot_act.txt", "a")
            f.write(str(time.time() - t0) + "\n")
            f.close()
            if not play_blind: time.sleep(ep.dt)
        self.robot.get_fitness(id_tag, seed)


    def __del__(self):
        p.disconnect()
