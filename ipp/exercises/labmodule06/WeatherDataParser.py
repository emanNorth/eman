from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule05.WeatherInfoContainer import CloudLayerData, VisibilityData, WindData

class WeatherDataParser():
    '''
    Base class responsible for parsing raw weather service data
    into a WeatherData object.

    Subclasses must implement the template method
    _createWeatherDataFromRawData().
    '''

    def __init__(self):
        '''
        Initialize the WeatherDataParser instance.
        Currently no instance attributes are set.
        '''
        pass

    def parseWeatherData(self, rawData: dict, stationID: str, stationName: str) -> WeatherData:
        '''
        Handle the parsing of raw weather data into a WeatherData object.

        Acts as a workflow method: checks that all required arguments
        are provided and then calls the template method to create
        a WeatherData instance.

        Args:
            rawData (dict): Raw data received from the weather service.
            stationID (str): The ID of the weather station.
            stationName (str): The name of the weather station.

        Returns:
            WeatherData: Parsed WeatherData object if successful,
                         None if input data is missing.
        '''
         # Only parse if all required data is provided
        if rawData and stationID and stationName:
            # Calls the template method to transform raw data into WeatherData
            return self._createWeatherDataFromRawData(rawData = rawData, stationID = stationID, stationName = stationName)
        else:
            # Warn user that input data is insufficient
            print("No raw data passed provided for parsing into WeatherData. Ignoring.")

            return None
        
    def _createWeatherDataFromRawData(self, rawData: dict, stationID: str, stationName: str) -> WeatherData:
        '''
        Template method to create a WeatherData object from raw data.

        This method must be implemented by subclasses to handle
        service-specific data parsing.

        Args:
            rawData (dict): Raw weather data from the service.
            stationID (str): The ID of the weather station.
            stationName (str): The name of the weather station.

        Returns:
            Parsed WeatherData object when implemented by a subclass.
            Currently None in the base class.
        '''
        pass