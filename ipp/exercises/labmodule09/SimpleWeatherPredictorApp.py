import argparse
import logging
import traceback
import random
import math
from time import sleep
from threading import Thread

from ipp.common.ConfigUtil import ConfigUtil
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherInfoContainer import WindData
from ipp.exercises.labmodule06.WeatherServiceManager import WeatherServiceManager
from ipp.exercises.labmodule09.WeatherHistoryDataCollector import WeatherHistoryDataCollector
from ipp.exercises.labmodule09.PredictedWeatherDataClientVisualizer import PredictedWeatherDataClientVisualizer
from ipp.exercises.labmodule09.SimpleWeatherPredictor import SimpleWeatherPredictor
# from ipp.exercises.labmodule10.WeatherDataAggregator import WeatherDataAggregator

LOG_FORMAT = "%(asctime)s:::%(thread)d:%(name)s.%(module)s.%(funcName)s()[%(lineno)s]:%(levelname)s:%(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)


class SimpleWeatherPredictorApp():
    '''
    Main application class to run weather prediction simulation
    or live weather data collection and visualization.
    '''

    def __init__(self):
        '''
        Initializes the Weather Predictor App with simulation or live mode.
        Sets up collector, predictor, visualizer, and optional weather service.
        '''
        logging.info("Initializing Weather Predictor App...")

        configUtil = ConfigUtil()

        # TODO: use the config file (IppConfig.props) to pull properties:
        #  - maxHistory
        #  - value of k
        #  - bool for useSim
        self.useSim = True
        self.maxHistory = 50
        self.k = 3

        # Core components
        self.collector = WeatherHistoryDataCollector(maxHistory=self.maxHistory)
        self.predictor = SimpleWeatherPredictor(k=self.k)
        self.visualizer = PredictedWeatherDataClientVisualizer(
            predictor=self.predictor, dataCollector=self.collector)

        # Weather service components (for non-simulation mode)
        if not self.useSim:
            self.wsManager = WeatherServiceManager()
            # Create aggregator to distribute data
            self.aggregator = WeatherDataAggregator(
                collector=self.collector,
                visualizer=self.visualizer
            )
            # Register aggregator as listener
            self.wsManager.setListener(self.aggregator)
        else:
            self.wsManager = None
            self.aggregator = None

        # Thread control
        self.predictionThread = None
        self.predictionRunning = False
        self.simulationThread = None
        self.simulationRunning = False

        self.isStarted = False

    def isAppStarted(self) -> bool:
        '''
        Returns whether the application has been started.
        '''
        return self.isStarted

    def startApp(self):
        '''
        Starts the Weather Predictor App, including simulation or live data,
        prediction loop, and visualization.
        '''
        if not self.isStarted:
            logging.info("Starting Weather Predictor App...")

            # Start data collection
            if self.useSim:
                logging.info("Starting in SIMULATION mode")
                self.simulationRunning = True
                self.simulationThread = Thread(
                    target=self._runSimulation,
                    daemon=True
                )
                self.simulationThread.start()
            else:
                logging.info("Starting in LIVE DATA mode")
                if self.wsManager and self.wsManager.startManager():
                    logging.info("Weather service manager started")
                else:
                    logging.error("Failed to start weather service manager")
                    return

            # Start prediction loop
            self.predictionRunning = True
            self.predictionThread = Thread(
                target=self._runPredictionLoop,
                daemon=True
            )
            self.predictionThread.start()
            logging.info("Prediction thread started")

            # Mark as started
            self.isStarted = True

            # Start visualizer (blocking call)
            logging.info("Starting visualizer...")
            self.visualizer.startVisualizer()

            logging.info("Weather Predictor App started.")
        else:
            logging.info("Weather Predictor App already started.")

    def stopApp(self, code: int):
        '''
        Stops the Weather Predictor App, including simulation, prediction, 
        and live data threads.
        '''
        if self.isStarted:
            logging.info("Weather Predictor App stopping...")

            if self.predictionRunning:
                logging.info("Stopping prediction thread...")
                self.predictionRunning = False
                if self.predictionThread:
                    self.predictionThread.join(timeout=2)

            if self.simulationRunning:
                logging.info("Stopping simulation thread...")
                self.simulationRunning = False
                if self.simulationThread:
                    self.simulationThread.join(timeout=2)

            if self.wsManager:
                self.wsManager.stopManager()

            self.isStarted = False
            logging.info("Weather Predictor App stopped with exit code %s.", str(code))
        else:
            logging.info("Weather Predictor App not yet started.")

    def _runPredictionLoop(self):
        '''
        Runs the continuous prediction loop for training and generating predictions.
        Updates the visualizer with predictions.
        '''
        logging.info("Prediction loop started")
        sleepCounter = 0

        while self.predictionRunning:
            sleep(1)
            sleepCounter += 1

            if sleepCounter % 30 == 0:
                history = self.collector.getHistoricalData(count=20)
                if len(history) >= 5:
                    logging.info(f"Training predictor with {len(history)} samples...")
                    success = self.predictor.train(history)
                    if success:
                        logging.info("Predictor training complete")
                        if hasattr(self.visualizer, 'isTrained'):
                            self.visualizer.isTrained = True

            if sleepCounter % 10 == 0 and self.predictor.isTrained:
                recentData = self.collector.getHistoricalData(count=2)
                if len(recentData) >= 2:
                    predictions = self.predictor.predict(recentData)
                    if predictions:
                        temp = predictions.get('temperature')
                        humidity = predictions.get('humidity')
                        if temp is not None and humidity is not None:
                            logging.info(f"Prediction: Temp={temp:.1f}°C, Humidity={humidity:.0f}%")
                        if hasattr(self.visualizer, 'updatePrediction'):
                            with self.visualizer.dataLock:
                                stations = list(self.visualizer.liveWeatherDataTable.keys())
                            for station in stations:
                                actual = {
                                    'station': station,
                                    'temperature': recentData[-1].get('temperature'),
                                    'humidity': recentData[-1].get('humidity')
                                }
                                self.visualizer.updatePrediction(predictions, actual)
                                logging.debug(f"Updated predictions for station {station}")
                        else:
                            logging.warning("Visualizer doesn't have updatePrediction method")

    def _runSimulation(self):
        '''
        Runs simulated weather data for testing, generating random temperature,
        humidity, pressure, and wind speed values.
        '''
        logging.info("Starting weather simulation...")
        stations = ['KBOS', 'KJFK', 'KLAX']

        stationData = {
            'KBOS': {'baseTemp': 15, 'baseHumidity': 65},
            'KJFK': {'baseTemp': 18, 'baseHumidity': 70},
            'KLAX': {'baseTemp': 22, 'baseHumidity': 55}
        }

        iteration = 0
        while self.simulationRunning:
            iteration += 1
            for station in stations:
                weather = WeatherData()
                weather.location = LocationData()
                weather.location.nameID = station

                baseTemp = stationData[station]['baseTemp']
                baseHumidity = stationData[station]['baseHumidity']
                seasonalTemp = 5 * math.sin(iteration * 0.1)

                weather.temperature = baseTemp + seasonalTemp + random.uniform(-2, 2)
                weather.humidity = baseHumidity + random.uniform(-10, 10)
                weather.pressure = random.uniform(98000, 102000)
                weather.wind = WindData()
                weather.wind.speedKph = random.uniform(5, 30)

                self.collector.handleIncomingWeatherData(weather)
                self.visualizer.handleIncomingWeatherData(weather)
                logging.debug(f"Simulated data for {station}: Temp={weather.temperature:.1f}°C")

            sleep(5)


