import pyrosim
import numpy as np

from robot import ROBOT
import experiment_parameters as ep
        
class HEX(ROBOT):

    def __init__(self):
        super().__init__()
        self.type = "hex"

    def make_body(self):
        pyrosim.Start_URDF("hex_body.urdf")
        #central body mass
        pyrosim.Send_Cube(
            name='body0',
            pos=[0,0, ep.length + ep.radius + ep.offset],
            size=[ep.length*2 + ep.radius*2, ep.radius*2, ep.radius*2]
        )

        #upper limbs + joints
        invert = 1 #for flipping to other side of robot
        for i in range(1, 7):
            pyrosim.Send_Joint(
                name='body0_body%d'%i,
                parent='body0',
                child='body%d'%i,
                type='revolute',
                position=[ep.length - ep.length*((i-1)//2),
                          invert*ep.radius,
                          ep.length+ep.radius+ep.offset],
                axis=[0, 0, 1]
            )
        
            pyrosim.Send_Cube(
                name='body%d'%i,
                pos=[0, invert*(ep.length/2 + ep.radius), 0],
                size=[ep.radius*2, ep.length + ep.radius*2, ep.radius*2]
            )
            invert *= -1
        
        #lower limbs + joints
        invert = 1
        for i in range(1, 7):
            pyrosim.Send_Joint(
                name='body%d_body%d'%(i, i+6),
                parent='body%d'%i,
                child='body%d'%(i+6),
                type='revolute',
                position=[0,
                          invert*(ep.length + ep.radius),
                          0],
                axis=[1, 0, 0]
            )
            
            pyrosim.Send_Cube(
                name='body%d'%(i+6),
                pos=[0, 0, -(ep.length/2 + ep.radius)],
                size=[ep.radius*2, ep.radius*2, ep.length + ep.radius*2]
            )
            invert *= -1
            
        pyrosim.End()

    
