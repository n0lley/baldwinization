import pyrosim

class SENSOR:
    
    def __init__(self, linkname):
        
        self.linkname = linkname
        self.values = []
        
    def get_value(self):
        return None
        
class Touch_Sensor(SENSOR):

    def __init__(self, linkname):
        super.__init__(linkname)
        
    def get_value(self):
        self.values.append(pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkname))

class Proprioceptive_Sensor(SENSOR):
    
    def __init__(self, jointname):
        self.jointname = jointname
        self.values = []
    
    def get_value(self):
        self.values.append(pyrosim.Get_Joint_Angle(self.jointname))
