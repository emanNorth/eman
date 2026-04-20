from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData


class WaterDataParser():
    '''
    Base class responsible for parsing raw water service data into a WaterData object.

    Subclasses must implement the template method
    _createWaterDataFromRawData().
    '''
    def __init__(self):
        '''
        Initialize the WaterDataParser instance. Currently no instance attributes are set.
        '''
        pass

    def parseWaterData(self, rawData: dict, siteID: str, siteName: str) -> WaterData:
        '''
        Handle the parsing of raw water data into a WaterData object.

        Acts as a workflow method: checks that all required arguments are provided 
        and then calls the template method to create a WaterData instance.

        Args:
            rawData (dict): Raw data received from the water service.
            siteID (str): The ID of the water monitoring location identifier.
            siteName (str): The name of the water monitoring location identifier.

        Returns:
            WaterData: Parsed WaterData object if successful, None if input data is missing.
        '''
         # Only parse if all required data is provided
        if rawData and siteID and siteName:
            # Calls the template method to transform raw data into WaterData
            return self._createWaterDataFromRawData(rawData = rawData, siteID = siteID, siteName = siteName)
        else:
            # Warn user that input data is insufficient
            print("No raw data passed provided for parsing into WaterData. Ignoring.")

            return None
        
    def _createWaterDataFromRawData(self, rawData: dict, siteID: str, siteName: str) -> WaterData:
        '''
        Template method to create a WaterData object from raw data.

        This method must be implemented by subclasses to handle
        service specific data parsing.

        Args:
            rawData (dict): Raw water data from the service.
            siteID (str): The ID of the water monitoring location identifier.
            siteName (str): The name of the water monitoring location identifier.

        Returns:
            Parsed WaterData object when implemented by a subclass.
            Currently None in the base class.
        '''
        pass
    
    


    