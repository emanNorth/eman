
import logging
import unittest

from typing import List
from datetime import datetime

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.labmodule07.StatsData import StatsData
from ipp.exercises.labmodule07.StatsCalculationsUtil import StatsCalculationsUtil

class StatsCalculationsUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing StatsCalculationsUtil class...")

    def setUp(self):
        # Run before each test method
        pass

    def tearDown(self):
        # Run after each test method
        pass

    def testStatsDataContainerDefaultValues(self):
        # Create an empty list to pass into the class method
        values: List[float] = []
        sData = StatsCalculationsUtil.calculateStats(values)
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()

        # Verify that the StatsData object contains correct default values
        self.assertEqual(sData.count, 0)
        self.assertEqual(sData.mean, 0.0)
        self.assertEqual(sData.median, 0.0)
        self.assertEqual(sData.min, 0.0)
        self.assertEqual(sData.max, 0.0)
        self.assertEqual(sData.standardDeviation, 0.0)

        # Assert timestamps are within 5 seconds
        timestampA = datetime.fromisoformat(sData.timestamp).timestamp()
        timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
        self.assertAlmostEqual(timestampA, timestampB, delta=5.0)

    def testStatsDataContainerCustomValues(self):
        # Create a list of floats to pass into the class method
        values: List[float] = [1.0, 3.0, 6.0, 8.0, 12.0, 15.0, 20.0]
        sData = StatsCalculationsUtil.calculateStats(values)
        isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()

        # Verify that the calculated statistics match the expected values
        self.assertEqual(sData.count, 7)
        self.assertAlmostEqual(sData.mean, 9.285714285714286)
        self.assertEqual(sData.median, 8.0)
        self.assertEqual(sData.min, 1.0)
        self.assertEqual(sData.max, 20.0)
        self.assertAlmostEqual(sData.standardDeviation, 6.77530529974568)

        # Assert timestamps are within 5 seconds
        timestampA = datetime.fromisoformat(sData.timestamp).timestamp()
        timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
        self.assertAlmostEqual(timestampA, timestampB, delta=5.0)