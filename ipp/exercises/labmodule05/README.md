# Programming in Python - An Introduction: Lab Module 05

### Description

Briefly describe the objectives of the Lab Module:

1) Demonstrate how to create a utility class in Python with methods for number division and temperature conversion between Fahrenheit and Celsius using classmethod.

2) Demonstrate how to create a utility class in Python with methods for converting the current time or a given time in milliseconds since the Epoch into ISO 8601 formatted strings.

3) Demonstrate how to create classes for representing weather related data, including location, wind, visibility, cloud layers, and complete weather reports using dataclasses.

4) Demonstrate how to create a base class (Vehicle) with boolean attributes and methods to get their values, then made subclasses (Automobile, Airplane, Train, Rocket) that inherit from Vehicle and set their own specific values.


### Exercise Activities

List the actions you took in implementing the Lab Module:

1) Created `CalculationsUtil.py` with `divideTwoNumbers`, `convertTempFtoC`, and `convertTempCtoF` using classmethods; created unit tests in `test_CalculationsUtil.py` to verify each method using unittest.

2) Created `TimeAndDateUtil.py` with `getCurrentLocalDateInMillis`, `getCurrentIso8601LocalDate`, and `getIso8601DateFromMillis` using classmethods; Converted milliseconds since the Epoch to seconds, implemented conversions of current time or a given time in milliseconds since the Epoch to ISO 8601 formatted strings, and removed microseconds for cleaner output. Created unit tests in `test_TimeAndDateUtil.py`to verify each method using unittest.

3) Created 
   - `LocationData.py` to hold information about a geographical location including name, city, region, country, coordinates, and elevation.
   - `WeatherInfoContainer.py` to hold detailed weather components: `WindData`, `VisibilityData`, and `CloudLayerData`.
   - `WeatherData.py` as a dataclass to aggregate all weather related information, including location, wind, visibility, cloud layers, temperature, humidity, pressure, and optional icon. Used default values and type hints. 

4) Created `ClassPractice01.py` with a base class `Vehicle` containing boolean attributes (`canFly`, `isElectric`, `hasWheels`, `requiresRails`) and optional attributes (`color`, `maxSpeed`) along with methods to get their values. Implemented subclasses `Automobile`, `Airplane`, `Train`, and `Rocket`, using inheritance and super() to assign subclass specific attributes. Added code at the end of the module to instantiate each class, call accessor methods, and verify inheritance relationships using isinstance().


### Unit and/or Integration Tests Executed

List the tests you exercised in validating your functionality for the Lab Module:

1) Ran `test_CalculationsUtil.py` in VS Code and implemented testing using the `unittest` framework, tested the module directly from within the IDE and the command line, verified `testDivideTwoIntegers`, `testDivideTwoFloats`, `testFarenheitToCelsiusConversion`, and `testCelsiusToFarenheitConversion` all passed.

2) Ran `test_TimeAndDateUtil.py` in VS Code using the `unittest` framework, tested the module directly from within the IDE and the command line, verified `testGetCurrentLocalDateInMillis`, `testGetCurrentIso8601LocalDate`, and `testGetIso8601DateFromMillis` all passed.

3) Ran `test_WeatherAndLocationData.py` in VS Code using the `unittest` framework, tested the module directly from within the IDE and the command line, verified the following tests all passed:  
   - `testWeatherDataContainerDefaultValues` confirmed that all default WeatherData attributes have the expected values and nested objects exist.  
   - `testWeatherDataContainerCustomValues` verified that custom values assigned to WeatherData attributes are stored correctly.  
   - `testLocationDataContainerDefaultValues` confirmed that all default LocationData attributes have the expected values.  
   - `testLocationDataContainerCustomValues` verified that custom values assigned to LocationData attributes are stored correctly.

4) Executed `ClassPractice01.py` directly in VS Code and from the command line. Instantiated each class (`Vehicle`, `Automobile`, `Airplane`, `Train`, `Rocket`), verified accessor method outputs for each object, and confirmed inheritance relationships using isinstance() checks to ensure subclasses correctly inherit from Vehicle.

EOF.




