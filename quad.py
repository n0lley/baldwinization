import pyrosim
import numpy as np

from robot import ROBOT
import experiment_parameters as ep

class QUAD(ROBOT):
    
    def __init__(self):
        super().__init__()
        self.type = "quad"

    def make_body():
        pyrosim.Start_URDF("quad_body.urdf")
        
        #body and first body-leg joint - root nodes
        pyrosim.Send_Cube(
            name='body0',
            pos=[0, 0, ep.length + ep.radius + ep.offset],
            size = [ep.length*3/4, ep.length*3/4, ep.length*3/4]
            )
            
        pyrosim.Send_Joint(
            name='body0_body1',
            parent='body0',
            child='body1',
            type='revolute',
            position=[ep.length*3/8, 0, ep.length + ep.radius + ep.offset],
            axis=[0,1,0]
            )
            
        #build upper legs and body-leg joints
        invert = 1 #for flipping x and y coordinates to other side of body
        for i in range(1, 5):
            
            pyrosim.Send_Cube(
                name='body%d'%i,
                pos=[(ep.length/2 + ep.radius)*(i%2)*invert,
                     (ep.length/2 + ep.radius)*((i-1)%2)*invert,
                      0],
                size=[ep.length*(i%2) + ep.radius*2,
                      ep.length*((i-1)%2) + ep.radius*2,
                      ep.radius*2]
            )
            
            if i==2: #flip coordinates after second limb is built
                invert*=-1
            
            if i < 4:
                pyrosim.Send_Joint(
                    name='body0_body%d'%(i+1),
                    parent='body0',
                    child='body%d'%(i+1),
                    type='revolute',
                    position=[((i-1)%2)*ep.length*3/8*invert,
                              (i%2)*ep.length*3/8*invert,
                              ep.length + ep.radius + ep.offset],
                    axis=[i%2,(i-1)%2,0]
                )
                
        #build lower legs and knee joints
        invert = 1 #same as last time, for flipping around the body
        for i in range(1, 5):
            pyrosim.Send_Joint(
                name='body%d_body%d'%(i, i+4),
                parent='body%d'%i,
                child='body%d'%(i+4),
                type='revolute',
                position=[(ep.length + ep.radius)*(i%2)*invert,
                          (ep.length + ep.radius)*((i-1)%2)*invert,
                          0],
                axis=[(i-1)%2, i%2, 0]
            )
            pyrosim.Send_Cube(
                name='body%d'%(i+4),
                pos=[0,0,-(ep.length/2 + ep.radius)],
                size=[ep.radius*2, ep.radius*2, ep.length+ep.radius*2]
            )
            if i==2: invert*=-1
        
        
        pyrosim.End()

    
