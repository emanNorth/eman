import logging
import unittest

from datetime import datetime

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.labmodule07.StatsData import StatsData


class StatsDataTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing StatsData class ...")
        
    def setUp(self):
        # Run before each test method
        pass
    
    def tearDown(self):
        # Run after each test method
        pass
    
    # StatsData Default Values
    def testStatsDataContainerDefaultValues(self):
        
        # Creates a StatsData object with all defults values.
        sData = StatsData()
        
        # Get the current timestamp in ISO8601 format.
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
    
        # Checks that all defalut attributes have the expected value
        self.assertEqual(sData.count, 0)
        self.assertEqual(sData.median, 0.0)
        self.assertEqual(sData.max, 0.0)
        self.assertEqual(sData.min, 0.0)
        self.assertEqual(sData.standardDeviation, 0.0)
        
        # assert they're within 5 seconds
        timestampA = datetime.fromisoformat(sData.timestamp).timestamp()
        timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
        self.assertAlmostEqual(timestampA,timestampB, delta=5.0)
        
    # StatData Custom Values
    def testStatsDataContainerCustomValues(self):
             
        # Creates a StatsData object with all defults values.
        sData = StatsData()
        
        # Get the current timestamp in ISO8601 format.
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
        
        # Assign custom values to the StatData object.
        sData.count = 5
        sData.mean = 55.0
        sData.median = 52.0
        sData.min = 25.0 
        sData.max = 75.0 
        sData.standardDeviation = 2.5 
        
        # Verify all custom values stored correctly.
        self.assertEqual(sData.count, 5)
        self.assertEqual(sData.mean, 55.0)
        self.assertEqual(sData.median, 52.0)
        self.assertEqual(sData.min, 25.0)
        self.assertEqual(sData.max, 75.0)
        self.assertEqual(sData.standardDeviation, 2.5)
        
        
        timestampA = datetime.fromisoformat(sData.timestamp).timestamp()
        timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
		
		# assert they're within 5 seconds
        self.assertAlmostEqual(timestampA, timestampB, delta = 5.0)
        
    