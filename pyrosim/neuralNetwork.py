from pyrosim.neuron  import NEURON

from pyrosim.synapse import SYNAPSE

import time

class NEURAL_NETWORK: 

    def __init__(self,nndfFileName, do_hebbian=True):

        self.neurons = {}

        self.synapses = {}
        
        self.do_hebbian = do_hebbian

        f = open(nndfFileName,"r")

        for line in f.readlines():

            self.Digest(line)

        f.close()
        
        self.Precalculate_Connections()

    def Print(self):

        self.Print_Sensor_Neuron_Values()

        self.Print_Hidden_Neuron_Values()

        self.Print_Motor_Neuron_Values()

        print("")
    
    def Update(self, robotId):
        for n in self.neurons:
            if self.neurons[n].Is_Sensor_Neuron():
                self.neurons[n].Update_Sensor_Neuron(robotId)
            else:
                self.neurons[n].Update_Hidden_Or_Motor_Neuron(self.neurons, self.synapses)
        for s in self.synapses:
            if self.do_hebbian:
                self.synapses[s].Update_Synapse(self.neurons[s[0]], self.neurons[s[1]])
                
    def get_neuron_names(self):
        return self.neurons.keys()
        
    def is_motor_neuron(self, neuron_name):
        return self.neurons[neuron_name].Is_Motor_Neuron()
    
    def get_motor_neurons_joint(self, neuron_name):
        return self.neurons[neuron_name].Get_Joint_Name()
        
    def get_value_of(self, neuron_name):
        return self.neurons[neuron_name].Get_Value()

    def get_synapse_activity(self):
        synapse_activity = {}
        for s in self.synapses:
            synapse_activity[s] = self.synapses[s].Get_Weights_At_Each_Update()
        return synapse_activity

# ---------------- Private methods --------------------------------------

    def Add_Neuron_According_To(self,line):

        neuron = NEURON(line)

        self.neurons[ neuron.Get_Name() ] = neuron

    def Add_Synapse_According_To(self,line):

        synapse = SYNAPSE(line)

        sourceNeuronName = synapse.Get_Source_Neuron_Name()

        targetNeuronName = synapse.Get_Target_Neuron_Name()

        self.synapses[sourceNeuronName , targetNeuronName] = synapse

    def Digest(self,line):

        if self.Line_Contains_Neuron_Definition(line):

            self.Add_Neuron_According_To(line)

        if self.Line_Contains_Synapse_Definition(line):

            self.Add_Synapse_According_To(line)
            
    def Precalculate_Connections(self):
        
        for synapse in self.synapses:
            self.neurons[synapse[1]].Add_Feeding_Neuron(synapse[0])

    def Line_Contains_Neuron_Definition(self,line):

        return "neuron" in line

    def Line_Contains_Synapse_Definition(self,line):

        return "synapse" in line

    def Print_Sensor_Neuron_Values(self):

        print("sensor neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Sensor_Neuron():

                self.neurons[neuronName].Print()

        print("")

    def Print_Hidden_Neuron_Values(self):

        print("hidden neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Hidden_Neuron():

                self.neurons[neuronName].Print()

        print("")

    def Print_Motor_Neuron_Values(self):

        print("motor neuron values: " , end = "" )

        for neuronName in sorted(self.neurons):

            if self.neurons[neuronName].Is_Motor_Neuron():

                self.neurons[neuronName].Print()

        print("")
