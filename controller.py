import numpy as np
import os
import time
import pickle

import experiment_parameters as ep
from snake import SNAKE
from quad import QUAD
from hex import HEX

class CONTROLLER:
    
    def __init__(self, type, id, input_parameters=None):
        """
        From provided robot type, establish genome dimensions and generate a random nn genome of that shape
        New robot types will need to expand this bit.
        If no hebbian parameters are provided for use, generate a new set of hebbian parameters.
        """
    
        dimensions = []
        self.genome = {}
        self.hebbian_parameters = {}
        self.fitness = 0
        self.ID = str(id)

        has_hebbs = True
        if input_parameters == None:
            has_hebbs = False
        else:
            self.hebbian_parameters = input_parameters

        #Robot type genome dimensions - Each column has a range of integers indicating the id numbers of the neurons
        if type == "snake":
            dimensions = [range(4), range(4,8), range(8,11)]
            self.generator = SNAKE()
        
        elif type == "quad":
            dimensions = [range(12), range(12, 24), range(24, 32)]
            self.generator = QUAD()
        
        elif type == "hex":
            dimensions = [range(18), range(18,36), range(36, 48)]
            self.generator = HEX()
            
        else:
            print("Error - robot type", type, "not recognized. Genome creation failed.")
            exit(0)

        #create (neuron, neuron) pairs and attach random synaptic weights to them
        #generate hebbian parameters if none have been provided (see function for more on that)
        for col in range(len(dimensions)-1):
            for n1 in dimensions[col]:
                for n2 in dimensions[col+1]:
                    self.genome[(n1, n2)] = self.generate_gene()
                    if not has_hebbs:
                        self.hebbian_parameters[(n1, n2)] = self.generate_hebbian()

    def generate_gene(self):
        """
        Generates and returns a synaptic weight + learning rate
        Should only be called at initialization
        """
        weight = (np.random.random()*2) - 1
        weight = round(weight, 6)

        learning_rate = np.random.random()
        learning_rate = round(learning_rate, 6)

        return [weight, learning_rate]

    def generate_hebbian(self):
        """
        Generates and returns a set of hebbian parameters.
        Should only be called at initialization and only if no parameters are provided.
        EDIT - This should only be called once, for the first robot of the first population.
        Subsequent robots get random perturbations of that original network (see najarro + risi paper)
        """
        parameter_set = []
        for i in range(4):
            p = round(np.random.random()*2 - 1, 6)
            parameter_set.append(p)

        return parameter_set

    def mutate(self, mutation_rate):
        """
        Modify each beginning synaptic weight with probability (ep.mutation_prob).
        Perturbations are on a normal distribution centered on the current synaptic weight, bounded within the range [-1, 1]
        """
        for gene in self.genome:
            if np.random.random() < mutation_rate:
                #modify initial weight
                self.genome[gene][0] = np.random.normal(loc = self.genome[gene][0])
                self.genome[gene][0] = round(self.genome[gene][0], 6)
                if self.genome[gene][0] < -1: self.genome[gene][0] = -1
                elif self.genome[gene][0] > 1: self.genome[gene][0] = 1

                #modify learning rate
                self.genome[gene][1] = np.random.normal(loc = self.genome[gene][1])
                self.genome[gene][1] = round(self.genome[gene][1], 6)
                if self.genome[gene][1] < 0: self.genome[gene][1] = 0
                elif self.genome[gene][1] > 1: self.genome[gene][1] = 1

    def set_ID(self, new_ID):
        self.ID = str(new_ID)

    def set_hebbian_parameters(self, new_hebb):
        self.hebbian_parameters = new_hebb

    def get_genome(self):
        return self.genome
        
    def get_hebbian_parameters(self):
        return self.hebbian_parameters
        
    def get_fitness(self):
        return self.fitness

    def reset(self):
        self.fitness = 0
        self.hebbian_parameters = None
    
    def Print(self):
        for gene in self.genome:
            print(gene, ":", self.genome[gene])

    def start_simulation(self, seed, play_blind=1):
        """
        Spins up a simulation with simulate.py
        Output channel goes to <RUN SEED>.txt
        Shouldn't put out more than the usual pybullet chatter unless something blows up
        """
        self.generator.make_brain(self.get_genome(), self.get_hebbian_parameters(), self.ID, seed)
        os.system("python3 simulate.py "+self.generator.get_type()+" "+str(play_blind)+" "+self.ID+" "+seed+" 2&>"+seed+".txt &")

    def wait_to_finish(self, seed):
        """
        Holding function until simulation wraps up+transcribes output to file
        Saves fitness and synaptic activity data to class vars then deletes those files
        """

        while not os.path.exists(seed+"/fitness"+self.ID+".txt"):
            time.sleep(.001)

        f = open(seed+"/fitness"+self.ID+".txt", 'r')
        fits = f.read().strip().split('\n')
        self.fitness = float(fits[-1])

        os.system("rm "+seed+"/fitness"+self.ID+".txt")

        f = open(seed+"/synapses"+self.ID+".p", 'rb')
        self.synaptic_activity = pickle.load(f)
        f.close()

        f = open(seed+"/neurons"+self.ID+".p", 'rb')
        self.neuron_activity = pickle.load(f)
        f.close()

        os.system("rm "+seed+"/synapses"+self.ID+".p")