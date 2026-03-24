import logging
import unittest

import matplotlib.pyplot as plt

from ipp.exercises.labmodule08.LiveWeatherDataClientVisualizer import LiveWeatherDataClientVisualizer
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherInfoContainer import WindData


class LiveWeatherDataClientVisualizerTest(unittest.TestCase):
    '''
    Unit tests for LiveWeatherDataClientVisualizer.

    Tests:
    - Initialization
    - Adding new weather data
    - Updating existing station data
    - Handling multiple stations
    '''

    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing LiveWeatherDataClientVisualizer...")
        
    def setUp(self):
        # Run before each test method
        pass 
    
    def tearDown(self):
        # Close all figures after each test
        plt.close('all')  

    def _createSampleWeatherData(self, station_id: str, temp: float = 25.0) -> WeatherData:
        '''
        Creates a simple WeatherData object for testing.

        Args:
            station_id (str): Station identifier
            temp (float): Temperature value

        Returns:
            WeatherData: Populated object
        '''
        wd = WeatherData()
        wd.location = LocationData()
        wd.location.nameID = station_id
        wd.temperature = temp
        wd.humidity = 50.0
        wd.pressure = 100000.0

        wd.wind = WindData()
        wd.wind.speedKph = 10.0

        return wd
    

    def testVisualizerInitialization(self):
        '''
        Test that visualizer initializes correctly.
        '''
        vis = LiveWeatherDataClientVisualizer()
        # Checks the dictionary exists (not None)
        self.assertIsNotNone(vis.liveWeatherDataTable)
        # Checks it starts empty (len = 0)
        self.assertEqual(len(vis.liveWeatherDataTable), 0)
        

    def testAddWeatherData(self):
        '''
        Test adding new weather data for a station.
        '''
        vis = LiveWeatherDataClientVisualizer()
        wd = self._createSampleWeatherData("KBOS")

        vis.handleIncomingWeatherData(wd)

        self.assertIn("KBOS", vis.liveWeatherDataTable)
        

    def testUpdateWeatherData(self):
        '''
        Test updating weather data for an existing station.
        '''
        vis = LiveWeatherDataClientVisualizer()

        wd1 = self._createSampleWeatherData("KBOS", 10.0)
        wd2 = self._createSampleWeatherData("KBOS", 20.0)

        vis.handleIncomingWeatherData(wd1)
        vis.handleIncomingWeatherData(wd2)

        self.assertEqual(vis.liveWeatherDataTable["KBOS"].temperature, 20.0)
        

    def testMultipleStations(self):
        '''
        Test storing weather data for multiple stations.
        '''
        vis = LiveWeatherDataClientVisualizer()

        wd1 = self._createSampleWeatherData("KBOS")
        wd2 = self._createSampleWeatherData("KJFK")

        vis.handleIncomingWeatherData(wd1)
        vis.handleIncomingWeatherData(wd2)

        self.assertEqual(len(vis.liveWeatherDataTable), 2)


if __name__ == '__main__':
    unittest.main()