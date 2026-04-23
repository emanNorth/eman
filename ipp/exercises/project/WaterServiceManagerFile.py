import itertools
import threading
from ipp.common.ConfigUtil import ConfigUtil
from apscheduler.schedulers.background import BackgroundScheduler

from ipp.exercises.project.WaterLocationDataFile import WaterLocationData
from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.NwisWaterServiceConnectorFile import NwisWaterServiceConnector
from ipp.exercises.project.WaterDataListenerFile import WaterDataListener
from ipp.exercises.project.WaterServiceConnectorFile import WaterServiceConnector
from ipp.exercises.project.SimpleBubbleSortFile import SimpleBubbleSort


class WaterServiceManager():
    '''
    Manages water data retrieval from a configured water service asynchronously.
    
    This class acts as a "state machine" to periodically fetch water data for
    a list of water sites using the APScheduler for concurrency. Users can
    attach a listener to receive water updates in real time.
    ''' 
    def __init__(self):
        '''
        Initializes the WaterServiceManager instance.
        
        Sets up the scheduler, running state, listener, and loads properties
        from the configuration file.
        '''
        self.scheduler = BackgroundScheduler()
        self.isRunning = False
        self.dataListener = None
        self.sorter = SimpleBubbleSort()
        self.paused = False

        # Load configuration properties and initialize water service
        self._initProperties()
        
    def _initProperties(self):
        '''
        Load configuration properties from IppConfig.props and setup the
        water service connection.

        Initializes the station polling cycle based on configured station IDs.
        '''
        self.configUtil = ConfigUtil()

        self.waterSvc = NwisWaterServiceConnector()
        self.clientSession = None
        self.isConnected = False

        # Read the site IDs to poll from configuration file
        self.pollStationIDs = \
            self.configUtil.getProperty( \
                WaterServiceConnector.WATER_SVC_SECTION_NAME, "pollStationIDs")
        
        # Split comma separated station IDs into a list and trim whitespace
        self.pollStationList = [stationID.strip() for stationID in self.pollStationIDs.split(',')]
        self.pollStationCycle = None

        if self.pollStationIDs:
            print(f"Polling water site ID's: {self.pollStationIDs}")
            # Create an infinite cycle to iterate through station IDs repeatedly
            self.pollStationCycle = itertools.cycle(self.pollStationList)
        else:
            # Default to Potomac River station
            self.pollStationIDs = "USGS-01646500"
            print(f"No water site ID's defined in config file. Using default: {self.pollStationIDs}")
            
    def _scheduleAndStartWaterServiceJob(self):
        '''
        Configures the APScheduler to repeatedly call `processWaterData` at
        intervals defined by the water service's polling rate.

        Ensures only one instance runs at a time and coalesces missed runs.
        '''
        pollRate = self.waterSvc.getPollRate()
        
        # Schedule job to fetch water data at defined pollRate intervals
        self.scheduler.add_job(
            func=self.processWaterData, 
            trigger='interval',
            id=self.pollStationIDs, 
            replace_existing=True, 
            seconds=pollRate,
            max_instances=1, 
            coalesce=True, 
            misfire_grace_time=None
        )
        
        # Start the scheduler in the background
        self.scheduler.start()
    
    def startManager(self):
        '''
        Starts the water service manager.

        Connects to the water service if not already connected, schedules
        the periodic water data fetching job, and sets the running state.
        
        Returns:
            success (bool): True if manager started successfully, else False
        '''
        success = False

        if not self.isRunning:
            print("Creating water service client and connecting to service.")

            # Connect to water service if not already connected
            if not self.waterSvc.isClientConnected():
                self.waterSvc.connectToService()

            self._scheduleAndStartWaterServiceJob()

            self.isRunning = True

            print("Water station manager is now up and running!")

            success = True
        else:
            print("Client is already connected to water service!")
            success = True

        return success
    
    def stopManager(self):
        '''
        Stops the water service manager.

        Disconnects from the water service, shuts down the scheduler,
        and updates the running state.

        Returns:
            success (bool): True if manager stopped successfully, else False
        '''
        success = False

        if self.isRunning:
            print("Disconnecting from water service.")
            
            # Disconnect the water service client if connected
            if self.waterSvc.isClientConnected():
                self.waterSvc.disconnectFromService()
                
            try:
                self.scheduler.shutdown(wait=False)
                self.isRunning = False
                success = True
            except:
                print("Failed to shutdown scheduler. Probably not running.")
        else:
            print("No water service connection created! Call startManager() first.")

        return success
    
    def _getLocationData(self, siteID: str = None):
        '''
        Returns WaterLocationData for a given water site ID.

        Args:
            siteID (str): The water site ID (e.g., USGS-01646500)
        
        Returns:
            WaterLocationData: Location details of the site
        '''
        if siteID == "USGS-01646500":
            # Potomac River at Little Falls
            locData = WaterLocationData()
            locData.siteName = "Potomac River, DC"
            locData.siteID = siteID
            locData.state = "MD"
            locData.county = "Montgomery County"
            locData.country = "USA"
            locData.latitude = 0.0
            locData.longitude = 0.0
            return locData
        
        elif siteID == "USGS-11455420":
            # Sacramento River at Delta CA
            locData = WaterLocationData()
            locData.siteName = "Sacramento River, CA"
            locData.siteID = siteID
            locData.state = "CA"
            locData.county = "Sacramento County"
            locData.country = "USA"
            locData.latitude = 0.0
            locData.longitude = 0.0
            return locData
        
        elif siteID == "USGS-09380000":
            # Colorado River at Lees Ferry, AZ
            locData = WaterLocationData()
            locData.siteName = "Colorado River, AZ"
            locData.siteID = siteID
            locData.state = "AZ"
            locData.county = "Coconino County"
            locData.country = "USA"
            locData.latitude = 0.0
            locData.longitude = 0.0
            return locData
        
        else:
            # Unknown - just use siteID and zero out lat / lon
            locData = WaterLocationData()
            locData.siteName = siteID
            locData.siteID = siteID
            locData.state = "Unknown"
            locData.county = "Unknown"
            locData.country = "Unknown"
            locData.latitude = 0.0
            locData.longitude = 0.0
            return locData
        
    def processWaterData(self):
        '''
        Fetches and processes the latest water data for the next station
        in the polling cycle.

        Retrieves raw and JSON formatted water data, and notifies the
        attached listener if available.

        Returns:
            jsonData (dict): Latest water data in JSON format
        '''
        siteID = next(self.pollStationCycle)
        print(f"Processing site ID: {siteID}")

        locData = self._getLocationData(siteID=siteID)

        # Request water data from the service
        rawData = self.waterSvc.requestCurrentWaterData(siteID=siteID, locData=locData)
        jsonData = self.waterSvc.getLatestWaterDataAsJson()
        wData = self.waterSvc.getLatestWaterData()

        # Checks whether the list exists
        if not hasattr(self, "waterDataList"):
            # Create the list the first time
            self.waterDataList = []
        # Add the latest record to the list
        self.waterDataList.append(wData)
    
        print(f"Just retrieved water data for site ID: {siteID}\n{jsonData}\n\n") 
       
        # Notify listener if one is attached
        if self.dataListener and wData:
            self.dataListener.handleIncomingWaterData(data=wData)

        return jsonData
    
    def setListener(self, listener: WaterDataListener = None):
        '''
        Sets the listener that will receive water data updates.

        Args:
            listener (WaterDataListener): Listener object to handle incoming data
        '''
        if listener:
            self.dataListener = listener
            
    def isClientConnected(self):
        '''
        Checks if the manager has an active client session with the water service.

        Returns:
            bool: True if connected, False otherwise
        '''
        return self.isConnected
    
    def sortWaterData(self, field: str = "flowRate_cfs", reverse: bool = False):
        '''
        Sorts the latest retrieved water data list by a chosen field.
        Triggered by user input (e.g., via button or CLI command).

        Args:
            field (str): Field name to sort by ('flowRate_cfs', 'waterLevel_ft', 'waterTemperature_c', etc.)
            reverse (bool): True for descending order
        Returns:
            sorted list of WaterData objects
        '''
        if self.paused:
            return
        self.scheduler.pause()
        
        # Make sure the list exists AND has data
        # self.waterDataList → should contain multiple WaterData objects
        if not hasattr(self, "waterDataList") or not self.waterDataList:
            print("No water data available to sort yet.")
            return None
        
        # Notify the GUI (if it exists) that new data has arrived
        if hasattr(self, "gui_ref") and self.gui_ref:
            try:
                self.gui_ref.notifyDataReceived()
            except Exception:
                pass
        
         # Handle nested field separately
        if field == "location.siteName":
            key_func = lambda w: w.location.siteName
        else:
            key_func = lambda w: getattr(w, field)
        
        # Sort the list using bubble sort with a key function
        sorted_list = self.sorter.sortByKey(
            self.waterDataList,
            # getattr(w, field) gets the value of the chosen field dynamically
            key_func=lambda w: getattr(w, field),
            reverse=reverse
        )
        # Replace old list with sorted list
        self.waterDataList = sorted_list
        
        print(f"Data sorted by {field} {'(descending)' if reverse else '(ascending)'}:")
        
        # Print each item in readable format
        for item in self.waterDataList:
            print(f"{item.location.siteName}: {field}={getattr(item, field)}")

        self.paused = True
        
        threading.Timer(20, self.resume).start()
        
        return self.waterDataList
    
    def resume(self):
        '''
        Resumes automatic water data updates after a pause.

        Sets the internal paused flag to False so that
        processWaterData() can continue fetching new data.
        '''
        self.paused = False
        self.scheduler.resume()
