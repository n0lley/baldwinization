import pyrosim
import numpy as np

from builder import BUILDER
import experiment_parameters as ep

class QUAD(BUILDER):
    
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

    
    def make_brain(self, weights, hebb):
        motorNeurons = []
        sensorNeurons = []
        hiddenNeurons = []
        
        pyrosim.Start_NeuralNetwork("quad_brain.nndf")
        
        for i in range(4): #Touch sensors on leg ends
            sensorNeurons.append(i)
            pyrosim.Send_Touch_Sensor_Neuron(name=i, linkName='body%d'%(i+5))

        for i in range(4, 8): #Proprioceptive sensors on hip joints
            sensorNeurons.append(i)
            pyrosim.Send_Proprioceptive_Sensor_Neuron(name=i, jointName='body0_body%d'%(i-3))
        
        for i in range(8, 12): #Proprioceptive sensors on knee joints
            sensorNeurons.append(i)
            pyrosim.Send_Proprioceptive_Sensor_Neuron(name=i, jointName='body%d_body%d'%(i-7, i-3))
        
        for i in range(12, 24):
            hiddenNeurons.append(i)
            pyrosim.Send_Hidden_Neuron(name=i)
        
        for i in range(24, 28): #Hip joint motors
            motorNeurons.append(i)
            pyrosim.Send_Motor_Neuron(name=i, jointName='body0_body%d'%(i-23))
        
        for i in range(28, 32): #Knee joint motors
            motorNeurons.append(i)
            pyrosim.Send_Motor_Neuron(name=i, jointName='body%d_body%d'%(i-27, i-23))
       
        for s in sensorNeurons:
            for h in hiddenNeurons:
                w = weights[(s, h)]
                pyrosim.Send_Synapse(sourceNeuronName=s, targetNeuronName=h, weight=w, learningRule=hebb[(s, h)])

        for h in hiddenNeurons:
            for m in motorNeurons:
                w = weights[(s, h)]
                pyrosim.Send_Synapse(sourceNeuronName=h, targetNeuronName=m, weight=w, learningRule=hebb[(s, h)])
        
        pyrosim.End()
