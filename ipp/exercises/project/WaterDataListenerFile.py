from ipp.exercises.project.WaterDataFile import WaterData


class WaterDataListener():
    '''
    Base class used to receive water data updates from the
    waterServiceManager.

    Subclasses must implement the _processWaterData() method
    to define how incoming water data should be handled.
    '''
    def __init__(self):
        '''
        Initialize the WaterDataListener.
        '''
        pass
    
    def handleIncomingWaterData(self, data: WaterData=None):
        '''
        Handle incoming WaterData from the Water service.

        Args:
            data (WaterData): The WaterData object received
                                from the Water service.

        Returns:
            None
        '''
        # Only process if data is not None
        if data:
            # Calls the template method
            self._processWaterData(waData = data)
            
    def _processWaterData(self, waData: WaterData=None ):
        '''
        Template method to process incoming water data.

        This method must be implemented by subclasses.

        Args:
            waData (WaterData): The WaterData instance to process.

        Returns:
            None
        '''
        pass
    
    
