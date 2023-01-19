from pyrosim import pyrosim
import pybullet as p
import os
import pickle

from pyrosim.neuralNetwork import NEURAL_NETWORK
import experiment_parameters as ep
from motor import MOTOR

class ROBOT:
    def __init__(self, robot_type, seed, id_tag):
            
        self.motors = {}
        
        body_file = robot_type+"_body.urdf"
        brain_file = seed+"/"+robot_type + "_brain"+id_tag+".nndf"
        
        self.robotId = p.loadURDF("/bodyfiles/"+body_file)
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK(brain_file, do_hebbian=True)

        os.system("rm "+brain_file)
        
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            
    def think(self):
        self.nn.Update(self.robotId)
    
    def act(self):
        for n in self.nn.get_neuron_names():
            if self.nn.is_motor_neuron(n):
                joint_name = self.nn.get_motor_neurons_joint(n)
                desired_angle = self.nn.get_value_of(n) * ep.joint_range
                self.motors[joint_name].set_value(self.robotId, desired_angle)
    
    def get_fitness(self, id_tag, seed):
        position = p.getLinkState(self.robotId, 0)[0]
        displacement = (position[0]**2 + position[1]**2)**.5
        synaptic_behavior = self.nn.get_synapse_activity()

        f = open(seed+"/tmp"+id_tag+".txt", 'w')
        f.write(str(displacement))
        f.close()

        f = open(seed+"/synapses"+id_tag+".p", 'wb')
        pickle.dump(synaptic_behavior, f)
        f.close()

        os.system("mv "+seed+"/tmp"+id_tag+".txt "+seed+"/fitness"+id_tag+".txt")
