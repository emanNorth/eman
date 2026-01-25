# Programming in Python - An Introduction: Lab Module 03

### Description

Briefly describe the objectives of the Lab Module:

1) Practice using basic Python program flow and function definitions.

2) Practice calling functions from within other functions and across modules.

3) Create a simple application that imports and calls functions across modules.


### Exercise Activities

List the actions you took in implementing the Lab Module:

1) Created `SimpleTempConversion.py` module to test temperature conversion functions including checking if the given temperature is within the desired indoor range and converting temperatures between Fahrenheit and Celsius.

2) Created `SimpleDivision.py` and `CalcFunctionCallingFunction.py` modules to test simple division calculations, demonstrated calling functions from other modules and handled division by zero exceptions.

3) Created a simple test application, `MyFirstTestApp.py`, that imports and calls functions from different modules as part of a basic application flow.



### Unit and/or Integration Tests Executed

List the tests you exercised in validating your functionality for the Lab Module:

1) Ran `SimpleTempConversion.py` to test indoor temperature range validation using values inside and outside the desired range limits.

2) Tested Fahrenheit to Celsius and Celsius to Fahrenheit conversions.

3) Tested division operations including division by zero cases, to verify exceptions are correctly handled within modules and when functions are imported.

# UML
### UML Diagram for SimpleTempConversion

+----------------------------+
| SimpleTempConversion |
+----------------------------+
| - min_indoor_temp_F |
| - max_indoor_temp_F |
+----------------------------+
| + isDesiredIndoorTempRange() |
| + convertTempFtoC() |
| + convertTempCtoF() |
+----------------------------+


### UML Diagram for SimpleDivision.py
+----------------------------------------------+
| SimpleDivision                               |
+----------------------------------------------+
|                                              |
+----------------------------------------------+
| + divideTwoNumbersWithExceptionHandling()     |
+----------------------------------------------+

### UML Diagram for CalcFunctionCallingFunction.py

+--------------------------------+
| CalcFunctionCallingFunction    |
+--------------------------------+
| + divideTwoNumbers()           |
+--------------------------------+
              |
              | calls
              v
+--------------------------------+
| SimpleDivision                 |
+--------------------------------+
| + divideTwoNumbersWithExceptionHandling() |
+--------------------------------+

### UML Diagram for MyFirstTestApp.py

+---------------------------+
| MyFirstTestApp            |
+---------------------------+
| + main()                  |
| + doWork()                |
+---------------------------+
              |
              | calls
              v
+----------------------------+
| SimpleTempConversion       |
+----------------------------+
| + convertTempFtoC()        |
+----------------------------+
EOF.