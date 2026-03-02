from ipp.exercises.labmodule05.WeatherData import WeatherData

class WeatherDataListener():
    '''
    Base class used to receive weather data updates from the
    WeatherServiceManager.

    Subclasses must implement the _processWeatherData() method
    to define how incoming weather data should be handled.
    '''
    
    def __init__(self):
        '''
        Initialize the WeatherDataListener.
        '''
        pass
    
    def handleIncomingWeatherData(self, data: WeatherData=None):
        '''
        Handle incoming WeatherData from the weather service.

        Args:
            data (WeatherData): The WeatherData object received
                                from the weather service.

        Returns:
            None
        '''
        # Only process if data is not None
        if data:
            # Calls the template method
            self._processWeatherData(wData = data)
            
    def _processWeatherData(self, wData: WeatherData=None ):
        '''
        Template method to process incoming weather data.

        This method must be implemented by subclasses.

        Args:
            wData (WeatherData): The WeatherData instance to process.

        Returns:
            None
        '''
        pass
    
    

