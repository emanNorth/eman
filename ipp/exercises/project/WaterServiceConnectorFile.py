import json
import requests

from ipp.common.ConfigUtil import ConfigUtil
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData
from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterDataParserFile import WaterDataParser


class WaterServiceConnector():
    '''
     Base class for connecting to an online water data service.

    Responsibilities:
    - Manage HTTP session.
    - Retrieve raw water data from a water service.
    - Optionally parse raw data into WaterData objects via a WaterDataParser.
    - Provide access to latest raw and parsed data.
    
    Subclasses must implement:
    - _createRequestUrl(): how to build service specific URLs.
    - _getLatestWaterData(): how to retrieve the raw data from the service.
    '''
    WATER_SVC_SECTION_NAME = "Settings.Water"

    def __init__(self, dataParser: WaterDataParser = None):
        '''
         Initialize the WaterServiceConnector instance.

        Args:
            dataParser (WaterDataParser, optional): Parser used to convert
                raw weather service data into a WaterrData object.
        '''
        # The parser that will convert raw data into WaterData
        self.dataParser = dataParser
        self._initProperties()

    def _initProperties(self):
        '''
        Initialize connector properties from the configuration file (IppConfig.props).

        Sets up:
        - baseUrl, userAgent, contentType, and serviceName
        - pollRate, requestTimeout
        - latest raw, JSON, and parsed data
        - HTTP session and connection state
        '''
        self.configUtil = ConfigUtil()
        # Service URL.
        self.baseUrl = \
            self.configUtil.getProperty( \
                WaterServiceConnector.WATER_SVC_SECTION_NAME, "baseUrl")
        self.baseUrl = self.baseUrl.rstrip("/")
        # HTTP header for requests.
        self.userAgent = \
            self.configUtil.getProperty( \
                WaterServiceConnector.WATER_SVC_SECTION_NAME, "userAgent")
        # HTTP Accept header.
        self.contentType = \
            self.configUtil.getProperty( \
                WaterServiceConnector.WATER_SVC_SECTION_NAME, "contentType")
        # Readable name of the service.
        self.serviceName = \
            self.configUtil.getProperty( \
                WaterServiceConnector.WATER_SVC_SECTION_NAME, "serviceName")
        # How often to poll the service.
        self.pollRate = \
            self.configUtil.getInteger( \
                WaterServiceConnector.WATER_SVC_SECTION_NAME, "pollCycleSecs")
        # HTTP timeout in seconds.
        self.requestTimeout = \
            self.configUtil.getInteger( \
                WaterServiceConnector.WATER_SVC_SECTION_NAME, "requestTimeoutSecs")
        
        # Caches for latest data.
        self.latestRawData = None
        self.latestJsonData = None
        self.latestWaterData = None

        # HTTP session object.
        self.clientSession = None
        # boolean flag for connection state.
        self.isConnected = False 

        print(f"Water site name and URL -> {self.serviceName} {self.baseUrl}")
        
    def _createRequestUrl(self, siteID: str = None, locData: WaterLocationData = None):
        '''
        Template method to create the URL for requesting water data.
        
        Must be implemented by subclasses because each water service
        has a different URL format and parameters.

        Args:
            siteID (str, optional): ID of the water site.
            locData (WterLocationData, optional): Location information.

        Returns:
            str: The full URL to request water data.
        '''
        pass

    def _getLatestWaterData(self, requestUrl: str = None, siteID: str = None, locData: WaterLocationData = None) -> dict:
        '''
        Template method to retrieve the latest water data from the service.

        Must be implemented by subclasses because each service returns
        data differently (JSON, XML, etc.).

        Args:
            requestUrl (str, optional): Full URL to fetch water data.
            siteID (str, optional): water site ID.
            locData (WaterLocationData, optional): Location information.

        Returns:
            dict: Raw water data, or None if request failed.
        '''
        pass
    
    def connectToService(self) -> bool:
        '''
        Establish an HTTP session to the water service.

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
            print(f"Connection to {self.serviceName} Water Service failed: {e}")

            return False
            
    def disconnectFromService(self) -> bool:
        '''
        Close the HTTP session to the water service.

        Returns:
            bool: True if disconnect was successful, False otherwise.
        '''
        print(f"Disconnecting from water service {self.serviceName}...")

        if self.clientSession:
            self.clientSession.close()
            self.clientSession = None
            self.isConnected = False

            print(f"Disconnected from {self.serviceName} Water Service")

            return True
            
        return False
    
    def requestCurrentWaterData(self, siteID: str = None, locData: WaterLocationData = None, parameter_code: str = None) -> bool:
        '''
        Request current water data from the water service.

        Workflow:
        1. Build the request URL (_createRequestUrl).
        2. Retrieve raw data from the service (_getLatestWaterData).
        3. Store raw data and JSON representation.
        4. If a parser is available, convert raw data to WaterData object.

        Args:
            siteID (str, optional): Water station ID.
            locData (LocationData, optional): Location info.

        Returns:
            bool: True if data was successfully retrieved, False otherwise.
        '''
        requestUrl = self._createRequestUrl(siteID = siteID, locData = locData, parameter_code = parameter_code)
        responseData = self._getLatestWaterData(requestUrl = requestUrl, siteID = siteID, locData = locData)

        if responseData:
            self.latestRawData = responseData
            self.latestJsonData = json.dumps(self.latestRawData, indent = 2)

            if self.dataParser:
                self.latestWaterData = \
                    self.dataParser.parseWaterData( \
                        rawData = responseData, siteID = siteID, siteName = locData.siteName)
                       
            print(f"Successfully retrieved current water data from URL: {requestUrl}")

            return True

        print(f"Failed to retrieve current water data from URL: {requestUrl}")

        return False
    
    def getLatestWaterData(self) -> WaterData:
        '''Return the latest parsed WaterrData object.'''
        return self.latestWaterData
    
    def getLatestWaterDataAsDict(self) -> dict:
        '''Return the latest raw water data as a dictionary.'''
        return self.latestRawData
    
    def getLatestWaterDataAsJson(self) -> str:
        '''Return the latest raw water data as a formatted JSON string.'''
        return self.latestJsonData
    
    def getPollRate(self) -> int:
        '''Return the configured polling interval (seconds).'''
        return self.pollRate
    
    def getRequestTimeout(self) -> int:
        '''Return the configured request timeout (seconds).'''
        return self.requestTimeout
    
    def getServiceName(self) -> str:
        '''Return the name of the water service.'''
        return self.serviceName
    
    def getBaseUrl(self) -> str:
        '''Return the base URL of the water service.'''
        return self.baseUrl
    
    def isClientConnected(self) -> bool:
        '''Return True if the HTTP session is currently connected.'''
        return self.isConnected    