import json
import requests

import ipp.common.ConfigConst as ConfigConst

from ipp.common.ConfigUtil import ConfigUtil
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule06.WeatherDataParser import WeatherDataParser

class WeatherServiceConnector():
    '''
     Base class for connecting to an online weather service.

    Responsibilities:
    - Manage HTTP connection/session.
    - Retrieve raw weather data from a weather service.
    - Optionally parse raw data into WeatherData objects via a WeatherDataParser.
    - Provide access to latest raw and parsed data.
    
    Subclasses must implement:
    - _createRequestUrl(): how to build service-specific URLs.
    - _getLatestWeatherData(): how to retrieve the raw data from the service.
    '''
    
    WEATHER_SVC_SECTION_NAME = "Settings.Weather"

    def __init__(self, dataParser: WeatherDataParser = None):
        '''
         Initialize the WeatherServiceConnector instance.

        Args:
            dataParser (WeatherDataParser, optional): Parser used to convert
                raw weather service data into a WeatherData object.
        '''
        # The parser that will convert raw data into WeatherData
        self.dataParser = dataParser
        self._initProperties()

    def _initProperties(self):
        '''
        Initialize connector properties from the configuration file (IppConfig.props).

        Sets up:
        - baseUrl, userAgent, contentType, serviceName
        - pollRate, requestTimeout
        - latest raw, JSON, and parsed data
        - HTTP session and connection state
        '''
        self.configUtil = ConfigUtil()
        # Service URL.
        self.baseUrl = \
            self.configUtil.getProperty( \
                WeatherServiceConnector.WEATHER_SVC_SECTION_NAME, "baseUrl")
        # HTTP header for requests.
        self.userAgent = \
            self.configUtil.getProperty( \
                WeatherServiceConnector.WEATHER_SVC_SECTION_NAME, "userAgent")
        # HTTP Accept header.
        self.contentType = \
            self.configUtil.getProperty( \
                WeatherServiceConnector.WEATHER_SVC_SECTION_NAME, "contentType")
        # Readable name of the service.
        self.serviceName = \
            self.configUtil.getProperty( \
                WeatherServiceConnector.WEATHER_SVC_SECTION_NAME, "serviceName")
        # How often to poll the service.
        self.pollRate = \
            self.configUtil.getInteger( \
                WeatherServiceConnector.WEATHER_SVC_SECTION_NAME, "pollCycleSecs")
        # HTTP timeout in seconds.
        self.requestTimeout = \
            self.configUtil.getInteger( \
                WeatherServiceConnector.WEATHER_SVC_SECTION_NAME, "requestTimeoutSecs")
        
        # Caches for latest data.
        self.latestRawData = None
        self.latestJsonData = None
        self.latestWeatherData = None

        # HTTP session object.
        self.clientSession = None
        # boolean flag for connection state.
        self.isConnected = False 

        print(f"Weather station name and URL -> {self.serviceName} {self.baseUrl}")
        
        
    def _createRequestUrl(self, stationID: str = None, locData: LocationData = None):
        '''
        Template method to create the URL for requesting weather data.
        
        Must be implemented by subclasses because each weather service
        has a different URL format and parameters.

        Args:
            stationID (str, optional): ID of the weather station.
            locData (LocationData, optional): Location information.

        Returns:
            str: The full URL to request weather data.
        '''
        pass

    def _getLatestWeatherData(self, requestUrl: str = None, stationID: str = None, locData: LocationData = None) -> dict:
        '''
        Template method to retrieve the latest weather data from the service.

        Must be implemented by subclasses because each service returns
        data differently (JSON, XML, etc.).

        Args:
            requestUrl (str, optional): Full URL to fetch weather data.
            stationID (str, optional): Weather station ID.
            locData (LocationData, optional): Location information.

        Returns:
            dict: Raw weather data, or None if request failed.
        '''
        pass
    
    
    def connectToService(self) -> bool:
        '''
        Establish an HTTP session to the weather service.

        Returns:
            bool: True if connection is successful, False otherwise.
        '''
        try:
            # Create a session for connection pooling
            self.clientSession = requests.Session()
            
            # Set default headers (required by most services)
            self.clientSession.headers.update({
                'User-Agent': self.userAgent,
                'Accept': self.contentType
            })
            
            return True
        
        except Exception as e:
            print(f"Connection to {self.serviceName} Weather Service failed: {e}")

            return False
            
    def disconnectFromService(self) -> bool:
        '''
        Close the HTTP session to the weather service.

        Returns:
            bool: True if disconnect was successful, False otherwise.
        '''
        print(f"Disconnecting from weather service {self.serviceName}...")

        if self.clientSession:
            self.clientSession.close()
            self.clientSession = None
            self.isConnected = False

            print(f"Disconnected from {self.serviceName} Weather Service")

            return True
            
        return False
    
    def requestCurrentWeatherData(self, stationID: str = None, locData: LocationData = None) -> bool:
        '''
        Request current weather data from the weather service.

        Workflow:
        1. Build the request URL (_createRequestUrl).
        2. Retrieve raw data from the service (_getLatestWeatherData).
        3. Store raw data and JSON representation.
        4. If a parser is available, convert raw data to WeatherData object.

        Args:
            stationID (str, optional): Weather station ID.
            locData (LocationData, optional): Location info.

        Returns:
            bool: True if data was successfully retrieved, False otherwise.
        '''
        requestUrl = self._createRequestUrl(stationID = stationID, locData = locData)
        responseData = self._getLatestWeatherData(requestUrl = requestUrl, stationID = stationID, locData = locData)

        if responseData:
            self.latestRawData = responseData
            self.latestJsonData = json.dumps(self.latestRawData, indent = 2)

            if self.dataParser:
                self.latestWeatherData = \
                    self.dataParser.parseWeatherData( \
                        rawData = responseData, stationID = stationID, stationName = locData.name)
            
            print(f"Successfully retrieved current weather data from URL: {requestUrl}")

            return True

        print(f"Failed to retrieve current weather data from URL: {requestUrl}")

        return False
    
    
    def getLatestWeatherData(self) -> WeatherData:
        '''Return the latest parsed WeatherData object.'''
        return self.latestWeatherData
    
    def getLatestWeatherDataAsDict(self) -> dict:
        '''Return the latest raw weather data as a dictionary.'''
        return self.latestRawData
    
    def getLatestWeatherDataAsJson(self) -> str:
        '''Return the latest raw weather data as a formatted JSON string.'''
        return self.latestJsonData
    
    def getPollRate(self) -> int:
        '''Return the configured polling interval (seconds).'''
        return self.pollRate
    
    def getRequestTimeout(self) -> int:
        '''Return the configured request timeout (seconds).'''
        return self.requestTimeout
    
    def getServiceName(self) -> str:
        '''Return the name of the weather service.'''
        return self.serviceName
    
    def getBaseUrl(self) -> str:
        '''Return the base URL of the weather service.'''
        return self.baseUrl
    
    def isClientConnected(self) -> bool:
        '''Return True if the HTTP session is currently connected.'''
        return self.isConnected    