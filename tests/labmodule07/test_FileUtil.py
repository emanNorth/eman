import logging
import unittest
import tempfile
import os

from typing import List

from ipp.exercises.labmodule07.FileUtil import FileUtil

class FileUtilTest(unittest.TestCase):
    '''
    Unit tests for the FileUtil class.

    Tests reading, writing, and existence checks for files and directories.
    '''
    
    # Set system temporary directory for creating test files
    TEST_PATH = tempfile.gettempdir()
    # The filename used for all temporary test files
    TEST_FILE = "IppTestFile.txt"
    
    @classmethod
    def setUpClass(cls):
        # Configure logging for the test run
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing FileUtil class...")
        
    def setUp(self):
        # Run before each test method
        pass 
        
    def tearDown(self):
        # Run after each test method
        pass
 
        
    def _createTestFileName(self) -> str:
        '''
        Creates the full path for the temporary test file.

        Returns:
            str: Full path to the test file in the system temp directory.
        '''
        
        # Combines temporary folder path and test file name
        fileName = os.path.join(tempfile.gettempdir(), FileUtilTest.TEST_FILE)
        return fileName
        
        
    def _createTestData(self) -> str:
        '''
        Creates the test data string to write and read.

        Returns:
            str: Test string data.
        '''
        testData = "Test data only. Nothing to see here."
        return testData
    
    
    def testReadFile(self):
        '''
        Tests that FileUtil.readTextFile correctly reads data from a file.
        '''
        fileName = self._createTestFileName()
        testData = self._createTestData()

        # write the file first to make sure it exists
        FileUtil.writeTextFile(fileName = fileName, content = testData)

        # load the data
        loadedData = FileUtil.readTextFile(fileName = fileName)

        # check if it matches the data just written
        self.assertEqual(loadedData, testData)
    
        
    def testWriteFile(self):
        '''
        Tests that FileUtil.writeTextFile correctly writes data to a file.
        '''
        fileName = self._createTestFileName()
        testData = self._createTestData()
        
        # write the file, check if it is successful
        self.assertTrue(FileUtil.writeTextFile(fileName = fileName, content = testData))
        
        # load the data
        loadedData = FileUtil.readTextFile(fileName = fileName)
        
        # check if it matches the data just written
        self.assertEqual(loadedData, testData)
            
        
    def testDoesFileExist(self):
        '''
        Tests that FileUtil.fileExists correctly identifies existing files.
        '''
        fileName = self._createTestFileName()
        # Create and writes the file
        self.testWriteFile()

        self.assertTrue(FileUtil.fileExists(fileName = fileName))
        

    def testDoesPathExist(self):
        '''
        Tests that FileUtil.directoryExists correctly identifies existing directories.
        '''
        dirName = tempfile.gettempdir()
        self.assertTrue(FileUtil.directoryExists(dirName = dirName))