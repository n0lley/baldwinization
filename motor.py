from pyrosim import pyrosim
import pybullet as p
import numpy as np
import math

class MOTOR:

    def __init__(self, jointname):
        
        self.jointname = jointname
        self.prepare_to_act()
        
    def prepare_to_act(self):
        pass
        
    def set_value(self, robot, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robot,
            jointName = self.jointname,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle*math.pi,
            maxForce = 100
            )
                
        
