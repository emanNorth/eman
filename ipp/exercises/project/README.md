# Programming in Python - An Introduction: Lab Module 10

### Description

Briefly describe the objectives of the Lab Module:

1) Implement a real time data capture system that retrieves live water monitoring data from the USGS NWIS API using HTTP requests and a service connector architecture.


2) Build both a GUI and a web based dashboard to visualize and interact with live water data, including aggregation and time series analysis using bar and line graphs.

3) Create a sort function that orders water data by numeric values and text based fields, and allow the user to trigger sorting through buttons in the application.


### Exercise Activities

List the actions you took in implementing the Lab Module:

1) Built a connector class that connects to the USGS NWIS API and retrieves live JSON water data for multiple monitoring stations.

2) Built a manager class that automatically cycles through different stations and keeps updating the latest water readings on a timer.

3) Made two ways to view the data:
A Tkinter desktop app that lets the user sort water data by flow, level, temperature, and site name.
A web dashboard using Dash that shows live graphs and updates automatically, i also implemented sorting functionality that allows users to organize data by flow rate, water level, temperature, and site name. The dashboard also updates graphs in real time as new data arrives.



### Unit and/or Integration Tests Executed

List the tests you exercised in validating your functionality for the Lab Module:

1) Tested the NwisWaterServiceConnector to verify it can connect to the USGS NWIS API, request live water data for a station, and return valid JSON responses.

2) Tested the WaterServiceManager to confirm it correctly starts the service, cycles through multiple stations, and continuously retrieves live water data using a timed scheduler.

3) Tested core system components including the LiveWaterDataWebVisualizer, SimpleBubbleSort, WaterData, and WaterLocationData classes to ensure correct data storage, sorting functionality, and live visualization updates in both the GUI and web dashboard.

EOF.
