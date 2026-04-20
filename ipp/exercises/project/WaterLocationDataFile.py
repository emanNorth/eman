from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil


class WaterLocationData():
    '''
    Holds information about a geographical location.
    '''
    def __init__(self):
        '''
        Initialize all attributes of the USGS water monitoring location.
        ''' 
        self.siteName: str = ""
        self.siteID: str = ""
        self.county: str = ""
        self.state: str = ""
        self.country: str = ""
        self.latitude: float = 0.0
        self.longitude: float = 0.0 
        self.elevation: float = 0.0


