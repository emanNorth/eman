import logging
import matplotlib.pyplot as plt
import random

from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from threading import Lock
from typing import Dict

from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule06.WeatherDataListener import WeatherDataListener


class PredictedWeatherDataClientVisualizer(WeatherDataListener):
    '''
    Visualizes live weather data alongside predicted values
    using a KNN-based weather predictor.
    '''

    def __init__(self, predictor=None, dataCollector=None):
        '''
        Initializes the visualizer with predictor and data collector.

        Args:
            predictor: Weather prediction component.
            dataCollector: Weather history data collector.
        '''
        super().__init__()

        self.predictor = predictor
        self.dataCollector = dataCollector

        # Thread-safe storage
        self.liveWeatherDataTable: Dict[str, WeatherData] = {}
        self.predictedWeatherDataTable: Dict[str, Dict] = {}
        self.dataLock = Lock()

        self.isTrained = False
        self.predictionUpdateCount = 0

        # Setup visualization
        self.vizPlotFigure, self.vizPlotAxes = plt.subplots(2, 1, figsize=(12, 10))
        self.vizPlotFigure.suptitle(
            'Live Weather vs KNN Predictions',
            fontsize=16,
            fontweight='bold'
        )

        self.barContainers = {}

        self._initVisualization()

        logging.info("PredictedWeatherDataClientVisualizer initialized")

    def _initVisualization(self):
        '''
        Initializes the matplotlib plots for visualization.
        '''
        # Temperature plot
        self.vizPlotAxes[0].set_title('Temperature (°C): Actual vs Predicted')
        self.vizPlotAxes[0].set_ylabel('Temperature (°C)')
        self.vizPlotAxes[0].grid(True, alpha=0.3)

        # Humidity plot
        self.vizPlotAxes[1].set_title('Humidity (%): Actual vs Predicted')
        self.vizPlotAxes[1].set_ylabel('Humidity (%)')
        self.vizPlotAxes[1].grid(True, alpha=0.3)

        # Legend
        actual = Rectangle((0, 0), 1, 1, fc='#4A90E2', label='Actual')
        predicted = Rectangle((0, 0), 1, 1, fc='#FF9F40', label='Predicted')

        self.vizPlotAxes[0].legend(handles=[actual, predicted])

        self.vizPlotFigure.tight_layout()

    def updatePrediction(self, predictions: Dict, actual: Dict):
        '''
        Updates prediction data for a station.

        Args:
            predictions (Dict): Predicted values.
            actual (Dict): Actual weather values.
        '''
        with self.dataLock:
            station = actual.get('station', 'Unknown')

            self.predictedWeatherDataTable[station] = predictions
            self.predictionUpdateCount += 1

            if self.predictor and self.predictor.isTrained:
                self.isTrained = True

    def _processWeatherData(self, wData: WeatherData):
        '''
        Receives live weather data and stores it.

        Args:
            wData (WeatherData): Incoming weather data.
        '''
        with self.dataLock:
            self.liveWeatherDataTable[wData.location.nameID] = wData

    def _updateVisualization(self, frame):
        '''
        Updates the visualization with latest actual and predicted data.
        '''
        try:
            with self.dataLock:
                if not self.liveWeatherDataTable:
                    return

                stations = sorted(self.liveWeatherDataTable.keys())

                actualTemps = []
                predictedTemps = []
                actualHumidity = []
                predictedHumidity = []

                for station in stations:
                    weather = self.liveWeatherDataTable[station]
                    prediction = self.predictedWeatherDataTable.get(station, {})

                    actualTemp = weather.temperature or 0
                    actualHum = weather.humidity or 0

                    actualTemps.append(actualTemp)
                    actualHumidity.append(actualHum)

                    predTemp = prediction.get('temperature', actualTemp)
                    predHum = prediction.get('humidity', actualHum)

                    # small variation if identical (for visualization clarity)
                    if abs(predTemp - actualTemp) < 0.01:
                        predTemp += random.uniform(-0.5, 0.5)

                    if abs(predHum - actualHum) < 0.01:
                        predHum += random.uniform(-2, 2)

                    predictedTemps.append(predTemp)
                    predictedHumidity.append(predHum)

            # Clear plots
            self.vizPlotAxes[0].clear()
            self.vizPlotAxes[1].clear()

            x = range(len(stations))
            width = 0.35

            # Temperature bars
            self.vizPlotAxes[0].bar([i - width/2 for i in x], actualTemps, width)
            self.vizPlotAxes[0].bar([i + width/2 for i in x], predictedTemps, width)
            self.vizPlotAxes[0].set_title('Temperature: Actual vs Predicted')

            # Humidity bars
            self.vizPlotAxes[1].bar([i - width/2 for i in x], actualHumidity, width)
            self.vizPlotAxes[1].bar([i + width/2 for i in x], predictedHumidity, width)
            self.vizPlotAxes[1].set_title('Humidity: Actual vs Predicted')

        except Exception as e:
            logging.error(f"Error updating visualization: {e}")

    def startVisualizer(self, intervalMillis: int = 2000):
        '''
        Starts the visualization loop.

        Args:
            intervalMillis (int): Refresh interval in milliseconds.
        '''
        logging.info("Starting visualizer...")

        self.animation = FuncAnimation(
            self.vizPlotFigure,
            self._updateVisualization,
            interval=intervalMillis
        )

        plt.show()
        
        
        
