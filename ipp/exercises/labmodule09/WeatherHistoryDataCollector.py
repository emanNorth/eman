from collections import deque
from datetime import datetime
from threading import Lock
from typing import List, Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler

from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule06.WeatherDataListener import WeatherDataListener
from ipp.exercises.labmodule07.FileUtil import FileUtil
from ipp.exercises.labmodule07.StatsCalculationsUtil import StatsCalculationsUtil
from ipp.exercises.labmodule07.StatsData import StatsData

class WeatherHistoryDataCollector(WeatherDataListener):
    '''
    Collects, stores, and manages historical weather data.

    Uses a rolling buffer to maintain a fixed-size history and
    supports saving, loading, and analyzing weather data.
    '''
    
    def __init__(self, maxHistory: int = 50):
        '''
        Initializes the data collector with a maximum history size
        and starts a background scheduler for periodic data saving.

        Args:
            maxHistory (int): Maximum number of records to store.
        '''
        super().__init__()
        
        self.maxHistory = maxHistory
        self.dataLock = Lock()
        
        # Rolling buffer for weather history
        # deque automatically drops oldest items when maxlen is reached
        self.weatherHistory = deque(maxlen = maxHistory)
        
        # Store the most recent data for quick access
        self.latestData = None
        
        # Background scheduler for periodic tasks
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
        # Schedule periodic data save every 5 minutes
        self.scheduler.add_job(
            func = self.saveDataToFile,
            trigger = "interval",
            minutes = 5,
            id = 'save_data'
        )
        
        print(f"Weather Data Collector initialized (maxHistory = {maxHistory})")
        
        
    def saveDataToFile(self, filename: str = None):
        '''
        Saves collected weather data to a JSON file.

        Args:
            filename (str): Optional filename. If not provided,
            a timestamp-based name is generated.
        '''
        try:
            with self.dataLock:
                if not self.weatherHistory:
                    print("No data to save")
                    return
                
                # Create filename with timestamp if not provided
                if filename is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"weather_data_{timestamp}.json"
                
                # Prepare data package for saving
                data = {
                    'saved_at': datetime.now().isoformat(),
                    'record_count': len(self.weatherHistory),
                    'max_history': self.maxHistory,
                    'statistics': self.getWeatherStats(),
                    'data': list(self.weatherHistory)
                }
                
                # Save using FileUtil from Lab Module 07
                if FileUtil.writeJsonFile(filename, data, indent=2):
                    print(f"Data saved to {filename} ({data['record_count']} records)")
                else:
                    print(f"Failed to save data to {filename}")
                    
        except Exception as e:
            print(f"Error saving data: {e}")
            import traceback
            traceback.print_exc()
            
            
    def loadDataFromFile(self, filename: str) -> bool:
        '''
        Loads weather data from a file into the history buffer.

        Args:
            filename (str): File to load data from.

        Returns:
            bool: True if data was loaded successfully, otherwise False.
        '''
        try:
            # Read using FileUtil from Lab Module 07
            data = FileUtil.readTextFile(filename)
            
            if not data:
                print(f"Failed to read data from {filename}")
                return False
            
            with self.dataLock:
                # Clear existing history
                self.weatherHistory.clear()
                
                # Load historical records
                records = data.get('data', [])
                for record in records:
                    self.weatherHistory.append(record)
                
                print(f"Loaded {len(records)} records from {filename}")
                return True
                
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        
    def _processWeatherData(self, wData: WeatherData):
        '''
        Processes incoming weather data and stores it in history.

        Args:
            wData (WeatherData): Incoming weather data object.
        ''' 
        
        with self.dataLock:
            # Store the full WeatherData object for latest access
            self.latestData = wData
            
            # Convert to simplified dictionary for history storage
            # This format is easier for KNN training and analysis
            record = {
                'timestamp': datetime.now().isoformat(),
                'station': wData.location.nameID,
                'temperature': wData.temperature,
                'humidity': wData.humidity,
                'pressure': wData.pressure,
                'windSpeed': wData.wind.speedKph if wData.wind else None,
                'dewpoint': wData.dewpoint if hasattr(wData, 'dewpoint') else None
            }
            
            # Add to rolling history buffer
            self.weatherHistory.append(record)
            
            # Log the collection
            print(f"Collected data from {record['station']}: "
                  f"Temp = {record['temperature']:.1f}°C, "
                  f"Humidity = {record['humidity']:.0f}%")
            
            
    def clearHistory(self):
        '''
        Clears all stored weather history data.
        '''
        with self.dataLock:
            self.weatherHistory.clear()
            self.latestData = None
            print("Weather history cleared")    
            
    def shutdown(self):
        '''
        Stops the scheduler and saves data before shutting down.
        '''
        try:
            print("Shutting down Weather Data Collector...")
            
            # Save data before shutdown
            self.saveDataToFile()
            
            # Shutdown scheduler
            if self.scheduler.running:
                self.scheduler.shutdown(wait = False)
                print("Scheduler stopped")
            
            print("Weather Data Collector shutdown complete")
            
        except Exception as e:
            print(f"Error during shutdown: {e}")
            import traceback
            traceback.print_exc()
            
    def getLatestData(self) -> Optional[Dict]:
        '''
        Retrieves the most recent weather record.

        Returns:
            Optional[Dict]: Latest weather data or None if empty.
        '''
        with self.dataLock:
            if self.weatherHistory:
                return self.weatherHistory[-1]
            return None
        
        
    def getHistoricalData(self, count: int = 10) -> List[Dict]:
        '''
        Retrieves the most recent weather records.

        Args:
            count (int): Number of records to return.

        Returns:
            List[Dict]: List of recent weather data.
        '''
        with self.dataLock:
            # Return last 'count' records
            # Convert deque slice to list for easier handling
            if count >= len(self.weatherHistory):
                return list(self.weatherHistory)
            else:
                return list(self.weatherHistory)[-count:]
            
    def getAllHistory(self) -> List[Dict]:
        '''
        Retrieves all stored weather history.

        Returns:
            List[Dict]: Complete history data.
        '''
        with self.dataLock:
            return list(self.weatherHistory)
        
    def getHistorySize(self) -> int:
        '''
        Returns the number of stored weather records.

        Returns:
            int: Size of the history buffer.
        '''
        with self.dataLock:
            return len(self.weatherHistory)
        
        
    def getWeatherStats(self) -> Dict[str, StatsData]:
        '''
        Calculates statistics for stored weather data.

        Returns:
            Dict[str, StatsData]: Statistics for each weather metric.
        '''
        
        with self.dataLock:
            if not self.weatherHistory:
                return {}
            
            # Extract values for each metric
            temperatures = []
            humidities = []
            pressures = []
            windSpeeds = []
            
            for record in self.weatherHistory:
                if record.get('temperature') is not None:
                    temperatures.append(record['temperature'])
                if record.get('humidity') is not None:
                    humidities.append(record['humidity'])
                if record.get('pressure') is not None:
                    pressures.append(record['pressure'])
                if record.get('windSpeed') is not None:
                    windSpeeds.append(record['windSpeed'])
            
            stats = {}
            
            if temperatures:
                stats['temperature'] = StatsCalculationsUtil.calculateStats(temperatures)
            if humidities:
                stats['humidity'] = StatsCalculationsUtil.calculateStats(humidities)
            if pressures:
                stats['pressure'] = StatsCalculationsUtil.calculateStats(pressures)
            if windSpeeds:
                stats['windSpeed'] = StatsCalculationsUtil.calculateStats(windSpeeds)
            
            return stats