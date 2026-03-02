import itertools

from apscheduler.schedulers.background import BackgroundScheduler

from ipp.common.ConfigUtil import ConfigUtil
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule06.NoaaWeatherServiceConnector import NoaaWeatherServiceConnector
from ipp.exercises.labmodule06.WeatherDataListener import WeatherDataListener
from ipp.exercises.labmodule06.WeatherServiceConnector import WeatherServiceConnector

class WeatherServiceManager():
    '''
    Manages weather data retrieval from a configured weather service asynchronously.
    
    This class acts as a "state machine" to periodically fetch weather data for
    a list of weather stations using the APScheduler for concurrency. Users can
    attach a listener to receive weather updates in real time.
    '''
    
    def __init__(self):
        '''
        Initializes the WeatherServiceManager instance.
        
        Sets up the scheduler, running state, listener, and loads properties
        from the configuration file.
        '''
        self.scheduler = BackgroundScheduler()
        self.isRunning = False
        self.dataListener = None

        # Load configuration properties and initialize weather service
        self._initProperties()
        
    def _initProperties(self):
        '''
        Load configuration properties from IppConfig.props and setup the
        weather service connection.

        Initializes the station polling cycle based on configured station IDs.
        Defaults to KBOS if no stations are configured.
        '''
        self.configUtil = ConfigUtil()

        self.weatherSvc = NoaaWeatherServiceConnector()
        self.clientSession = None
        self.isConnected = False

        # Read the station IDs to poll from configuration file
        self.pollStationIDs = \
            self.configUtil.getProperty( \
                WeatherServiceConnector.WEATHER_SVC_SECTION_NAME, "pollStationIDs")
        
        self.pollStationList = [stationID.strip() for stationID in self.pollStationIDs.split(',')]
        self.pollStationCycle = None

        if self.pollStationIDs:
            print(f"Polling weather station ID's: {self.pollStationIDs}")

            self.pollStationCycle = itertools.cycle(self.pollStationList)
        else:
            # default to Boston (KBOS)
            self.pollStationIDs = "KBOS"

            print(f"No weather station ID's defined in config file. Using default: {self.pollStationIDs}")
            
    def _scheduleAndStartWeatherServiceJob(self):
        '''
        Configures the APScheduler to repeatedly call `processWeatherData` at
        intervals defined by the weather service's polling rate.

        Ensures only one instance runs at a time and coalesces missed runs.
        '''
        pollRate = self.weatherSvc.getPollRate()
        
    
        # delays once a response is received
        # Schedule job to fetch weather data at defined pollRate intervals
        self.scheduler.add_job( \
            func = self.processWeatherData, trigger = 'interval', \
            id = self.pollStationIDs, replace_existing = True, seconds = pollRate, \
            max_instances = 1, coalesce = True, misfire_grace_time = None)
        
        # Start the scheduler in the background
        self.scheduler.start() 
        
    
    def startManager(self):
        '''
        Starts the weather service manager.

        Connects to the weather service if not already connected, schedules
        the periodic weather data fetching job, and sets the running state.
        
        Returns:
            success (bool): True if manager started successfully, else False
        '''
        success = False

        if not self.isRunning:
            print("Creating weather service client and connecting to service.")

            # Connect to weather service if not already connected
            if not self.weatherSvc.isClientConnected():
                self.weatherSvc.connectToService()

            self._scheduleAndStartWeatherServiceJob()

            self.isRunning = True

            print("Weather station manager is now up and running!")

            success = True
        else:
            print("Client is already connected to weather service!")
            success = True

        return success
    
    
    def stopManager(self):
        '''
        Stops the weather service manager.

        Disconnects from the weather service, shuts down the scheduler,
        and updates the running state.

        Returns:
            success (bool): True if manager stopped successfully, else False
        '''
        success = False

        
        if self.isRunning:
            print("Disconnecting from weather service.")
            
            # Disconnect the weather service client if connected
            if self.weatherSvc.isClientConnected():
                self.weatherSvc.disconnectFromService()
                
            try:
                self.scheduler.shutdown(wait = False)
                self.isRunning = False
                success = True
            except:
                print("Failed to shutdown scheduler. Probably not running.")
        else:
            print("No weather service connection created! Call startManager() first.")

        return success
    
    
    def _getLocationData(self, stationID: str = None):
        '''
        Returns LocationData for a given weather station ID.

        Args:
            stationID (str): The weather station ID (e.g., KBOS, KJFK)
        
        Returns:
            LocationData: Location details of the station
        '''
        if stationID == "KJFK":
            # NYC (JFK airport)
            locData = LocationData()
            locData.name = "JFK International Airport"
            locData.city = "New York"
            locData.region = "NY"
            locData.country = "USA"
            locData.latitude = 40.63972
            locData.longitude = 73.77889

            return locData
        
        elif stationID == "KORD":
            # ORD (O'Hare airport)
            locData = LocationData()
            locData.name = "O'Hare International Airport"
            locData.city = "Chicago"
            locData.region = "IL"
            locData.country = "USA"
            locData.latitude = 40.978611
            locData.longitude = 73.904724

            return locData
        elif stationID == "KBOS":
            # BOS (Logan aiport)
            locData = LocationData()
            locData.name = "Logan International Airport"
            locData.city = "Boston"
            locData.region = "MA"
            locData.country = "USA"
            locData.latitude = 40.35843
            locData.longitude = 73.05977

            return locData
        else:
            # Unknown - just use stationID and zero out lat / lon
            locData = LocationData()
            locData.name = stationID
            locData.city = stationID
            locData.region = stationID
            locData.country = stationID
            locData.latitude = 0.0
            locData.longitude = 0.0

            return locData
        
    def processWeatherData(self):
        '''
        Fetches and processes the latest weather data for the next station
        in the polling cycle.

        Retrieves raw and JSON-formatted weather data, and notifies the
        attached listener if available.

        Returns:
            jsonData (dict): Latest weather data in JSON format
        '''
        stationID = next(self.pollStationCycle)
        print(f"Processing station ID: {stationID}")

        locData = self._getLocationData(stationID = stationID)

        # Request weather data from the service
        rawData = self.weatherSvc.requestCurrentWeatherData(stationID = stationID, locData = locData)
        jsonData = self.weatherSvc.getLatestWeatherDataAsJson()
        wData = self.weatherSvc.getLatestWeatherData()


        #print(f"Just retrieved weather data for station ID: {stationID}")
        print(f"Just retrieved weather data for station ID: {stationID}\n{jsonData}\n\n")
       
        # Notify listener if one is attached
        if self.dataListener:
            self.dataListener.handleIncomingWeatherData(data = wData)

        return jsonData
    
    
    def setListener(self, listener: WeatherDataListener = None):
        '''
        Sets the listener that will receive weather data updates.

        Args:
            listener (WeatherDataListener): Listener object to handle incoming data
        '''
        if listener:
            self.dataListener = listener
            
    def isClientConnected(self):
        '''
        Checks if the manager has an active client session with the weather service.

        Returns:
            bool: True if connected, False otherwise
        '''
        return self.isConnected