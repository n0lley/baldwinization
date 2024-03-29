from pyrosim import pyrosim

from builder import BUILDER
import experiment_parameters as ep
        
class HEX(BUILDER):

    def __init__(self):
        super().__init__()
        self.type = "hex"

    def make_body(self):
        pyrosim.Start_URDF("bodyfiles/hex_body.urdf")
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

    
    
    def make_brain(self, weights, hebb, filetag, seed):
        motorNeurons = []
        sensorNeurons = []
        hiddenNeurons = []
        
        pyrosim.Start_NeuralNetwork(seed+"/hex_brain"+filetag+".nndf")
        
        for i in range(6): #Hip Proprioceptive
            sensorNeurons.append(i)
            pyrosim.Send_Proprioceptive_Sensor_Neuron(name=i, jointName='body0_body%d'%(i+1))

        for i in range(6, 12): #Knee Proprioceptive
            sensorNeurons.append(i)
            pyrosim.Send_Proprioceptive_Sensor_Neuron(name=i, jointName='body%d_body%d'%(i-5, i+1))
        
        for i in range(12, 18): #Feet Touch Sensors
            sensorNeurons.append(i)
            pyrosim.Send_Touch_Sensor_Neuron(name=i, linkName='body%d'%(i-5))
        
        for i in range(18, 36):
            hiddenNeurons.append(i)
            pyrosim.Send_Hidden_Neuron(name=i)
        
        for i in range(36, 42): #Hip joint motors
            motorNeurons.append(i)
            pyrosim.Send_Motor_Neuron(name=i, jointName='body0_body%d'%(i-35))
        
        for i in range(42, 48): #Knee joint motors
            motorNeurons.append(i)
            pyrosim.Send_Motor_Neuron(name=i, jointName='body%d_body%d'%(i-41, i-35))

        for s in sensorNeurons:
            for h in hiddenNeurons:
                w = weights[(s, h)][0]
                learning_rule = [weights[(s, h)][1]] #grab synapse learning rate
                learning_rule.extend(hebb[(s, h)]) #bundle with hebb rules
                pyrosim.Send_Synapse(sourceNeuronName=s, targetNeuronName=h, weight=w, learningRule=learning_rule)

        for h in hiddenNeurons:
            for m in motorNeurons:
                w = weights[(h, m)][0]
                learning_rule = [weights[(h, m)][1]] #grab synapse learning rate
                learning_rule.extend(hebb[(h, m)]) #bundle with hebb rules
                pyrosim.Send_Synapse(sourceNeuronName=h, targetNeuronName=m, weight=w, learningRule=learning_rule)
        
        pyrosim.End()
