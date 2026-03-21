
import logging
import unittest
import tempfile
import os

from ipp.exercises.labmodule07.DataConverterUtil import DataConverterUtil
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule07.StatsData import StatsData
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherInfoContainer import CloudLayerData, VisibilityData, WindData

class DataConverterUtilTest(unittest.TestCase):
    '''
    Tests Unit tests for the DataConverterUtil class.
    Tests conversion between objects and JSON, and file operations.
    
    Tests conversion of WeatherData and StatsData objects to and from JSON,
    and reading and writing these objects to files.
    '''
    
    # Set system temporary directory for creating test files
    TEST_PATH = tempfile.gettempdir()
    # The filename used for all temporary test files
    TEST_FILE = "IppTestFile.txt"
    
    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing DataConverterUtil class...")
        
    def setUp(self):
        # Run before each test method
        pass 
    
    def tearDown(self):
        # Run after each test method
        pass
    
    def _createTestFileName(self) -> str:
        '''
        Creates the full path for the temporary test file.

        Returns:
            str: Full path to the test file in the system temp directory.
        '''
        
        # Combines temporary folder path and test file name
        fileName = os.path.join(tempfile.gettempdir(), DataConverterUtilTest.TEST_FILE)
        return fileName
    
    def _createSampleWeatherData(self) -> WeatherData:
        '''
        Creates a WeatherData object with sample nested data.

        Returns:
            WeatherData: Populated WeatherData object.
        '''
        
        wd = WeatherData()
        wd.source = "TestSource"
        wd.url = "http://test.com"
        wd.description = "Sunny"
        wd.temperature = 25.5
        wd.humidity = 60.0
        wd.pressure = 1012.0
        wd.windspeed = 5.5
        wd.conditions = "Clear"
        wd.icon = "sunny"

        # Location
        loc = LocationData()
        loc.name = "Test Location"
        loc.latitude = 42.0
        loc.longitude = -71.0
        wd.location = loc

        # Wind
        wind = WindData()
        wind.speed = 5.5
        wd.wind = wind

        # Visibility
        vis = VisibilityData()
        vis.distance = 10000
        wd.visibility = vis

        # Cloud layers
        cloud = CloudLayerData()
        cloud.coverage = "Few"
        wd.cloudLayers = [cloud]

        return wd

      
    def _createSampleStatsData(self) -> StatsData:
        '''
        Creates a StatsData object with sample data.

        Returns:
            StatsData: Populated StatsData object.
        '''
        stats = StatsData()
        stats.count = 5
        stats.mean = 10.0
        stats.median = 9.0
        stats.min = 2.0
        stats.max = 20.0
        stats.standardDeviation = 3.5
        return stats
    
    def testWeatherDataToJson(self):
        '''
        Test converting WeatherData object to JSON string.
        '''
        wd = self._createSampleWeatherData()
        json_str = DataConverterUtil.weatherDataToJson(wd)

        self.assertIsInstance(json_str, str)
        self.assertIn("TestSource", json_str)
        
    
    def testJsonToWeatherData(self):
        '''
        Test converting JSON string to WeatherData object.
        '''
        
        wd = self._createSampleWeatherData()
        json_str = DataConverterUtil.weatherDataToJson(wd)

        new_wd = DataConverterUtil.jsonToWeatherData(json_str)

        self.assertIsNotNone(new_wd)
        self.assertEqual(new_wd.source, wd.source)
        self.assertEqual(new_wd.location.name, wd.location.name)
        self.assertEqual(len(new_wd.cloudLayers), 1)
        
        
    def testStatsDataToJson(self):
        '''
        Test converting StatsData object to JSON string.
        '''
        stats = self._createSampleStatsData()
        json_str = DataConverterUtil.statsDataToJson(stats)
        
        self.assertIsInstance(json_str, str)
        self.assertIn("mean", json_str)
        
    
    def testJsonToStatsData(self):
        '''
        Test converting JSON string to StatsData object.
        '''
       
        stats = self._createSampleStatsData()
        json_str = DataConverterUtil.statsDataToJson(stats)

        new_stats = DataConverterUtil.jsonToStatsData(json_str)

        self.assertIsNotNone(new_stats)
        self.assertEqual(new_stats.mean, stats.mean)
        self.assertEqual(new_stats.max, stats.max)
        
    
    def testWriteStatsDataToFile(self):
        '''
        test Converting StatsData to JSON and write to a file.
        '''
        fileName = self._createTestFileName()
        stats = self._createSampleStatsData()

        result = DataConverterUtil.writeStatsDataToFile(stats, fileName)
        self.assertTrue(result)

    
    def testReadStatsDataFromFile(self):
        '''
        test Reading JSON from file and converting it to a StatsData object.
        '''

        fileName = self._createTestFileName()
        stats = self._createSampleStatsData()

        DataConverterUtil.writeStatsDataToFile(stats, fileName)
        loaded = DataConverterUtil.readStatsDataFromFile(fileName)

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.mean, stats.mean)
    
    def testWriteWeatherDataToFile(self):
        '''
        test Converting WeatherData to JSON and write to a file.
        '''
       
        fileName = self._createTestFileName()
        wd = self._createSampleWeatherData()

        result = DataConverterUtil.writeWeatherDataToFile(wd, fileName)
        self.assertTrue(result)
    
    def testReadWeatherDataFromFile(self):
        '''
        test Reading JSON from file and converting it to a WeatherData object.
        '''
        fileName = self._createTestFileName()
        wd = self._createSampleWeatherData()

        DataConverterUtil.writeWeatherDataToFile(wd, fileName)
        loaded = DataConverterUtil.readWeatherDataFromFile(fileName)

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.source, wd.source)
        self.assertEqual(loaded.location.name, wd.location.name)
    
    
    
    

    
        
    