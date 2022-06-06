import pyrosim

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

    
    
    def make_brain(self, weights, hebb, filetag):
        motorNeurons = []
        sensorNeurons = []
        hiddenNeurons = []
        
        pyrosim.Start_NeuralNetwork("nnfiles/hex_brain"+filetag+".nndf")
        
        for i in range(6): #Touch sensors on leg ends
            sensorNeurons.append(i)
            pyrosim.Send_Touch_Sensor_Neuron(name=i, linkName='body%d'%(i+5))

        for i in range(6, 12): #Proprioceptive sensors on hip joints
            sensorNeurons.append(i)
            pyrosim.Send_Proprioceptive_Sensor_Neuron(name=i, jointName='body0_body%d'%(i-3))
        
        for i in range(12, 18): #Proprioceptive sensors on knee joints
            sensorNeurons.append(i)
            pyrosim.Send_Proprioceptive_Sensor_Neuron(name=i, jointName='body%d_body%d'%(i-7, i-3))
        
        for i in range(18, 36):
            hiddenNeurons.append(i)
            pyrosim.Send_Hidden_Neuron(name=i)
        
        for i in range(36, 42): #Hip joint motors
            motorNeurons.append(i)
            pyrosim.Send_Motor_Neuron(name=i, jointName='body0_body%d'%(i-23))
        
        for i in range(42, 48): #Knee joint motors
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
