import logging
import unittest
from datetime import datetime

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherInfoContainer import WindData, VisibilityData, CloudLayerData
from ipp.exercises.labmodule05.WeatherData import WeatherData


class WeatherAndLocationDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing WeatherData class...")

    def setUp(self):
        # Run before each test method.
        pass

    def tearDown(self):
        # Run after each test method,
        pass
     
    # WeatherData Default Values
    def testWeatherDataContainerDefaultValues(self):
        # Creates a weather data object with all defults values.
        wData = WeatherData()
        # Get the current timestamp in ISO8601 format.
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
        
        # Checks that all defalut attributes have the expected value
        self.assertEqual(wData.source, "")
        self.assertEqual(wData.url, "")
        self.assertEqual(wData.description, "")

        self.assertEqual(wData.temperature, 0.0)
        self.assertEqual(wData.humidity, 0.0)
        self.assertEqual(wData.pressure, 0.0)
        self.assertEqual(wData.windspeed, 0.0)

        timestampA = datetime.fromisoformat(wData.timestamp).timestamp()
        timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
        self.assertAlmostEqual(timestampA, timestampB, delta=5.0)

        # Checks that the nested object exist.
        self.assertIsNotNone(wData.location)
        self.assertIsNotNone(wData.wind)
        self.assertIsNotNone(wData.visibility)
        # Confirms that cloudlayer starts as an empty list.
        self.assertEqual(len(wData.cloudLayers), 0)
     
    # WeatherData Custom Values
    def testWeatherDataContainerCustomValues(self):
        wData = WeatherData()
        locData = LocationData()
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()

        # Assign custom values to the weatherData object.
        wData.source = "test"
        wData.url = "https://www.example.com"
        wData.description = "My weather site."
        wData.timestamp = isoTimeDate
        wData.temperature = 15.0
        wData.humidity = 45.0
        wData.pressure = 1005.0
        wData.windspeed = 5.0
        wData.location = locData

        # Verify all custom values stored correctly.
        self.assertEqual(wData.source, "test")
        self.assertEqual(wData.url, "https://www.example.com")
        self.assertEqual(wData.description, "My weather site.")
        self.assertEqual(wData.timestamp, isoTimeDate)

        self.assertEqual(wData.temperature, 15.0)
        self.assertEqual(wData.humidity, 45.0)
        self.assertEqual(wData.pressure, 1005.0)
        self.assertEqual(wData.windspeed, 5.0)
        self.assertEqual(wData.location, locData)


    # LocationData Default Values
    def testLocationDataContainerDefaultValues(self):
        locData = LocationData()
        self.assertEqual(locData.name, "")
        self.assertEqual(locData.nameID, "")
        self.assertEqual(locData.city, "")
        self.assertEqual(locData.region, "")
        self.assertEqual(locData.country, "")
        self.assertEqual(locData.latitude, 0.0)
        self.assertEqual(locData.longitude, 0.0)
        self.assertEqual(locData.elevation, 0.0)

    # LocationData Custom Values
    def testLocationDataContainerCustomValues(self):
        locData = LocationData()
        locData.name = "My Location"
        locData.nameID = "LOC001"
        locData.city = "Boston"
        locData.region = "MA"
        locData.country = "USA"
        locData.latitude = 42.36
        locData.longitude = -71.06
        locData.elevation = 12.0
        
        # Verify all custom values stored correctly.
        self.assertEqual(locData.name, "My Location")
        self.assertEqual(locData.nameID, "LOC001")
        self.assertEqual(locData.city, "Boston")
        self.assertEqual(locData.region, "MA")
        self.assertEqual(locData.country, "USA")
        self.assertEqual(locData.latitude, 42.36)
        self.assertEqual(locData.longitude, -71.06)
        self.assertEqual(locData.elevation, 12.0)





