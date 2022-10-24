import math

import pyrosim as pyrosim

import pyrosim.constants as c

class SYNAPSE: 

    def __init__(self,line):

        self.Determine_Source_Neuron_Name(line)

        self.Determine_Target_Neuron_Name(line)

        self.Determine_Weight(line)
        
        self.Determine_Learning_Rule(line)
        
        self.weightsAtEachUpdate = [self.Get_Weight()]

    def Get_Source_Neuron_Name(self):

        return self.sourceNeuronName

    def Get_Target_Neuron_Name(self):

        return self.targetNeuronName

    def Get_Weight(self):

        return self.weight
    
    def Get_Learning_Rules(self):
        
        return self.learningRule

    def Get_Weights_At_Each_Update(self):

        return self.weightsAtEachUpdate
    
    def Update_Synapse(self, presynapticNeuron, postsynapticNeuron):
        rate = self.learningRule[0]
        A = self.learningRule[1]
        B = self.learningRule[2]
        C = self.learningRule[3]
        D = self.learningRule[4]
        
        x = presynapticNeuron.Get_Value()
        y = postsynapticNeuron.Get_Value()
        
        delta = rate * (A*x*y + B*x + C*y + D) #From Najarro and Risi, Metalearning through Hebbian Plasticity
        self.weight = self.Get_Weight() + delta
        self.weight = round(self.Get_Weight(), 6)
        if self.weight > 1:
            self.weight = 1
        elif self.weight < -1:
            self.weight = -1
        self.weightsAtEachUpdate.append(self.Get_Weight())

# -------------------------- Private methods -------------------------

    def Determine_Source_Neuron_Name(self,line):

        if "sourceNeuronName" in line:

            splitLine = line.split('"')

            self.sourceNeuronName = splitLine[1]

    def Determine_Target_Neuron_Name(self,line):

        if "targetNeuronName" in line:

            splitLine = line.split('"')

            self.targetNeuronName = splitLine[3]

    def Determine_Weight(self,line):

        if "weight" in line:

            splitLine = line.split('"')

            self.weight = float( splitLine[5] )

    def Determine_Learning_Rule(self, line):
        
        if "learningRule" in line:
            
            splitLine = line.split('"')
            
            rules = splitLine[7]
            rules = rules[1:len(rules)-1]
            rules = rules.split(", ")
            self.learningRule = [float(r) for r in rules]
