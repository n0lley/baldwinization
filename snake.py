import pyrosim

from builder import BUILDER
import experiment_parameters as ep

class SNAKE(BUILDER):
    
    def __init__(self):
        super().__init__()
        self.type = "snake"
        
    def make_body(self):
        
        pyrosim.Start_URDF("bodyfiles/snake_body.urdf")

        pyrosim.Send_Cube(
            name='body0',
            pos=[0,0,ep.radius+ep.offset],
            size=[ep.length + ep.radius*2, ep.radius*2, ep.radius*2]
        )

        pyrosim.Send_Joint(
            name='body0_body1',
            parent='body0',
            child='body1',
            type='revolute',
            position=[ep.length/2 + ep.radius, 0, ep.radius/2],
            axis=[0,1,0]
        )

        for i in range(1, 4):
                    
            pyrosim.Send_Cube(
                name='body%d'%i,
                pos=[ep.length/2 + ep.radius,0,ep.radius/2],
                size=[ep.length + ep.radius*2, ep.radius*2, ep.radius*2]
                )
                
            if i < 3:
                pyrosim.Send_Joint(
                    name='body%d_body%d'%(i, i+1),
                    parent='body%d'%(i),
                    child='body%d'%(i+1),
                    type='revolute',
                    position=[ep.length + ep.radius*2, 0, 0],
                    axis=[0,(i-1)%2,i%2]
                    )
            
        pyrosim.End()

    def make_brain(self, weights, hebb, filetag):
        motorNeurons = []
        sensorNeurons = []
        hiddenNeurons = []
        
        pyrosim.Start_NeuralNetwork("nnfiles/snake_brain"+filetag+".nndf")
        pyrosim.Send_Touch_Sensor_Neuron(name=0, linkName='body0')
        sensorNeurons.append(0)
        
        for i in range(1, 4):
            sensorNeurons.append(i)
            pyrosim.Send_Proprioceptive_Sensor_Neuron(name=i, jointName='body%d_body%d'%(i-1, i))

        for i in range(4, 8):
            hiddenNeurons.append(i)
            pyrosim.Send_Hidden_Neuron(name=i)

        for i in range(8, 11):
            motorNeurons.append(i)
            pyrosim.Send_Motor_Neuron(name=i, jointName='body%d_body%d'%(i-8, i-7))

        for s in sensorNeurons:
            for h in hiddenNeurons:
                w = weights[(s, h)][0]
                learning_rule = [weights[(s, h)][1]] #grab synapse learning rate
                learning_rule.extend(hebb[(s, h)]) #bundle with hebb rules
                pyrosim.Send_Synapse(sourceNeuronName=s, targetNeuronName=h, weight=w, learningRule=learning_rule)

        for h in hiddenNeurons:
            for m in motorNeurons:
                w = weights[(s, h)][0]
                learning_rule = [weights[(s, h)][1]] #grab synapse learning rate
                learning_rule.extend(hebb[(s, h)]) #bundle with hebb rules
                pyrosim.Send_Synapse(sourceNeuronName=h, targetNeuronName=m, weight=w, learningRule=learning_rule)
        
        pyrosim.End()
