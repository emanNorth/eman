import logging
import unittest

from ipp.exercises.project.LiveWaterDataWebVisualizerFile import LiveWaterDataWebVisualizer
from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData


class LiveWaterDataWebVisualizerTest(unittest.TestCase):
    '''
    Unit tests for LiveWaterDataWebVisualizer.

    Tests:
    - Initialization
    - Adding new water data
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
        logging.info("Testing LiveWaterDataWebVisualizer...")

    def setUp(self):
        # Run before each test method
        pass

    def tearDown(self):
        # Run after each test method
        pass

    def _createSampleWaterData(self, site_id: str, name: str, flow: float = 100.0) -> WaterData:
        '''
        Creates a simple WaterData object for testing.

        Args:
            site_id (str): Station identifier
            name (str): Station name
            flow (float): Flow rate value

        Returns:
            WaterData: Populated object
        '''
        wd = WaterData()
        wd.location = WaterLocationData()
        wd.location.siteID = site_id
        wd.location.siteName = name

        wd.flowRate_cfs = flow
        wd.waterLevel_ft = 5.0
        wd.waterTemperature_c = 15.0

        return wd

    def testVisualizerInitialization(self):
        '''
        Test that visualizer initializes correctly.
        '''
        vis = LiveWaterDataWebVisualizer()

        self.assertIsNotNone(vis.liveWaterDataTable)
        self.assertEqual(len(vis.liveWaterDataTable), 0)
        self.assertIsNotNone(vis.app)

    def testAddWaterData(self):
        '''
        Test adding new water data for a station.
        '''
        vis = LiveWaterDataWebVisualizer()
        wd = self._createSampleWaterData("USGS-001", "Test River")

        vis.handleIncomingWaterData(wd)

        self.assertIn("USGS-001", vis.liveWaterDataTable)

    def testUpdateWaterData(self):
        '''
        Test updating water data for an existing station.
        '''
        vis = LiveWaterDataWebVisualizer()

        wd1 = self._createSampleWaterData("USGS-001", "Test River", 100.0)
        wd2 = self._createSampleWaterData("USGS-001", "Test River", 200.0)

        vis.handleIncomingWaterData(wd1)
        vis.handleIncomingWaterData(wd2)

        self.assertEqual(vis.liveWaterDataTable["USGS-001"].flowRate_cfs, 200.0)

    def testMultipleStations(self):
        '''
        Test handling multiple stations.
        '''
        vis = LiveWaterDataWebVisualizer()

        wd1 = self._createSampleWaterData("USGS-001", "River A")
        wd2 = self._createSampleWaterData("USGS-002", "River B")

        vis.handleIncomingWaterData(wd1)
        vis.handleIncomingWaterData(wd2)

        self.assertEqual(len(vis.liveWaterDataTable), 2)

    def testSummaryGeneration(self):
        '''
        Test that summary renders without errors.
        '''
        vis = LiveWaterDataWebVisualizer()

        data = [
            self._createSampleWaterData("USGS-001", "River A", 100.0),
            self._createSampleWaterData("USGS-002", "River B", 200.0)
        ]

        summary = vis._createSummary(data)

        self.assertIsNotNone(summary)

    def testChartCreation(self):
        '''
        Test chart creation does not fail.
        '''
        vis = LiveWaterDataWebVisualizer()

        data = [
            self._createSampleWaterData("USGS-001", "River A", 100.0),
            self._createSampleWaterData("USGS-002", "River B", 200.0)
        ]

        charts = vis._createCharts(data)

        self.assertEqual(len(charts), 4)


if __name__ == '__main__':
    unittest.main()