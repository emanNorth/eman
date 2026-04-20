import logging
import time
import unittest

from ipp.exercises.project.WaterLocationDataFile import WaterLocationData
from ipp.exercises.project.NwisWaterServiceConnectorFile import NwisWaterServiceConnector


class NwisWaterServiceConnectorTest(unittest.TestCase):
    '''
    Unit tests for NwisWaterServiceConnector.

    Tests include:
    - Connecting and disconnecting from the NWIS water service.
    - Requesting current water data for a given site.
    - Verifying that service properties return expected values.
    '''

    @classmethod
    def setUpClass(cls):
        """Run once before all tests to configure logging."""
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing NwisWaterServiceConnector class...")

    def setUp(self):
        '''Run before each test method; creates a fresh connector instance.'''
        self.waterSvc = NwisWaterServiceConnector()

    def tearDown(self):
        '''Run after each test method; placeholder for cleanup if needed.'''
        pass

    def testWaterServiceConnection(self):
        '''
        Test connecting to and disconnecting from NWIS service.
        Verifies connectToService() and disconnectFromService() return True.
        '''
        self.assertTrue(self.waterSvc.connectToService())
        time.sleep(2)
        self.assertTrue(self.waterSvc.disconnectFromService())

    def testWaterServiceRequestBySite(self):
        '''
        Test requesting water data for a sample site.
        Verifies that JSON data is returned and not None.
        '''
        locData = self._createSampleLocationData()

        # Connect to the service
        self.assertTrue(self.waterSvc.connectToService())
        time.sleep(5)

        # Request current water data for the sample site
        self.assertTrue(
            self.waterSvc.requestCurrentWaterData(
                siteID=locData.siteID, locData=locData
            )
        )

        # Retrieve latest water data as JSON
        jsonData = self.waterSvc.getLatestWaterDataAsJson()
        print(jsonData)

        # Ensure JSON data is not None
        self.assertIsNotNone(jsonData)
        time.sleep(5)

        # Disconnect from service
        self.assertTrue(self.waterSvc.disconnectFromService())

    def testWaterServiceProperties(self):
        '''
        Test service-specific properties.
        Verifies the service name is as expected.
        '''
        self.assertEqual(
            self.waterSvc.getServiceName(),
            "USGS NWIS Water Service"
        )
        # TODO: Add assertions for pollRate, baseUrl, etc.

    def _createSampleLocationData(self) -> WaterLocationData:
        '''
        Helper method to create a sample WaterLocationData object.

        Returns:
            WaterLocationData: populated with sample coordinates and metadata.
        '''
        locData = WaterLocationData()
        locData.siteID = "01646500"
        locData.siteName = "CHARLES RIVER AT WALTHAM, MA"
        locData.state = "MA"
        locData.country = "USA"
        locData.latitude = 42.36
        locData.longitude = -71.26

        return locData