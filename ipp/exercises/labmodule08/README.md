# Programming in Python - An Introduction: Lab Module 08

### Description

Briefly describe the objectives of the Lab Module:

1) Demonstrate how to create a live weather data visualizer using matplotlib, threading, and real time updates from multiple weather stations. The visualizer receives WeatherData objects and displays them in a dashboard with multiple subplots.


2) Demonstrate how to create a live weather data visualizer using Dash, Plotly, threading, and real time updates from multiple weather stations. The visualizer receives WeatherData objects and displays them in a web dashboard with charts and summary statistics.


### Exercise Activities

List the actions you took in implementing the Lab Module:

1) Created `LiveWeatherDataClientVisualizer.py` with a class that extends `WeatherDataListener` to process and to visualize live weather data from multiple stations.

Set up a matplotlib figure with subplots and configured titles, colors, gridlines, and layout.
Implemented `handleIncomingWeatherData()` to receive WeatherData objects from the listener and store them in a thread-safe dictionary.
Added `_updateVisualization()` method to refresh bar plots for temperature, humidity, wind speed, and pressure every few seconds using FuncAnimation.
Created a test mode using a Thread to simulate incoming weather data for demonstration purposes.
Ensured proper initialization, updating, and cleanup of the figure to handle multiple stations and live data.


2) Created `LiveWeatherDataWebVisualizer.py` with a class that extends `WeatherDataListener` to process and  visualize live weather data from multiple stations in a web browser.

Set up a Dash web server and created the layout with a header, statistics section, and charts container.
Implemented a thread-safe dictionary using `Lock` to store WeatherData objects by station ID.
Added callback logic to update the dashboard every few seconds using the Interval component.
Implemented `_processWeatherData()` to receive WeatherData objects and update the internal data storage.
Created helper methods to build the UI including `_createStatsSummary()`, `_createStatCard()`, `_createCharts()`, and `_createChart()`.
Used Plotly to generate bar charts for temperature, humidity, wind speed, and pressure.
Created a test mode using a Thread to simulate incoming weather data for multiple stations and demonstrate real time updates in the web dashboard.



### Unit and/or Integration Tests Executed

List the tests you exercised in validating your functionality for the Lab Module:

1) Ran `test_LiveWeatherDataClientVisualizer.py` in VS Code using the unittest framework: tested the module directly from within the IDE and the command line, verified the following tests all passed:
`testVisualizerInitialization()` confirmed that the visualizer initializes correctly with an empty data dictionary.
`testHandleIncomingWeatherData()` verified that incoming WeatherData objects are correctly stored and updated in the dictionary.
`testUpdateVisualization()` confirmed that the visualization updates bar plots correctly when new data arrives.
`testMultipleStationUpdates()` verified that multiple stations data are displayed and updated simultaneously in the subplots.
`testCleanup()` ensured that the visualizer closes figures properly after tests to avoid memory or plotting issues.


2) Ran `test_LiveWeatherDataWebVisualizer.py` in VS Code using the unittest framework: tested the module directly from within the IDE and the command line, verified the following tests all passed:
`testVisualizerInitialization()` confirmed that the visualizer initializes correctly with an empty data dictionary.
`testAddWeatherData()` verified that incoming WeatherData objects are correctly stored in the dictionary.
`testUpdateWeatherData()` confirmed that existing station data is updated correctly when new data is received.
`testMultipleStations()` verified that multiple stations are stored and handled correctly.
`testStatsSummaryGeneration()` confirmed that the statistics summary is created without errors.
`testChartCreation()` verified that chart components are created correctly for all weather metrics.

EOF.
