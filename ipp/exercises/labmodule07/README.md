# Programming in Python - An Introduction: Lab Module 07

### Description

Briefly describe the objectives of the Lab Module:

1) Demonstrate how to create classes for representing statistical data, including count, mean, median, min, max, standard deviation, and timestamp.

2) Demonstrate how to create a utility class for calculating statistical values, including count, mean, median, min, max, standard deviation, and timestamp.

3) Demonstrate how to create a utility class for file operations, including reading, writing, and checking the existence of files and directories.

4) Demonstrate how to create a utility class for converting objects to and from JSON and saving and loading them from files.


### Exercise Activities

List the actions you took in implementing the Lab Module:

1) 
- Created `StatsData.py` to hold statistical information including count, mean, median, min, max, standardDeviation, and timestamp. Default values are assigned in the constructor and timestamp is generated using TimeAndDateUtil.

- Created `test_StatsData.py` as a unittest module to validate StatsData.
Created StatsDataTest class. 
Implemented `testStatsDataContainerDefaultValues` to confirm all default attribute values and timestamp accuracy.Implemented `testStatsDataContainerCustomValues` to confirm custom attribute values are stored correctly and timestamp is within 5 seconds of creation.

2) 
- Created `StatsCalculationsUtil.py` with the `StatsCalculationsUtil` class inheriting from `CalculationsUtil` and a classmethod `calculateStats()` to accept a list of floats and return a StatsData object, handling empty lists and sets count, min, max, mean, median, standard deviation, and timestamp.

- Created unit tests in `test_StatsCalculationsUtil.py` to verify default and custom lists of floats, confirming calculated statistical values and timestamp accuracy within 5 seconds.

3) Created `FileUtil.py` with `readTextFile`, `writeTextFile`, `fileExists`, and `directoryExists` using classmethods; implemented reading and writing text files with error handling, checking file and directory existence, and handling missing files, permissions, and encoding issues. Created unit tests in `test_FileUtil.py` to verify each method using unittest.

4) Created `DataConverterUtil.py` with classmethods to convert `WeatherData` and `StatsData` objects to and from JSON.  
- Handled nested objects (`LocationData`, `WindData`, `VisibilityData`, `CloudLayerData`) and lists when converting WeatherData.  
- Implemented writing and reading objects to and from files with error handling.  
- Created `test_DataConverterUtil.py` as a unittest module to validate conversions and file operations.


### Unit and/or Integration Tests Executed

List the tests you exercised in validating your functionality for the Lab Module:

1) Ran `test_StatsData.py` in VS Code using the unittest framework, tested the module directly from within the IDE and the command line, verified the following tests all passed:
`testStatsDataContainerDefaultValues` confirmed that all default StatsData attributes have the expected values and timestamp is within 5 seconds of creation.
`testStatsDataContainerCustomValues` verified that custom values assigned to StatsData attributes are stored correctly and timestamp is within 5 seconds of creation.

2) Ran `test_StatsCalculationsUtil.py` in VS Code using the unittest framework, tested the module directly from within the IDE and the command line, verified the following tests all passed:
`testStatsDataContainerDefaultValues` confirmed that an empty list produces a StatsData object with default values and timestamp within 5 seconds.
`testStatsDataContainerCustomValues` verified that a list of floats produces correct statistics and timestamp within 5 seconds.

3) Ran `test_FileUtil.py` in VS Code using the unittest framework, tested the module directly from within the IDE and the command line, verified the following tests all passed: 
`testReadFile()` confirmed reading a file returns correct content
`testWriteFile()` confirmed writing a file and stores correct data
`testDoesFileExist()` confirmed file existence detection works
`testDoesPathExist()` confirmed directory existence detection works.

4) Ran `test_DataConverterUtil.py` in VS Code using the unittest framework: tested the module directly from within the IDE and the command line, verified the following tests all passed: 
`testWeatherDataToJson()` confirmed that a WeatherData object is correctly converted into a JSON string.
`testJsonToWeatherData()` verified that a JSON string is correctly converted back into a WeatherData object, including nested objects such as location and cloud layers.
`testStatsDataToJson()` confirmed that a StatsData object is correctly converted into a JSON string.
`testJsonToStatsData()` verified that a JSON string is correctly converted back into a StatsData object with accurate values.
`testWriteStatsDataToFile()` confirmed that a StatsData object can be successfully written to a file in JSON format.
`testReadStatsDataFromFile()` verified that a StatsData object can be correctly read from a file and reconstructed from JSON.
`testWriteWeatherDataToFile()` confirmed that a WeatherData object can be successfully written to a file in JSON format.
`testReadWeatherDataFromFile()` verified that a WeatherData object can be correctly read from a file and reconstructed from JSON, including nested data structures

EOF.
