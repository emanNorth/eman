import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from threading import Lock
from typing import Dict

from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterDataListenerFile import WaterDataListener
from ipp.exercises.project.SimpleBubbleSortFile import SimpleBubbleSort


class LiveWaterDataClientVisualizer(WaterDataListener): 
    '''
    A visualizer that listens for incoming WaterData objects and displays
    them in real time using matplotlib.

    Stores the latest water data per station and updates a 2x2 dashboard
    showing water level, flow rate, water temperature, and a time series.
    
    Includes sort buttons to sort data by value or by station name (alphabetical).
    '''
    
    def __init__(self):
        '''
        Initialize the visualizer.
        - Creates a thread-safe storage for water data from multiple stations
        - Sets up the matplotlib figure and subplots
        - Applies initial styling to the visualization
        - Creates sort buttons for user interaction
        '''
        super().__init__()
    
        # Thread-safe storage for water data from multiple stations
        self.liveWaterDataTable: Dict[str, WaterData] = {}
        self.dataLock = Lock()
        
        # Sorting state
        self.sorter = SimpleBubbleSort()
        self.sortByValue = False  # False = sort by station name (alphabetical), True = sort by value
        self.sortReverse = False  # False = ascending, True = descending
        
        # Time series data storage (for time-bound visualization)
        self.timeSeriesData: Dict[str, list] = {}  # {stationID: [(timestamp, flowRate), ...]}
        self.maxTimeSeriesPoints = 20  # Keep last 20 readings per station
        
        # Setup the matplotlib figure and axes
        self.vizPlotFigure, self.axes = plt.subplots(2, 2, figsize=(14, 10))
        self.vizPlotFigure.suptitle('Live Water Data Dashboard - USGS NWIS', fontsize=16, fontweight='bold')
        
        # Configure the figure background
        self.vizPlotFigure.patch.set_facecolor('#f0f0f0')
        
        # Store references to bar containers for updates
        self.barContainers = {}
        
        # Initialize the visualization
        self._setupVisualization()
        
        # Setup sort buttons
        self._setupButtons()
            
    def _setupVisualization(self):
        '''
        Configure the initial appearance of each subplot.

        - Sets titles for water level, flow rate, water temperature, and time series
        - Applies background color and grid styling to each subplot
        - Adjusts layout to prevent overlap with the main title
        '''
        # Configure each subplot
        titles = ['Water Level (ft)', 'Flow Rate (cfs)', 'Water Temperature (°C)', 'Flow Rate Over Time']
        
        for ax, title in zip(self.axes.flat, titles):
            ax.set_title(title, fontweight='bold')
            ax.set_facecolor('#ffffff')
            ax.grid(True, alpha=0.3, linestyle='--')
        
        # Adjust layout to prevent overlap
        self.vizPlotFigure.tight_layout(rect=[0, 0.08, 1, 0.96])
        
    def _setupButtons(self):
        '''
        Create sort buttons for user interaction.
        
        - Sort by Value button: sorts bars by their numeric value
        - Sort by Name button: sorts bars alphabetically by station name
        - Toggle Order button: switches between ascending and descending
        '''
        # Create button axes at the bottom of the figure
        ax_sort_value = plt.axes([0.15, 0.02, 0.2, 0.04])
        ax_sort_name = plt.axes([0.40, 0.02, 0.2, 0.04])
        ax_toggle_order = plt.axes([0.65, 0.02, 0.2, 0.04])
        
        # Create buttons
        self.btnSortValue = Button(ax_sort_value, 'Sort by Value', color='#4ECDC4', hovercolor='#45B7D1')
        self.btnSortName = Button(ax_sort_name, 'Sort by Name', color='#FF6B6B', hovercolor='#FFA07A')
        self.btnToggleOrder = Button(ax_toggle_order, 'Order: Ascending', color='#95a5a6', hovercolor='#7f8c8d')
        
        # Connect button click events
        self.btnSortValue.on_clicked(self._onSortByValue)
        self.btnSortName.on_clicked(self._onSortByName)
        self.btnToggleOrder.on_clicked(self._onToggleOrder)
        
    def _onSortByValue(self, event):
        '''
        Handle Sort by Value button click.
        Sets sorting mode to sort by numeric value.
        '''
        with self.dataLock:
            self.sortByValue = True
            print("Sorting by value")
            
    def _onSortByName(self, event): 
        '''
        Handle Sort by Name button click.
        Sets sorting mode to sort alphabetically by station name.
        '''
        with self.dataLock:
            self.sortByValue = False
            print("Sorting by station name (alphabetical)")
            
    def _onToggleOrder(self, event):
        '''
        Handle Toggle Order button click.
        Switches between ascending and descending sort order.
        '''
        with self.dataLock:
            self.sortReverse = not self.sortReverse
            order_text = "Descending" if self.sortReverse else "Ascending"
            self.btnToggleOrder.label.set_text(f'Order: {order_text}')
            print(f"Sort order changed to: {order_text}")
        
    def _processWaterData(self, waData: WaterData = None):
        '''
        Store incoming WaterData in a thread-safe dictionary.

        - Uses station ID as the key
        - Adds new stations or updates existing ones with latest data
        - Maintains time series data for flow rate

        Args:
            waData (WaterData): Incoming water data object
        '''
        with self.dataLock:
            if waData:
                stationID = waData.location.siteID
                
                # Store the data indexed by station ID
                self.liveWaterDataTable[stationID] = waData
                
                # Update time series data for flow rate
                if stationID not in self.timeSeriesData:
                    self.timeSeriesData[stationID] = []
                
                # Append new reading with timestamp
                self.timeSeriesData[stationID].append({
                    'timestamp': waData.timestamp,
                    'flowRate': waData.flowRate_cfs
                })
                
                # Keep only the last N points
                if len(self.timeSeriesData[stationID]) > self.maxTimeSeriesPoints:
                    self.timeSeriesData[stationID] = self.timeSeriesData[stationID][-self.maxTimeSeriesPoints:]
                    
    def _getSortedStations(self, stations: list, values: list) -> tuple:
        '''
        Sort stations and their corresponding values based on current sort settings.
        
        Args:
            stations (list): List of station names
            values (list): List of corresponding values
            
        Returns:
            tuple: (sorted_stations, sorted_values)
        '''
        if not stations:
            return [], []
        
        # Create pairs of (station, value)
        pairs = list(zip(stations, values))
        
        if self.sortByValue:
            # Sort by value using bubble sort
            sorted_pairs = self.sorter.sortByKey(
                pairs, 
                key_func=lambda x: x[1], 
                reverse=self.sortReverse
            )
        else:
            # Sort by station name (alphabetical) using bubble sort
            sorted_pairs = self.sorter.sortByKey(
                pairs, 
                key_func=lambda x: x[0], 
                reverse=self.sortReverse
            )
        
        # Unzip back into separate lists
        sorted_stations = [p[0] for p in sorted_pairs]
        sorted_values = [p[1] for p in sorted_pairs]
        
        return sorted_stations, sorted_values
                    
    def _updateVisualization(self, frame):
        '''
        Update the dashboard with the latest water data.

        - Called repeatedly by FuncAnimation
        - Extracts data for all stations
        - Applies sorting based on user selection
        - Clears and redraws each subplot with updated bar charts and time series

        Args:
            frame: Animation frame index (provided by matplotlib, not used)
        '''
        with self.dataLock:
            if not self.liveWaterDataTable:
                return
            
            # Get current data
            stations = list(self.liveWaterDataTable.keys())
            
            # Extract metrics for each station
            waterLevels = [self.liveWaterDataTable[s].waterLevel_ft for s in stations]
            flowRates = [self.liveWaterDataTable[s].flowRate_cfs for s in stations]
            waterTemps = [self.liveWaterDataTable[s].waterTemperature_c for s in stations]
            
            # Get station names for display (using siteName instead of siteID)
            siteNames = [self.liveWaterDataTable[s].location.siteName for s in stations]
            
            # Sort data for the three bar charts
            sortedNames_level, sortedLevels = self._getSortedStations(siteNames, waterLevels)
            sortedNames_flow, sortedFlows = self._getSortedStations(siteNames, flowRates)
            sortedNames_temp, sortedTemps = self._getSortedStations(siteNames, waterTemps)
            
            # Colors for each chart
            colors = ['#3498db', '#2ecc71', '#e74c3c']
            
            # Update Water Level subplot (top-left)
            ax = self.axes[0, 0]
            ax.clear()
            if sortedLevels:
                bars = ax.bar(sortedNames_level, sortedLevels, color=colors[0], alpha=0.7, edgecolor='black')
                # Add value labels on bars
                for bar, val in zip(bars, sortedLevels):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                           f'{val:.2f}', ha='center', va='bottom', fontsize=8)
            ax.set_title('Water Level (ft)', fontweight='bold')
            ax.set_ylabel('Feet')
            ax.set_xticks(range(len(sortedNames_level)))
            ax.set_xticklabels(sortedNames_level, rotation=0, ha='right')
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Update Flow Rate subplot (top-right)
            ax = self.axes[0, 1]
            ax.clear()
            if sortedFlows:
                bars = ax.bar(sortedNames_flow, sortedFlows, color=colors[1], alpha=0.7, edgecolor='black')
                for bar, val in zip(bars, sortedFlows):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                           f'{val:.0f}', ha='center', va='bottom', fontsize=8)
            ax.set_title('Flow Rate (cfs)', fontweight='bold')
            ax.set_ylabel('Cubic Feet/Second')
            ax.set_xticks(range(len(sortedNames_flow)))
            ax.set_xticklabels(sortedNames_flow, rotation=0, ha='right')
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Update Water Temperature subplot (bottom-left)
            ax = self.axes[1, 0]
            ax.clear()
            if sortedTemps:
                bars = ax.bar(sortedNames_temp, sortedTemps, color=colors[2], alpha=0.7, edgecolor='black')
                for bar, val in zip(bars, sortedTemps):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                           f'{val:.1f}', ha='center', va='bottom', fontsize=8)
            ax.set_title('Water Temperature (°C)', fontweight='bold')
            ax.set_ylabel('Celsius')
            ax.set_xticks(range(len(sortedNames_temp)))
            ax.set_xticklabels(sortedNames_temp, rotation=0, ha='right')
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Update Time Series subplot (bottom-right) - Flow Rate Over Time
            ax = self.axes[1, 1]
            ax.clear()
            
            lineColors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6', '#f39c12']
            for idx, stationID in enumerate(stations):
                if stationID in self.timeSeriesData and self.timeSeriesData[stationID]:
                    readings = self.timeSeriesData[stationID]
                    # Use index as x-axis (time point)
                    xVals = list(range(len(readings)))
                    yVals = [r['flowRate'] for r in readings]
                    # Use siteName instead of siteID for the legend
                    siteName = self.liveWaterDataTable[stationID].location.siteName
                    color = lineColors[idx % len(lineColors)]
                    ax.plot(xVals, yVals, marker='o', label=siteName, color=color, linewidth=2, markersize=4)
            
            ax.set_title('Flow Rate Over Time (Time-Bound)', fontweight='bold')
            ax.set_xlabel('Reading Number')
            ax.set_ylabel('Flow Rate (cfs)')
            ax.legend(loc='upper left', fontsize=8)
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Update layout
            self.vizPlotFigure.tight_layout(rect=[0, 0.08, 1, 0.96])
            
    def startVisualizer(self):
        '''
        Start the live visualization.

        - Initializes the animation loop using FuncAnimation
        - Updates the display at a fixed interval (every 2 seconds)
        - Opens the matplotlib window and blocks execution until closed
        '''
        # Create animation that updates every 2 seconds (2000 ms)
        self.animation = FuncAnimation(
            self.vizPlotFigure,
            self._updateVisualization,
            interval=2000,
            cache_frame_data=False
        )
        
        # Show the window (this blocks until window is closed)
        plt.show()
            
                        
