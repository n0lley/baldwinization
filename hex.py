from pyrosim import pyrosim

from builder import BUILDER
import experiment_parameters as ep
        
class HEX(BUILDER):

    def __init__(self):
        super().__init__()
        self.type = "hex"

    def manual_make_body(self):
        #de-looping the body build process to see if that removes the weird bilaterally parallel movement
        #it didn't
        pyrosim.Start_URDF("bodyfiles/hex_body.urdf")
        # central body mass
        pyrosim.Send_Cube(
            name='body0',
            pos=[0, 0, ep.length + ep.radius + ep.offset],
            size=[ep.length * 2 + ep.radius * 2, ep.radius * 2, ep.radius * 2]
        )

        #upper leg segments
        pyrosim.Send_Joint(
            name='body0_body1',
            parent='body0',
            child='body1',
            type='revolute',
            position=[ep.length,
                      ep.radius,
                      ep.length + ep.radius + ep.offset],
            axis=[0, 0, 1]
        )
        pyrosim.Send_Cube(
            name='body1',
            pos=[0, ep.length / 2 + ep.radius, 0],
            size=[ep.radius * 2, ep.length + ep.radius * 2, ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body0_body2',
            parent='body0',
            child='body2',
            type='revolute',
            position=[ep.length,
                      -1 * ep.radius,
                      ep.length + ep.radius + ep.offset],
            axis=[0, 0, 1]
        )
        pyrosim.Send_Cube(
            name='body2',
            pos=[0, -1 * (ep.length / 2 + ep.radius), 0],
            size=[ep.radius * 2, ep.length + ep.radius * 2, ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body0_body3',
            parent='body0',
            child='body3',
            type='revolute',
            position=[0,
                      ep.radius,
                      ep.length + ep.radius + ep.offset],
            axis=[0, 0, 1]
        )
        pyrosim.Send_Cube(
            name='body3',
            pos=[0, (ep.length / 2 + ep.radius), 0],
            size=[ep.radius * 2, ep.length + ep.radius * 2, ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body0_body4',
            parent='body0',
            child='body4',
            type='revolute',
            position=[0,
                      -1 * ep.radius,
                      ep.length + ep.radius + ep.offset],
            axis=[0, 0, 1]
        )
        pyrosim.Send_Cube(
            name='body4',
            pos=[0, -1 * (ep.length / 2 + ep.radius), 0],
            size=[ep.radius * 2, ep.length + ep.radius * 2, ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body0_body5',
            parent='body0',
            child='body5',
            type='revolute',
            position=[-1 * ep.length,
                      ep.radius,
                      ep.length + ep.radius + ep.offset],
            axis=[0, 0, 1]
        )
        pyrosim.Send_Cube(
            name='body5',
            pos=[0, (ep.length / 2 + ep.radius), 0],
            size=[ep.radius * 2, ep.length + ep.radius * 2, ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body0_body6',
            parent='body0',
            child='body6',
            type='revolute',
            position=[-1 * ep.length,
                      -1 * ep.radius,
                      ep.length + ep.radius + ep.offset],
            axis=[0, 0, 1]
        )
        pyrosim.Send_Cube(
            name='body6',
            pos=[0, -1 * (ep.length / 2 + ep.radius), 0],
            size=[ep.radius * 2, ep.length + ep.radius * 2, ep.radius * 2]
        )

        # lower limbs + joints
        pyrosim.Send_Joint(
            name='body1_body7',
            parent='body1',
            child='body7',
            type='revolute',
            position=[0,
                      (ep.length + ep.radius),
                      0],
            axis=[1, 0, 0]
        )
        pyrosim.Send_Cube(
            name='body7',
            pos=[0, 0, -(ep.length / 2 + ep.radius)],
            size=[ep.radius * 2, ep.radius * 2, ep.length + ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body2_body8',
            parent='body2',
            child='body8',
            type='revolute',
            position=[0,
                      -1 * (ep.length + ep.radius),
                      0],
            axis=[1, 0, 0]
        )
        pyrosim.Send_Cube(
            name='body8',
            pos=[0, 0, -(ep.length / 2 + ep.radius)],
            size=[ep.radius * 2, ep.radius * 2, ep.length + ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body3_body9',
            parent='body3',
            child='body9',
            type='revolute',
            position=[0,
                      (ep.length + ep.radius),
                      0],
            axis=[1, 0, 0]
        )
        pyrosim.Send_Cube(
            name='body9',
            pos=[0, 0, -(ep.length / 2 + ep.radius)],
            size=[ep.radius * 2, ep.radius * 2, ep.length + ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body4_body10',
            parent='body4',
            child='body10',
            type='revolute',
            position=[0,
                      -1 * (ep.length + ep.radius),
                      0],
            axis=[1, 0, 0]
        )
        pyrosim.Send_Cube(
            name='body10',
            pos=[0, 0, -(ep.length / 2 + ep.radius)],
            size=[ep.radius * 2, ep.radius * 2, ep.length + ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body5_body11',
            parent='body5',
            child='body11',
            type='revolute',
            position=[0,
                      (ep.length + ep.radius),
                      0],
            axis=[1, 0, 0]
        )
        pyrosim.Send_Cube(
            name='body11',
            pos=[0, 0, -(ep.length / 2 + ep.radius)],
            size=[ep.radius * 2, ep.radius * 2, ep.length + ep.radius * 2]
        )
        pyrosim.Send_Joint(
            name='body6_body12',
            parent='body6',
            child='body12',
            type='revolute',
            position=[0,
                      -1 * (ep.length + ep.radius),
                      0],
            axis=[1, 0, 0]
        )
        pyrosim.Send_Cube(
            name='body12',
            pos=[0, 0, -(ep.length / 2 + ep.radius)],
            size=[ep.radius * 2, ep.radius * 2, ep.length + ep.radius * 2]
        )

        pyrosim.End()

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
