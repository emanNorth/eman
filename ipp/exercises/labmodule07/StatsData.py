
from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil


class StatsData:
    '''
    Hold StatData information including, count, median, min, max, 
    standard deviation & time stamp
   
    '''
    
    def __init__(self):
        '''
        Initialize StatData attributes with default values.
        '''
        self.count : int = 0
        self.mean: float = 0.0
        self.median : float = 0.0
        self.min: float = 0.0 
        self.max: float = 0.0 
        self.standardDeviation: float = 0.0 
        self.timestamp: str = TimeAndDateUtil.getCurrentIso8601LocalDate()
        
    