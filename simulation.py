import pybullet as p
import pybullet_data
import pyrosim
import time

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, type):
        
        self.physicsClient = p.connect(p.GUI)
        #self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT(type)

    def run(self):
        for timestep in range(1000):
            p.stepSimulation()
            self.robot.think()
            self.robot.act()
            time.sleep(.001)
        print(self.robot.get_fitness())


    def __del__(self):
        p.disconnect()
