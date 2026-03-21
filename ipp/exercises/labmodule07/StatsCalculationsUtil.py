import statistics

from typing import List

from ipp.exercises.labmodule05.CalculationsUtil import CalculationsUtil
from ipp.exercises.labmodule07.StatsData import StatsData

class StatsCalculationsUtil(CalculationsUtil):
    '''
    Utility class for calculating statistical information from a list of floats.
    Inherits from CalculationsUtil.
    '''
    def __init__(self):
        ''' Initialize the StatsCalculationsUtil class.'''
        pass
    
    @classmethod
    def calculateStats(cls, values: List[float]) -> StatsData:
        '''
        Calculate statistics for a list of float values.

        Handles empty lists by returning default StatsData.
        set count, min, max, mean, median, standard deviation, and timestamp.
        
        Args:
            values (List[float]): List of float numbers to calculate statistics from.
            
        Returns:
            StatsData: An object containing count, min, max, mean, median,
                       standard deviation, and timestamp.
        '''
        
        try:
            # Checks if the input list is empty or None
            if not values:
                return StatsData()
            
            stats = StatsData()
            
            # Set the number of values
            stats.count = len(values)
            
            # Set minimum value in the list
            stats.min = min(values)
            
            # Set maximum value in the list
            stats.max = max(values)
            
            # Set statistical mean
            stats.mean = statistics.mean(values)
            
            # Set statistical median
            stats.median = statistics.median(values)
        
            # set standard deviation only if there are 2 or more values
            if len(values) > 1:
                stats.standardDeviation = statistics.stdev(values)
            else:
                stats.standardDeviation = 0.0
              
            # Returns the fully populated StatsData object.  
            return stats
        
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return None
        
    
        
        
        
        
        