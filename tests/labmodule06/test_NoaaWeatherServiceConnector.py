import logging
import time
import unittest

from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule06.NoaaWeatherServiceConnector import NoaaWeatherServiceConnector

class NoaaWeatherServiceConnectorTest(unittest.TestCase):
    '''
    Unit tests for NoaaWeatherServiceConnector.

    Tests include:
    - Connecting and disconnecting from the NOAA weather service.
    - Requesting current weather data for a given station.
    - Verifying that service properties return expected values.
    '''

    @classmethod
    def setUpClass(cls):
        """Run once before all tests to configure logging."""
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing NoaaWeatherServiceConnector class...")

    def setUp(self):
        '''Run before each test method; creates a fresh connector instance.'''
        self.weatherSvc = NoaaWeatherServiceConnector()

    def tearDown(self):
        '''Run after each test method; placeholder for cleanup if needed.'''
        pass

    def testWeatherServiceConnection(self):
        '''
        Test connecting to and disconnecting from NOAA service.
        Verifies connectToService() and disconnectFromService() return True.
        '''
        self.assertTrue(self.weatherSvc.connectToService())
        time.sleep(5)  # wait briefly to simulate service response
        self.assertTrue(self.weatherSvc.disconnectFromService())

    def testWeatherServiceRequestByStation(self):
        '''
        Test requesting weather data for a sample station.
        Verifies that JSON data is returned and not None.
        '''
        locData = self._createSampleLocationData()
        
        # Connect to the service
        self.assertTrue(self.weatherSvc.connectToService())
        time.sleep(5)

        # Request current weather data for the sample station
        self.assertTrue(
            self.weatherSvc.requestCurrentWeatherData(
                stationID=locData.name, locData=locData
            )
        )

        # Retrieve the latest weather data as JSON
        jsonData = self.weatherSvc.getLatestWeatherDataAsJson()
        print(jsonData)

        # Ensure the JSON data is not None
        self.assertIsNotNone(jsonData)
        time.sleep(5)

        # Disconnect from the service
        self.assertTrue(self.weatherSvc.disconnectFromService())

    def testWeatherServiceProperties(self):
        '''
        Test service-specific properties.
        Verifies the service name is as expected.
        '''
        self.assertEqual(self.weatherSvc.getServiceName(), "NOAA Weather Service")
        # TODO: Add assertions for other service properties like pollRate, baseUrl, etc.

    def _createSampleLocationData(self) -> LocationData:
        '''
        Helper method to create a sample LocationData object.

        Returns:
            LocationData: populated with sample coordinates and metadata.
        '''
        locData = LocationData()
        locData.name = "KBOS"
        locData.city = "Boston"
        locData.region = "MA"
        locData.country = "USA"
        locData.latitude = 42.35843
        locData.longitude = -71.05977

        return locData