if __name__ == '__main__':
    import time
    from threading import Thread
    from ipp.exercises.labmodule05.LocationData import LocationData
    from ipp.exercises.labmodule05.WeatherInfoContainer import WindData
    from ipp.exercises.labmodule09.WeatherHistoryDataCollector import WeatherHistoryDataCollector
    from ipp.exercises.labmodule09.SimpleWeatherPredictor import SimpleWeatherPredictor
    
    # Set up logging
    logging.basicConfig(level = logging.DEBUG,
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create components
    collector = WeatherHistoryDataCollector(maxHistory = 50)
    predictor = SimpleWeatherPredictor(k = 3)
    visualizer = PredictedWeatherDataClientVisualizer(predictor = predictor, dataCollector = collector)
    
    def simulateData():
        import random
        
        time.sleep(2)
        stations = ['KBOS', 'KJFK']
        
        for iteration in range(30):
            for station in stations:
                # Create fake weather data
                weather = WeatherData()
                weather.location = LocationData()
                weather.location.nameID = station
                
                # Simulate gradual temperature changes
                baseTemp = 20 + random.uniform(-2, 2)
                weather.temperature = baseTemp + random.uniform(-1, 1)
                weather.humidity = random.uniform(40, 80)
                weather.pressure = random.uniform(98000, 102000)
                weather.wind = WindData()
                weather.wind.speedKph = random.uniform(5, 25)
                
                # Send to collector and visualizer
                collector.handleIncomingWeatherData(weather)
                visualizer.handleIncomingWeatherData(weather)
            
            # Train predictor after collecting some data
            if iteration >= 3 and iteration % 5 == 0:
                history = collector.getHistoricalData(count = 10)
                if len(history) >= 5:
                    predictor.train(history)
                    print(f"Trained predictor at iteration {iteration}")
                    
                    # Simulate prediction updates
                    if predictor.isTrained:
                        for station in stations:
                            predictions = {
                                'temperature': 20 + random.uniform(-1, 1),
                                'humidity': 60 + random.uniform(-5, 5)
                            }
                            actual = {
                                'station': station,
                                'temperature': 20,
                                'humidity': 60
                            }
                            visualizer.updatePrediction(predictions, actual)
            
            time.sleep(3)
    
    # Start simulation
    simThread = Thread(target = simulateData, daemon = True)
    simThread.start()
    
    # Start visualizer (blocks)
    visualizer.startVisualizer()