if __name__ == '__main__':
    '''
    Simple test to demonstrate the visualizer.
    In production, this would be connected to WaterServiceManager.
    '''
    import time
    from threading import Thread
    import random
    
    # Create the visualizer
    visualizer = LiveWaterDataClientVisualizer()
    
    # Simulate incoming water data
    def simulateWaterData():
        """Generate fake water data for testing"""
        from ipp.exercises.project.WaterLocationDataFile import WaterLocationData
        
        # Give plt.show() time to open the figure window
        time.sleep(2)
        
        stations = [
            ('USGS-01646500', 'Potomac River'),
            ('USGS-11455420', 'Sacramento River'),
            ('USGS-09380000', 'Colorado River')
        ]
        
        for _ in range(30):  # Send 30 updates
            for siteID, siteName in stations:
                # Create fake water data
                water = WaterData()
                water.location = WaterLocationData()
                water.location.siteID = siteID
                water.location.siteName = siteName
                water.waterLevel_ft = random.uniform(2.0, 15.0)
                water.flowRate_cfs = random.uniform(100, 5000)
                water.waterTemperature_c = random.uniform(5.0, 25.0)
                water.timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
                
                # Send to visualizer
                visualizer.handleIncomingWaterData(water)
            
            time.sleep(3)  # Update every 3 seconds
    
    # Start data simulation in background
    dataThread = Thread(target=simulateWaterData, daemon=True)
    dataThread.start()
    
    # Start the visualizer (blocks until window closed)
    visualizer.startVisualizer()