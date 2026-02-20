
from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil

class LocationData():
    '''
    Holds information about a geographical location and its coordinates.
    '''
    
    def __init__(self):
        '''
        Initialize all attributes of the location.
        
        Args:
            None 
            
        Returns: 
            None 
        ''' 
        self.name: str = ""
        self.nameID: str = ""
        self.city: str = ""
        self.region: str = ""
        self.country: str = ""
        self.latitude: float = 0.0
        self.longitude: float = 0.0 
        self.elevation: float = 0.0
     