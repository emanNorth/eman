import datetime
import logging
import time
import unittest

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData
from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterServiceManagerFile import WaterServiceManager
from ipp.common.ConfigUtil import ConfigUtil


class WaterServiceManagerTest(unittest.TestCase):
    '''
    Unit tests for the WaterServiceManager class.

    This test case starts the water service manager, allows it to run
    for a short period to simulate data retrieval, and then stops the manager.
    It can be expanded with additional tests for edge cases, listener handling,
    and station configuration.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Runs once before all tests in this class.

        Configures the logging system to display debug level messages.
        '''
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing WaterServiceManager class...")

    def setUp(self):
        '''
        Runs before each test method.

        Initializes a new WaterServiceManager instance for testing.
        '''
        self.waterSvcMgr = WaterServiceManager()

    def tearDown(self):
        '''
        Runs after each test method.

        Can be used to clean up resources if needed. Currently, no cleanup is required.
        '''
        pass

    def testWaterServiceManagerExecution(self):
        '''
        Tests the basic execution of WaterServiceManager.

        Steps:
            1. Starts the manager (connects to service and schedules jobs)
            2. Allows it to run for approximately 2 minutes to simulate data polling
            3. Stops the manager (disconnects and shuts down scheduler)

        Note:
            This test primarily ensures that the manager can start, process
            water data asynchronously, and stop without errors.
        '''
        # Start the manager
        self.waterSvcMgr.startManager()

        # Allow manager to run for ~2 minutes to fetch water data
        # It keeps the test running long enough for the background scheduler to actually execute and fetch data.
        time.sleep(120)

        # Stop the manager
        self.waterSvcMgr.stopManager()