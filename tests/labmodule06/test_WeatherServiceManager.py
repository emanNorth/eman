import datetime
import logging
import time
import unittest

from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule06.WeatherServiceManager import WeatherServiceManager

class WeatherServiceManagerTest(unittest.TestCase):
    '''
    Unit tests for the WeatherServiceManager class.

    This test case starts the weather service manager, allows it to run
    for a short period to simulate data retrieval, and then stops the manager.
    It can be expanded with additional tests for edge cases, listener handling,
    and station configuration.
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Runs once before all tests in this class.

        Configures the logging system to display debug-level messages.
        '''
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing WeatherServiceManager class...")

    def setUp(self):
        '''
        Runs before each test method.

        Initializes a new WeatherServiceManager instance for testing.
        '''
        self.weatherSvcMgr = WeatherServiceManager()

    def tearDown(self):
        '''
        Runs after each test method.

        Can be used to clean up resources if needed. Currently, no cleanup is required.
        '''
        pass

    def testWeatherServiceManagerExecution(self):
        '''
        Tests the basic execution of WeatherServiceManager.

        Steps:
            1. Starts the manager (connects to service and schedules jobs)
            2. Allows it to run for approximately 2 minutes to simulate data polling
            3. Stops the manager (disconnects and shuts down scheduler)

        Note:
            This test primarily ensures that the manager can start, process
            weather data asynchronously, and stop without errors.
        '''
        # Start the manager
        self.weatherSvcMgr.startManager()

        # Allow manager to run for ~2 minutes to fetch weather data
        time.sleep(120)

        # Stop the manager
        self.weatherSvcMgr.stopManager()