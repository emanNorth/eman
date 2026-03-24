import logging
import unittest

from ipp.exercises.labmodule08.LiveWeatherDataWebVisualizer import LiveWeatherDataWebVisualizer
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherInfoContainer import WindData


class LiveWeatherDataWebVisualizerTest(unittest.TestCase):
    '''
    Unit tests for LiveWeatherDataWebVisualizer.

    Tests:
    - Initialization
    - Adding new weather data
    - Updating existing station data
    - Handling multiple stations
    - Basic chart/stat generation
    '''

    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing LiveWeatherDataWebVisualizer...")
        
    def setUp(self):
        # Run before each test method
        pass
    
    def tearDown(self):
        # Run after each test method
        pass 

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
        vis = LiveWeatherDataWebVisualizer()

        self.assertIsNotNone(vis.liveWeatherDataTable)
        self.assertEqual(len(vis.liveWeatherDataTable), 0)
        self.assertIsNotNone(vis.webServer)
        

    def testAddWeatherData(self):
        '''
        Test adding new weather data for a station.
        '''
        vis = LiveWeatherDataWebVisualizer()
        wd = self._createSampleWeatherData("KBOS")

        vis.handleIncomingWeatherData(wd)

        self.assertIn("KBOS", vis.liveWeatherDataTable)
        

    def testUpdateWeatherData(self):
        '''
        Test updating weather data for an existing station.
        '''
        vis = LiveWeatherDataWebVisualizer()

        wd1 = self._createSampleWeatherData("KBOS", 10.0)
        wd2 = self._createSampleWeatherData("KBOS", 20.0)

        vis.handleIncomingWeatherData(wd1)
        vis.handleIncomingWeatherData(wd2)

        self.assertEqual(vis.liveWeatherDataTable["KBOS"].temperature, 20.0)
        

    def testMultipleStations(self):
        '''
        Test handling multiple stations.
        '''
        vis = LiveWeatherDataWebVisualizer()

        wd1 = self._createSampleWeatherData("KBOS")
        wd2 = self._createSampleWeatherData("KJFK")

        vis.handleIncomingWeatherData(wd1)
        vis.handleIncomingWeatherData(wd2)

        self.assertEqual(len(vis.liveWeatherDataTable), 2)
        

    def testStatsSummaryGeneration(self):
        '''
        Test that stats summary renders without errors.
        '''
        vis = LiveWeatherDataWebVisualizer()

        data = [
            self._createSampleWeatherData("KBOS", 10.0),
            self._createSampleWeatherData("KJFK", 20.0)
        ]

        summary = vis._createStatsSummary(data)

        self.assertIsNotNone(summary)

    def testChartCreation(self):
        '''
        Test chart creation does not fail.
        '''
        vis = LiveWeatherDataWebVisualizer()

        data = [
            self._createSampleWeatherData("KBOS", 10.0),
            self._createSampleWeatherData("KJFK", 20.0)
        ]

        charts = vis._createCharts(data)

        self.assertEqual(len(charts), 4)


if __name__ == '__main__':
    unittest.main()