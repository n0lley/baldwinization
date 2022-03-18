import numpy as np
import os

from robot import ROBOT
from snake import SNAKE
from quad import QUAD
from hex import HEX

class CONTROLLER:
    
    def __init__(self, type):
    
        dimensions = []
        self.genome = {}
        self.fitness = 0
        self.behavior = {}
        
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
        
        for col in range(len(dimensions)-1):
            for n1 in dimensions[col]:
                for n2 in dimensions[col+1]:
                    self.genome[(n1, n2)] = self.generate_gene()
        
    
    def generate_gene(self):
        weight = (np.random.random()*2) - 1
        weight = round(weight, 6)
        learningRate = round(np.random.random(), 6)
        gene = [weight, learningRate]
        for i in range(4):
            param = round(np.random.random(), 6)
            gene.append(param)
        return gene

    def mutate(self):
        for gene in self.genome:
            if np.random.random() < ep.mutation_prob:
                gene[0] = np.random.normal(loc = gene[0])
                gene[0] = round(gene[0], 6)
                if gene[0] < -1: gene[0] = -1
                elif gene[0] > 1: gene[0] = 1
            
            if np.random.random() < ep.mutation_prob:
                gene[1] = round(np.random.normal(loc=gene[1]), 6)
                if gene[1] < 0: gene[0] = 0
                elif gene[1] > 1: gene[0] = 1
                
                for i in range(2,6):
                    gene[i] = round(np.random.normal(loc=gene[i]), 6)
                    if gene[i] < 0 : gene[i] = -1
                    elif gene[i] > 1 : gene[i] = 1

    def get_genome(self):
        return self.genome
    
    def Print(self):
        for gene in self.genome:
            print(gene, ":", self.genome[gene])

    def evaluate(self):
        self.generator.make_brain(self.get_genome())
        os.system("python3 simulate.py "+self.generator.get_type())
