
class WindData:
    '''
    Holds wind information including speed, gust, and direction.
    '''
    def __init__(self):
        '''
        Initialize all wind attributes with default values.
        
        Args:
            None 
            
        Returns: 
            None 
        ''' 
        self.speedKph = 0.0
        self.gustKph = 0.0
        self.directionDegrees = 0.0
    
class VisibilityData:
    '''
    Holds visibility information in meters.
    '''
    def __init__(self):
        '''
        Initialize visibility attribute with a default value.
        
        Args:
            None 
            
        Returns: 
            None 
        ''' 
        self.meters = 0.0

class CloudLayerData:
    '''
    Holds cloud layer information including amount and base altitude.
    '''
    def __init__(self):
        '''
        Initialize cloud layer attributes with default values..
        
        Args:
            None 
            
        Returns: 
            None 
        ''' 
        self.amount = 0.0
        self.baseMeters = 0.0
        
        