import logging
import unittest
from datetime import datetime

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData


class WaterAndLocationDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing WaterData class...")

    def setUp(self):
        # Run before each test method.
        pass

    def tearDown(self):
        # Run after each test method,
        pass
     
    # WaterData Default Values
    def testWaterDataContainerDefaultValues(self):
        # Creates a water data object with all defults values.
        wData = WaterData()
        # Get the current timestamp in ISO8601 format.
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
        
        # Checks that all defalut attributes have the expected value
        self.assertEqual(wData.source, "")
        self.assertEqual(wData.url, "")
        self.assertEqual(wData.description, "")

        self.assertEqual(wData.waterLevel_ft, 0.0)
        self.assertEqual(wData.flowRate_cfs, 0.0)
        self.assertEqual(wData.waterTemperature_c, 0.0)

        self.assertEqual(wData.variable, "")
        self.assertEqual(wData.qualifier, "")
        self.assertEqual(wData.unit, "")

        timestampA = datetime.fromisoformat(wData.timestamp).timestamp()
        timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
        self.assertAlmostEqual(timestampA, timestampB, delta=5.0)

        # Checks that the nested object exist.
        self.assertIsNotNone(wData.location)
     
    # WaterData Custom Values
    def testWaterDataContainerCustomValues(self):
        wData = WaterData()
        locData = WaterLocationData()
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()

        # Assign custom values to the waterData object.
        wData.source = "test"
        wData.url = "https://www.example.com"
        wData.description = "My water site."
        wData.timestamp = isoTimeDate

        wData.waterLevel_ft = 10.0
        wData.flowRate_cfs = 20.0
        wData.waterTemperature_c = 5.0

        wData.variable = "flowRate"
        wData.qualifier = "Approved"
        wData.unit = "ft^3/s"

        wData.location = locData

        # Verify all custom values stored correctly.
        self.assertEqual(wData.source, "test")
        self.assertEqual(wData.url, "https://www.example.com")
        self.assertEqual(wData.description, "My water site.")
        self.assertEqual(wData.timestamp, isoTimeDate)

        self.assertEqual(wData.waterLevel_ft, 10.0)
        self.assertEqual(wData.flowRate_cfs, 20.0)
        self.assertEqual(wData.waterTemperature_c, 5.0)

        self.assertEqual(wData.variable, "flowRate")
        self.assertEqual(wData.qualifier, "Approved")
        self.assertEqual(wData.unit, "ft^3/s")
        self.assertEqual(wData.location, locData)

    # WaterLocationData Default Values
    def testWaterLocationDataContainerDefaultValues(self):
        locData = WaterLocationData()
        self.assertEqual(locData.siteName, "")
        self.assertEqual(locData.siteID, "")
        self.assertEqual(locData.county, "")
        self.assertEqual(locData.state, "")
        self.assertEqual(locData.country, "")
        self.assertEqual(locData.latitude, 0.0)
        self.assertEqual(locData.longitude, 0.0)
        self.assertEqual(locData.elevation, 0.0)

    # WaterLocationData Custom Values
    def testWaterLocationDataContainerCustomValues(self):
        locData = WaterLocationData()
        locData.siteName = "My Location"
        locData.siteID = "LOC001"
        locData.county = "TestCounty"
        locData.state = "MA"
        locData.country = "USA"
        locData.latitude = 42.36
        locData.longitude = -71.06
        locData.elevation = 12.0
        
        # Verify all custom values stored correctly.
        self.assertEqual(locData.siteName, "My Location")
        self.assertEqual(locData.siteID, "LOC001")
        self.assertEqual(locData.county, "TestCounty")
        self.assertEqual(locData.state, "MA")
        self.assertEqual(locData.country, "USA")
        self.assertEqual(locData.latitude, 42.36)
        self.assertEqual(locData.longitude, -71.06)
        self.assertEqual(locData.elevation, 12.0)
        
        