import pybullet as p
import pybullet_data
import time

from world import WORLD
from robot import ROBOT
import experiment_parameters as ep

class SIMULATION:
    def __init__(self, type, play_blind, id_tag, seed):
        play_blind = int(play_blind)
        if play_blind:
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, ep.gravity)
        self.world = WORLD()
        self.robot = ROBOT(type, seed, id_tag)

    def run(self, play_blind, id_tag, seed):
        for timestep in range(ep.sim_time):
            p.stepSimulation()
            self.robot.think()
            self.robot.act()
            if not play_blind: time.sleep(ep.dt)
        self.robot.get_fitness(id_tag, seed)


    def __del__(self):
        p.disconnect()
