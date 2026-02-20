import logging
import unittest
import time
import datetime

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil


class TimeAndDateUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run.
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing TimeAndDateUtil class...")
     

    def setUp(self):
        # Run before each test method.
        pass
   
    
    def tearDown(self):
        # Run after each test method.
        pass
    
    
    def testGetCurrentLocalDateInMillis(self):
        # Call the method to get the current time in milliseconds.
        current_millis = TimeAndDateUtil.getCurrentLocalDateInMillis()
        
        # Check that the result is an integer.
        self.assertIsInstance(current_millis, int)
        
        # Check that the result is greater than zero. 
        self.assertGreater(current_millis, 0)
    
         
    def testGetCurrentIso8601LocalDate(self):
        # Call the method to get the current time as an ISO 8601 string.
        curA = TimeAndDateUtil.getCurrentIso8601LocalDate()
        
        # Expected ISO 8601 string value using datetime.
        curB = datetime.datetime.fromtimestamp(time.time()).replace(microsecond=0).isoformat()

        # Checks that the actual output matches the expected output,
        # may fail if system is very slow, because time passes between the two calls.
        self.assertEqual(curA, curB)
           
          
    def testGetIso8601DateFromMillis(self):
        # Get the current time in milliseconds.
        now_millis = int(time.time() * 1000)
        
        # Call the method to get the time from (now_millis) as an ISO 8601 string.
        curA = TimeAndDateUtil.getIso8601DateFromMillis(now_millis)
        
        # Expected ISO 8601 string value from (now_millis), using datetime.
        curB = datetime.datetime.fromtimestamp(now_millis / 1000).replace(microsecond=0).isoformat()

        # Checks that the actual output matches the expected output, may fail if system is very slow.
        self.assertEqual(curA, curB)


