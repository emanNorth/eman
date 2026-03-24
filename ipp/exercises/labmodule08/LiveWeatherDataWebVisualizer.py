import dash
import plotly.graph_objs as go

from dash import dcc, html
from dash.dependencies import Input, Output

from threading import Lock
from typing import Dict, List

from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule06.WeatherDataListener import WeatherDataListener


class LiveWeatherDataWebVisualizer(WeatherDataListener):
    '''
    A visualizer that listens for incoming WeatherData objects and displays
    them in real time from multiple stations using Dash and Plotly.
    
   Stores the latest weather data per station, and renders updated
    charts and statistics in a web browser.
    '''

    COLORS = {
        'background': '#1a1a2e',
        'card': '#16213e',
        'text': '#ffffff',
        'accent': '#0f4c75',
        'temperature': '#e94560',
        'humidity': '#3fc1c9',
        'wind': '#fc5185',
        'pressure': '#364f6b'
    }
 
    def __init__(self, host: str = '127.0.0.1', port: int = 8050):
        '''
        Initializes the web visualizer.
        
        - Sets up the Dash web server
        - Creates a thread-safe storage for weather data from multiple stations
        - Configures the layout and callbacks for dynamic updates.

        Args:
            host (str): The host address where the web server will run (default is localhost).
            port (int): The port number for the web server (default is 8050).
        '''
        super().__init__()
        
        # Server configuration
        self.host = host
        self.port = port
        
        # Thread-safe storage for weather data from multiple stations
        self.liveWeatherDataTable: Dict[str, WeatherData] = {}
        self.dataLock = Lock()
        
        # Create the Dash application
        self.webServer = dash.Dash(__name__)
        self.webServer.title = 'Live Weather Dashboard'
        
        # Setup the layout and callbacks
        self._setupLayout()
        self._setupCallbacks()
        
        
    def _setupLayout(self):
        '''
        Defines the layout of the web dashboard.

        Creates the main page structure including header,
        statistics section, charts container, and update interval.
        '''
        
        self.webServer.layout = html.Div(
            style = {'backgroundColor': self.COLORS['background'], 'minHeight': '100vh', 'padding': '20px'},
            children = [
                # Header
                html.H1(
                    'Live Weather Data Dashboard',
                    style = {
                        'textAlign': 'center',
                        'color': self.COLORS['text'],
                        'marginBottom': '30px',
                        'fontFamily': 'Arial, sans-serif'
                    }
                ),
                
                # Statistics summary
                html.Div(id = 'stats-summary', style = {'marginBottom': '20px'}),
                
                # Charts container
                html.Div(
                    id = 'charts-container',
                    style = {'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '20px'}
                ),
                
                # Interval component for automatic updates every 2 seconds
                dcc.Interval(
                    id = 'interval-component',
                    interval = 2000,  # Update every 2000ms (2 seconds)
                    n_intervals = 0
                )
            ]
        )
    
    
    def _setupCallbacks(self):
        '''
        Sets up dashboard updates.

        Triggers updateDashboard() every interval.
        Updates stats section and charts using current weather data.
        '''
        
        # # This function is triggered every 2 seconds by the Interval component
        # It updates the dashboard with the latest weather data
        @self.webServer.callback(
            [Output('stats-summary', 'children'),
             Output('charts-container', 'children')],
            [Input('interval-component', 'n_intervals')]
        )

        def updateDashboard(n):
            with self.dataLock:
                if not self.liveWeatherDataTable:
                    # If no weather data is available yet, show the default "Waiting for data" message
                    return self._createEmptyState()
                
                # Get current data
                # Convert dictionary of WeatherData objects to a list
                weatherList = list(self.liveWeatherDataTable.values())
                # Sorts the list by the station name inside each WeatherData object.
                weatherList.sort(key = lambda w: w.location.nameID)
                
                # Create statistics summary
                statsSummary = self._createStatsSummary(weatherList)
                
                # Create charts
                charts = self._createCharts(weatherList)
                
                return statsSummary, charts
            
            
    def _createEmptyState(self):
        '''
        Creates a placeholder view when no weather data is available yet.

        Returns:
            Tuple: A message div and an empty chart list
        '''
        emptyMessage = html.Div(
            'Waiting for weather data...',
            style = {
                'textAlign': 'center',
                'color': self.COLORS['text'],
                'fontSize': '20px',
                'padding': '50px'
            }
        )
        return emptyMessage, []
    
    
    def _createStatsSummary(self, weatherList: List[WeatherData]):
        '''
        Generates a summary section displaying aggregate weather statistics.

        Calculates averages for temperature, humidity, and wind speed,
        along with total station count.

        Args:
            weatherList (List[WeatherData]): List of weather data objects

        Returns:
            html.Div: Dashboard summary section
        '''
        # Calculate averages
        avgTemp = sum(w.temperature for w in weatherList) / len(weatherList)
        avgHumidity = sum(w.humidity for w in weatherList) / len(weatherList)
        avgWind = sum(w.wind.speedKph for w in weatherList) / len(weatherList)
        stationCount = len(weatherList)
        
        return html.Div(
            style = {'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '15px'},
            children = [
                self._createStatCard('Stations', f'{stationCount}', self.COLORS['accent']),
                self._createStatCard('Avg Temp', f'{avgTemp:.1f}°C', self.COLORS['temperature']),
                self._createStatCard('Avg Humidity', f'{avgHumidity:.0f}%', self.COLORS['humidity']),
                self._createStatCard('Avg Wind', f'{avgWind:.1f} kph', self.COLORS['wind'])
            ]
        )
        
    def _createStatCard(self, title: str, value: str, color: str):
        '''
        Creates a styled card displaying a single statistic.

        Args:
            title (str): Label of the statistic
            value (str): Value to display
            color (str): Accent color for the card

        Returns:
            html.Div: Styled stat card component
        '''
        return html.Div(
            style = {
                'backgroundColor': self.COLORS['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'borderLeft': f'4px solid {color}',
                'textAlign': 'center'
            },
            children = [
                html.H3(
                    title,
                    style = {'color': self.COLORS['text'], 'fontSize': '14px', 'marginBottom': '10px'}
                ),
                html.H2(
                    value,
                    style = {'color': color, 'fontSize': '28px', 'margin': '0'}
                )
            ]
        )  
        
        
    def _createCharts(self, weatherList: List[WeatherData]):
        '''
        Generates all chart components for the dashboard.

        Creates bar charts for temperature, humidity,
        wind speed, and pressure across stations.

        Args:
            weatherList (List[WeatherData]): List of weather data

        Returns:
            List: List of Dash graph components
        '''
        stations = [w.location.nameID for w in weatherList]
        
        # Create four charts
        charts = [
            self._createChart( \
                'Temperature (°C)', stations, 
                [w.temperature for w in weatherList], self.COLORS['temperature']),
            self._createChart( \
                'Humidity (%)', stations,
                [w.humidity for w in weatherList], self.COLORS['humidity']),
            self._createChart( \
                'Wind Speed (kph)', stations,
                [w.wind.speedKph for w in weatherList], self.COLORS['wind']),
            self._createChart( \
                'Pressure (Pa)', stations,
                [w.pressure for w in weatherList], self.COLORS['pressure'])
        ]
        
        return charts 
    
    
    def _createChart(self, title: str, stations: List[str], values: List[float], color: str):
        '''
        Creates a single bar chart for a weather metric.

        Args:
            title (str): Chart title
            stations (List[str]): Station identifiers
            values (List[float]): Metric values
            color (str): Bar color

        Returns:
            dcc.Graph: Plotly graph component
        '''
        figure = go.Figure(
            data = [
                go.Bar(
                    x = stations,
                    y = values,
                    marker_color = color,
                    hovertemplate = '<b>%{x}</b><br>%{y:.1f}<extra></extra>'
                )
            ]
        )
        
        figure.update_layout(
            title = title,
            paper_bgcolor = self.COLORS['card'],
            plot_bgcolor = self.COLORS['card'],
            font = dict(color = self.COLORS['text']),
            margin = dict(t = 40, b = 40, l = 40, r = 40),
            xaxis = dict(showgrid = False),
            yaxis = dict(showgrid = True, gridcolor = 'rgba(255,255,255,0.1)')
        )
        
        return dcc.Graph(figure = figure, config = {'displayModeBar': False})
        
    def _processWeatherData(self, wData: WeatherData):
        '''
        Store incoming WeatherData in a thread-safe dictionary.

        - Uses station ID as the key
        - Adds new stations or updates existing ones with latest data

        Args:
            wData (WeatherData): Incoming weather data object
        '''
        
        with self.dataLock:
            # Store the data indexed by station name
            self.liveWeatherDataTable[wData.location.nameID] = wData   
        
        
    def startVisualizer(self):
        '''
        Starts the Dash web server for the weather dashboard.

        This method blocks execution until the server is stopped.
        '''
        # Print info to the console so the user knows where to open the browser
        print(f"\nStarting web visualizer at http://{self.host}:{self.port}/")
        print("Press CTRL+C to stop the server\n")
        
        # Run the Dash server
        self.webServer.run(
            host = self.host,
            port = self.port,
            debug = False, # Turn off debug mode so errors aren't shown in interactive mode
            use_reloader = False  # Disable reloader to prevent issues with threads
        )    
        
        
    # Example usage for testing
if __name__ == '__main__':
    """
    Simple test to demonstrate the visualizer.
    In production, this would be connected to WeatherServiceManager.
    """
    import time
    from threading import Thread
    
    # Create the visualizer
    visualizer = LiveWeatherDataWebVisualizer()
    
    # Simulate incoming weather data
    def simulateWeatherData():
        """Generate fake weather data for testing"""
        import random
        from ipp.exercises.labmodule05.LocationData import LocationData
        from ipp.exercises.labmodule05.WeatherInfoContainer import WindData
        
        time.sleep(3)  # Wait for server to start
        
        stations = ['KBOS', 'KLGA', 'KJFK']
        
        while True:
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
    
    # Start the web server (blocks until stopped with CTRL+C)
    visualizer.startVisualizer()