def main():
    '''
    Main entry point for the Weather Predictor App. Parses arguments and starts
    the application in simulation or live mode.
    '''
    argParser = argparse.ArgumentParser(
        description='Weather Predictor App for testing weather predictions as part of the Intro to Python Programming course.')

    argParser.add_argument('-c', '--configFile', help='Optional custom configuration file for the Weather Predictor App.')
    configFile = None

    try:
        args = argParser.parse_args()
        configFile = args.configFile
        logging.info('Parsed configuration file arg: %s', configFile)
    except:
        logging.info('No arguments to parse.')

    configUtil = ConfigUtil(configFile)
    wpa = None

    try:
        wpa = SimpleWeatherPredictorApp()
        wpa.startApp()
        while True:
            print("App is running forever - with 5 second pauses...")
            sleep(5)

    except KeyboardInterrupt:
        logging.warning('Keyboard interruption for Weather Predictor App. Exiting.')
        if wpa:
            wpa.stopApp(-1)

    except Exception as e:
        logging.error('Startup exception caused Weather Predictor App to fail. Exiting.')
        traceback.print_exception(type(e), e, e.__traceback__)
        if wpa:
            wpa.stopApp(-2)

    logging.info('Exiting Weather Predictor App.')
    exit()


if __name__ == '__main__':
    main()