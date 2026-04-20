import logging
import unittest

import matplotlib.pyplot as plt

from ipp.exercises.project.LiveWaterDataClientVisualizerFile import LiveWaterDataClientVisualizer
from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData


class LiveWaterDataClientVisualizerTest(unittest.TestCase):
    '''
    Unit tests for LiveWaterDataClientVisualizer.

    Tests:
    - Initialization
    - Adding new water data
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
        logging.info("Testing LiveWaterDataClientVisualizer...")

    def setUp(self):
        # Run before each test method
        pass

    def tearDown(self):
        # Close all matplotlib figures after each test
        plt.close('all')

    def _createSampleWaterData(self, station_id: str, flow: float = 1000.0) -> WaterData:
        '''
        Creates a simple WaterData object for testing.

        Args:
            station_id (str): Station identifier
            flow (float): Flow rate value

        Returns:
            WaterData: Populated test object
        '''
        wd = WaterData()
        wd.location = WaterLocationData()
        wd.location.siteID = station_id
        wd.location.siteName = "Test Station"
        
        wd.waterLevel_ft = 10.0
        wd.flowRate_cfs = flow
        wd.waterTemperature_c = 15.0
        wd.timestamp = "2026-01-01T00:00:00"

        return wd

    def testVisualizerInitialization(self):
        '''
        Test that visualizer initializes correctly.
        '''
        vis = LiveWaterDataClientVisualizer()

        # Dictionary should exist
        self.assertIsNotNone(vis.liveWaterDataTable)

        # Should start empty
        self.assertEqual(len(vis.liveWaterDataTable), 0)

    def testAddWaterData(self):
        '''
        Test adding new water data for a station.
        '''
        vis = LiveWaterDataClientVisualizer()

        wd = self._createSampleWaterData("USGS-01646500")

        vis.handleIncomingWaterData(wd)

        self.assertIn("USGS-01646500", vis.liveWaterDataTable)

    def testUpdateWaterData(self):
        '''
        Test updating water data for an existing station.
        '''
        vis = LiveWaterDataClientVisualizer()

        wd1 = self._createSampleWaterData("USGS-01646500", 1000.0)
        wd2 = self._createSampleWaterData("USGS-01646500", 2000.0)

        vis.handleIncomingWaterData(wd1)
        vis.handleIncomingWaterData(wd2)

        self.assertEqual(
            vis.liveWaterDataTable["USGS-01646500"].flowRate_cfs,
            2000.0
        )

    def testMultipleStations(self):
        '''
        Test storing water data for multiple stations.
        '''
        vis = LiveWaterDataClientVisualizer()

        wd1 = self._createSampleWaterData("USGS-01646500")
        wd2 = self._createSampleWaterData("USGS-06730500")

        vis.handleIncomingWaterData(wd1)
        vis.handleIncomingWaterData(wd2)

        self.assertEqual(len(vis.liveWaterDataTable), 2)


if __name__ == '__main__':
    unittest.main()