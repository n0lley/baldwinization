import math

import pybullet

import pyrosim.pyrosim as pyrosim

import pyrosim.constants as c

import math

class NEURON: 

    def __init__(self,line):
    
        self.linkName = None
        self.jointName = None
        self.neuronsFeedingThis = []
        self.activityHistory = []

        self.Determine_Name(line)

        self.Determine_Type(line)

        self.Search_For_Link_Name(line)

        self.Search_For_Joint_Name(line)

        self.Set_Value(0.0)
        
    def Update_Sensor_Neuron(self, robotId):
        if self.jointName is None:
            sensor_value = pyrosim.Get_Touch_Sensor_Value_For_Link(self.Get_Link_Name())
        else:
            sensor_value = pyrosim.Get_Joint_Angle(robotId, self.Get_Joint_Name())/math.pi
        self.Set_Value(sensor_value)
        self.Round_Value()
        self.activityHistory.append(self.Get_Value())
    
    def Update_Hidden_Or_Motor_Neuron(self, neurons, synapses):
        self.Set_Value(0)
        for n in self.Get_Neurons_Feeding_This():
            self.Allow_Presynaptic_Neuron_To_Influence_Me(neurons[n], synapses[(n, self.Get_Name())])
            
        self.Threshold()
        self.Round_Value()
        self.activityHistory.append(self.Get_Value())
        
        
    def Allow_Presynaptic_Neuron_To_Influence_Me(self, neuron, synapse):
        synaptic_input = neuron.Get_Value() * synapse.Get_Weight()
        self.Add_To_Value(synaptic_input)

    def Add_To_Value( self, value ):

        self.Set_Value( self.Get_Value() + value )

    def Get_Joint_Name(self):

        return self.jointName

    def Get_Link_Name(self):

        return self.linkName

    def Get_Name(self):

        return self.name

    def Get_Value(self):

        return self.value
    
    def Get_Neurons_Feeding_This(self):
        
        return self.neuronsFeedingThis

    def Is_Sensor_Neuron(self):

        return self.type == c.SENSOR_NEURON

    def Is_Hidden_Neuron(self):

        return self.type == c.HIDDEN_NEURON

    def Is_Motor_Neuron(self):

        return self.type == c.MOTOR_NEURON

    def Print(self):

        # self.Print_Name()

        # self.Print_Type()

        self.Print_Value()

        # print("")

    def Set_Value(self,value):

        self.value = value
        
    def Round_Value(self):
        
        self.value = round(self.value, 6)

    def Get_History(self):

        return self.activityHistory

# -------------------------- Private methods -------------------------

    def Determine_Name(self,line):

        if "name" in line:

            splitLine = line.split('"')

            self.name = splitLine[1]

    def Determine_Type(self,line):

        if "sensor" in line:

            self.type = c.SENSOR_NEURON

        elif "motor" in line:

            self.type = c.MOTOR_NEURON

        else:

            self.type = c.HIDDEN_NEURON

    def Print_Name(self):

       print(self.name)

    def Print_Type(self):

       print(self.type)

    def Print_Value(self):

       print(self.value , " " , end="" )

    def Search_For_Joint_Name(self,line):

        if "jointName" in line:

            splitLine = line.split('"')

            self.jointName = splitLine[5]

    def Search_For_Link_Name(self,line):

        if "linkName" in line:

            splitLine = line.split('"')

            self.linkName = splitLine[5]

    def Threshold(self):

        self.value = math.tanh(self.value)
        
    def Add_Feeding_Neuron(self, neuronId):
        
        if neuronId not in self.Get_Neurons_Feeding_This():
            self.neuronsFeedingThis.append(neuronId)
