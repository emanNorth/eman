import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from threading import Lock
from typing import Dict

from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule06.WeatherDataListener import WeatherDataListener


class LiveWeatherDataClientVisualizer(WeatherDataListener):
    '''
    A visualizer that listens for incoming WeatherData objects and displays
    them in real time using matplotlib.

    Stores the latest weather data per station and updates a 2x2 dashboard
    showing temperature, humidity, wind speed, and pressure.
    '''
    
    def __init__(self):
        '''
        Initialize the visualizer.
        - Creates a thread-safe storage for weather data from multiple stations
        - Sets up the matplotlib figure and subplots
        - Applies initial styling to the visualization
        '''
        super().__init__()
    
        # Thread-safe storage for weather data from multiple stations
        # Creates an empty dictionary. Stores weather data by station name.
        self.liveWeatherDataTable: Dict[str, WeatherData] = {} 
        self.dataLock = Lock()
        
        # Setup the matplotlib figure and axes
        self.vizPlotFigure, self.axes = plt.subplots(2, 2, figsize = (12, 8))
        self.vizPlotFigure.suptitle('Live Weather Data Dashboard', fontsize = 16, fontweight = 'bold')
        
        # Configure the figure background
        self.vizPlotFigure.patch.set_facecolor('#f0f0f0')
        
        # Store references to bar containers for updates
        self.barContainers = {}
        
        # Initialize the visualization
        self._setupVisualization()
            
            
    def _setupVisualization(self):
        '''
        Configure the initial appearance of each subplot.

        - Sets titles for temperature, humidity, wind speed, and pressure
        - Applies background color and grid styling to each subplot
        - Adjusts layout to prevent overlap with the main title
        '''
        
        # Configure each subplot
        titles = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (kph)', 'Pressure (Pa)']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        for ax, title, color in zip(self.axes.flat, titles, colors):
            ax.set_title(title, fontweight = 'bold')
            ax.set_facecolor('#ffffff')
            ax.grid(True, alpha = 0.3, linestyle = '--')
        
        # Adjust layout to prevent overlap
        self.vizPlotFigure.tight_layout(rect = [0, 0, 1, 0.96])
        
        
    def _processWeatherData(self, wData: WeatherData):
        '''
        Store incoming WeatherData in a thread-safe dictionary.

        - Uses station ID as the key
        - Adds new stations or updates existing ones with latest data

        Args:
            wData (WeatherData): Incoming weather data object
        '''
        
        with self.dataLock:
            if wData:
                # Store the data indexed by station name
                self.liveWeatherDataTable[wData.location.nameID] = wData
                    
                    
    def _updateVisualization(self, frame):
        '''
        Update the dashboard with the latest weather data.

        - Called repeatedly by FuncAnimation
        - Extracts data for all stations
        - Clears and redraws each subplot with updated bar charts

        Args:
            frame: Animation frame index (provided by matplotlib, not used)
        '''
        
        with self.dataLock:
            if not self.liveWeatherDataTable:
                return
            
            # Get current data
            # Gets all station IDs from the dictionary
            stations = list(self.liveWeatherDataTable.keys())
            stations.sort()  # Sort for consistent display
    
            # Extract metrics for each station
            temps = [self.liveWeatherDataTable[s].temperature for s in stations]
            humidity = [self.liveWeatherDataTable[s].humidity for s in stations]
            windSpeed = [self.liveWeatherDataTable[s].wind.speedKph for s in stations]
            pressure = [self.liveWeatherDataTable[s].pressure for s in stations]
        
            # Update each subplot
            datasets = [temps, humidity, windSpeed, pressure]
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

            for ax, data, color in zip(self.axes.flat, datasets, colors):
                # Clears previous drawing on that subplot
                ax.clear()
                ax.bar(stations, data, color = color, alpha = 0.7, edgecolor = 'black')
                ax.set_xticks(range(len(stations)))  # Set tick positions first
                ax.set_xticklabels(stations, rotation = 45, ha = 'right')
                ax.grid(True, alpha = 0.3, linestyle = '--')

            # Reset titles after clearing
            titles = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (kph)', 'Pressure (Pa)']
            for ax, title in zip(self.axes.flat, titles):
                ax.set_title(title, fontweight = 'bold')
            
            self.vizPlotFigure.tight_layout(rect = [0, 0, 1, 0.96])
            
    def startVisualizer(self):
        '''
        Start the live visualization.

        - Initializes the animation loop using FuncAnimation
        - Updates the display at a fixed interval (e.g., every 2 seconds)
        - Opens the matplotlib window and blocks execution until closed
        '''
        
        # Create animation that updates every 2 seconds (2000 ms)
        self.animation = FuncAnimation(
            self.vizPlotFigure,
            self._updateVisualization,
            interval = 2000,
            cache_frame_data = False
        )
        
        # Show the window (this blocks until window is closed)
        plt.show()
            
                        
if __name__ == '__main__':
    '''
    Simple test to demonstrate the visualizer.
    In production, this would be connected to WeatherServiceManager.
    '''
    import time
    from threading import Thread
    
    # Create the visualizer
    visualizer = LiveWeatherDataClientVisualizer()
    
    # Simulate incoming weather data
    def simulateWeatherData():
        """Generate fake weather data for testing"""
        import random
        from ipp.exercises.labmodule05.LocationData import LocationData
        from ipp.exercises.labmodule05.WeatherInfoContainer import WindData
        
        # Gives plt.show() time to open the figure window
        time.sleep(2)  
        
        stations = ['KBOS', 'KLGA', 'KJFK']
        
        for _ in range(20):  # Send 20 updates
            for station in stations:
                # Create fake weather data
                weather = WeatherData()
                weather.location = LocationData()
                weather.location.nameID = station
                weather.temperature = random.uniform(-10, 35)
                weather.humidity = random.uniform(30, 90)
                weather.pressure = random.uniform(98000, 103000)
                weather.wind = WindData()
                weather.wind.speedKph = random.uniform(0, 50)
                
                # Send to visualizer
                visualizer.handleIncomingWeatherData(weather)
            
            time.sleep(3)  # Update every 3 seconds
    
    # Start data simulation in background
    dataThread = Thread(target = simulateWeatherData, daemon = True)
    dataThread.start()
    
    # Start the visualizer (blocks until window closed)
    visualizer.startVisualizer()