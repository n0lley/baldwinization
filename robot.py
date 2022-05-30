import pyrosim
import pybullet as p
import numpy as np

from neuralNetwork import NEURAL_NETWORK
from motor import MOTOR
import experiment_parameters as ep

class ROBOT:
    def __init__(self, robot_type):
            
        self.motors = {}
        
        body_file = robot_type+"_body.urdf"
        brain_file = robot_type+"_brain.nndf"
        
        self.robotId = p.loadURDF("/botfiles/"+body_file)
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK(brain_file, do_hebbian=True)
        
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            
    def think(self):
        self.nn.Update(self.robotId)
    
    def act(self):
        for n in self.nn.get_neuron_names():
            if self.nn.is_motor_neuron(n):
                joint_name = self.nn.get_motor_neurons_joint(n)
                desired_angle = self.nn.get_value_of(n)
                self.motors[joint_name].set_value(self.robotId, desired_angle)
    
    def get_fitness(self):
        position = p.getLinkState(self.robotId, 0)[0]
        displacement = (position[0]**2 + position[1]**2)**.5
        f = open("fitnesses/fitness.txt", 'w')
        f.write(str(displacement))
        f.close()
    
    def make_body(self):
        pass
    
    def make_brain(self):
        pass
