# Test 1 vehicles and derivatives 

class Vehicle:
    '''
    Holds vehicle information including flying capability,
    electric status, wheels, and rail requirements.
    '''
    def __init__(self, canFly, isElectric, hasWheels, requiresRails):
        '''
        Initialize vehicle attributes.
        '''
        self.canFly = canFly
        self.isElectric = isElectric
        self.hasWheels = hasWheels
        self.requiresRails = requiresRails
        
        # Optional additional attributes (not required as constructor arguments)
        self.color = "Unknown"
        self.maxSpeed = 0.0
        
    # Accessor methods (getters)
    def getCanFly(self):
        return self.canFly
        
    def getIsElectric(self):
        return self.isElectric
        
    def getHasWheels(self):
        return self.hasWheels
        
    def getRequiresRails(self):
        return self.requiresRails
        
    def getColor(self):
        return self.color 
        
    def getMaxSpeed(self):
        return self.maxSpeed 
        
        
class Automobile(Vehicle):
    '''
    Automobile is derived from Vehicle.
    Automobiles cannot fly and do not require rails.
    '''
        
    def __init__(self, isElectric, color="Unknown", maxSpeed=0.0):
        '''
        Initialize an Automobile object, inheriting from Vehicle.

        Args:
            isElectric (bool): Indicates whether the automobile is electric.
            color (str, optional): The color of the automobile. Defaults to "Unknown".
            maxSpeed (float, optional): The maximum speed of the automobile. Defaults to 0.0.

        Actions:
            canFly is fixed to False (cars cannot fly)
            hasWheels is fixed to True (all cars have wheels)
            requiresRails is fixed to False (cars do not run on rails)
            color and maxSpeed can be customized per object
    
        '''
        super().__init__(canFly=False, isElectric=isElectric, hasWheels=True, requiresRails=False)
        self.color = color
        self.maxSpeed = maxSpeed
        
class Airplane(Vehicle):
    '''
    Airplane is derived from Vehicle.
    Airplanes can fly and do not require rails.
    '''
    
    def __init__(self):
        '''
        Initialize an airplane object, inheriting from vehicle.
            
        Args:
            None
                
        Actions:
            canFly is fixed to True (Airplane can fly).
            isElectric is fixed on False (Airplane run on fuel)
            hasWheels is fixed to True (all Airplane have wheels for landing and take off).
            requiresRails is fixed to False (Airplane don't run on rails).
        '''
        super().__init__(canFly=True, isElectric=False, hasWheels=True, requiresRails=False)
        
        
class Train(Vehicle):
    '''
    Train is derived from vehicle.
    Trains cannot fly and always run on rails.
    '''
        
    def __init__(self, isElectric):
        '''
        Initialize a train object, inheriting from vehicle.
            
        Args:
            isElectric (bool): Indicates whether the train is electric.
                
        Actions:
            canFly is fixed to False (trains cannot fly).
            hasWheels is fixed to True (all trains have wheels).
            requiresRails is fixed to True (trains run on rails).
        '''
        super().__init__(canFly=False, isElectric=isElectric, hasWheels=True, requiresRails=True)
            
class Rocket(Vehicle):
    '''
    Rocket is derived from vehicle.
    Rockets can fly and do not require rails.
    '''
    def __init__(self):
        '''
        Initialize a rocket object, inheriting from vehicle.
            
        Args:
            None
                
        Actions:
            canFly is fixed to True (Rockets can fly).
            isElectric is fixed on False (Rockets run on fuel)
            hasWheels is fixed to False (all Rockets don't have wheels).
            requiresRails is fixed to False (Rockets don't run on rails).
        '''
        super().__init__(canFly=True, isElectric=False, hasWheels=False, requiresRails=False)
        
            
# Test 2: Instantiate and test objects

v = Vehicle(False, False, False, False) 
a = Automobile(True, "Blue", 180.0)
p = Airplane()
t = Train(True)
r = Rocket()

print(v.getCanFly())
print(v.getRequiresRails())
print(a.getColor())
print(a.getMaxSpeed())
print(p.getIsElectric())
print(p.getHasWheels())
print(t.getIsElectric())
print(t.getMaxSpeed())
print(r.getRequiresRails())
print(r.getHasWheels())

# check instance of each (i: is the object, t: is the class we are checking against)
print(isinstance(v, Vehicle))
print(isinstance(a, Vehicle))
print(isinstance(p, Airplane))
print(isinstance(p, Train))
print(isinstance(t, Train))
print(isinstance(r, Vehicle))
print(isinstance(r, Rocket))
