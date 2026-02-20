import logging
import unittest

from ipp.exercises.labmodule05.CalculationsUtil import CalculationsUtil


class CalculationsUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing CalculationsUtil class...")

    def setUp(self):
        # Run before each test method
        pass

    def tearDown(self):
        # Run after each test method
        pass

    def testDivideTwoIntegers(self):
        self.assertEqual(0.0, CalculationsUtil.divideTwoNumbers(1, 0))
        self.assertEqual(5.0, CalculationsUtil.divideTwoNumbers(10, 2))
        self.assertEqual(2.0, CalculationsUtil.divideTwoNumbers(10, 5))
        self.assertEqual(1.0, CalculationsUtil.divideTwoNumbers(10, 10))

    def testDivideTwoFloats(self):
        self.assertEqual(0.0, CalculationsUtil.divideTwoNumbers(1.5, 0))
        self.assertEqual(5.5, CalculationsUtil.divideTwoNumbers(11, 2))
        self.assertEqual(2.5, CalculationsUtil.divideTwoNumbers(5, 2))
        self.assertEqual(1.5, CalculationsUtil.divideTwoNumbers(1.5, 1.0))

    def testFarenheitToCelsiusConversion(self):
        self.assertEqual(0.0, CalculationsUtil.convertTempFtoC(32.0))
        self.assertEqual(100.0, CalculationsUtil.convertTempFtoC(212.0))
        self.assertEqual(-17.8, CalculationsUtil.convertTempFtoC(0.0))
        self.assertEqual(37.8, CalculationsUtil.convertTempFtoC(100.0))

    def testCelsiusToFarenheitConversion(self):
        self.assertEqual(32.0, CalculationsUtil.convertTempCtoF(0.0))
        self.assertEqual(212.0, CalculationsUtil.convertTempCtoF(100.0))
        self.assertEqual(-40.0, CalculationsUtil.convertTempCtoF(-40.0))
        self.assertEqual(50.0, CalculationsUtil.convertTempCtoF(10.0))
