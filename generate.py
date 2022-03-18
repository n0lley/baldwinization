import pyrosim
import experiment_parameters as ep

import numpy as np

def create_world():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.End()
    
def quad_brain():
    pyrosim.Start_NeuralNetwork("quad_brain.nndf")
    pyrosim.End()
    
def hex_brain():
    pyrosim.Start_NeuralNetwork("hex_brain.nndf")
    pyrosim.End()

create_world()
