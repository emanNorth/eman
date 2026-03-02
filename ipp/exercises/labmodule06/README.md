# Programming in Python - An Introduction: Lab Module 06

### Description

Briefly describe the objectives of the Lab Module:

1) Demonstrate how to create base classes in Python for a weather service application:
. `WeatherDataListener` with template method `_processWeatherData()` to handle incoming weather data updates.
. `WeatherDataParser` with template method `_createWeatherDataFromRawData()` to parse raw weather service data into WeatherData objects.

2) Demonstrate the creation of the `WeatherServiceConnector` base class that:
. Fetches raw weather data from a public weather service.
. Stores raw data `latestRawData` and JSON string `latestJsonData` internally.
. Optionally uses a WeatherDataParser `self.dataParser` to parse raw data into a structured WeatherData object `latestWeatherData`.
. Provides access to both raw and parsed data via getter methods.
. Manages HTTP connections with `connectToService()` and `disconnectFromService()`.
. Serves as a central hub so managers and listeners can access weather data without interacting with the parser directly.

3) Implemented modules to fetch and parse NOAA weather data:
. `NoaaWeatherDataParser`: subclass of WeatherDataParser; transforms raw NOAA JSON into structured WeatherData objects.
. `NoaaWeatherServiceConnector`:subclass of WeatherServiceConnector; connects to NOAA, retrieves raw weather data, and stores both raw and parsed data for access by managers/listeners.

4) Implemented modules to manage asynchronous weather data retrieval from NOAA:
. `WeatherServiceManager`: primary manager class; uses APScheduler to poll configured weather stations, fetches data via a .. `WeatherServiceConnector`, and notifies listeners.
. `WeatherDataListener`: interface for receiving updates from the manager when new weather data is retrieved.



### Exercise Activities

List the actions you took in implementing the Lab Module:

1) 
. Created `WeatherDataListener.py` with __init__(), `handleIncomingWeatherData()`, and `_processWeatherData() methods`, ; `handleIncomingWeatherData()` acts as a gatekeeper and calls `_processWeatherData()`; `_processWeatherData()` is a placeholder to be overridden by subclasses. 

. Created `WeatherDataParser.py` with __init__(), `parseWeatherData()`, and `_createWeatherDataFromRawData()` methods; `parseWeatherData()` validates input and calls the template method; `_createWeatherDataFromRawData()` is a placeholder for subclass implementation.

. Added weather service configuration to IppConfig.props with [WeatherPredictorApp] and [Settings.Weather] sections including service name, polling intervals, device info, and logging o


2) Created `WeatherServiceConnector.py` implementing:
. __init__(): accepts an optional `WeatherDataParser` and calls `_initProperties()`.
. `_initProperties()`: reads configuration from IppConfig.props and sets attributes (baseUrl, serviceName, pollRate, requestTimeout, userAgent, contentType, clientSession, isConnected, latestRawData, latestJsonData, latestWeatherData).
. Template methods: `_createRequestUrl()` and `_getLatestWeatherData()` as placeholders for service-specific URL and data retrieval.
. Connection management: `connectToService()` opens a session and sets headers; `disconnectFromService()` closes it and resets status.
. Workflow `requestCurrentWeatherData()`: fetches raw data, stores it, parses it if parser is provided, stores parsed data, and prints success/failure messages.
. Getter methods: access connector attributes and latest raw/parsed data.
. Design: connector acts as a hub storing raw and parsed data for manager/listener access without direct parser interaction.

3) 
.  Created `NoaaWeatherDataParser.py` subclassing `WeatherDataParser` with class `NoaaWeatherDataParser`; implemented `_createWeatherDataFromRawData()` to extract and map NOAA JSON fields (location, timestamp, temperature, dewpoint, wind, humidity, visibility, pressure, cloud layers) into a structured WeatherData object,handling missing values or null data with defaults and adding debug print statements.

. Created `NoaaWeatherServiceConnector.py`  subclassing `WeatherServiceConnector`, with class `NoaaWeatherServiceConnector`; implemented `_createRequestUrl()` to generate station specific NOAA URL, `_getLatestWeatherData()` to perform HTTP GET requests using requests.Session(), handle errors, and supplement location data; used `NoaaWeatherDataParser` internally to parse raw data into WeatherData objects.

. Created `test_NoaaWeatherServiceConnector.py` using unittest to validate connection setup, weather data retrieval, JSON output, and service properties.

4) 
. Created `WeatherServiceManager.py` with class `WeatherServiceManager`; implemented:
init() and _initProperties() to configure scheduler, station polling cycle, and weather service connection.
`_scheduleAndStartWeatherServiceJob()` to configure APScheduler interval jobs for periodic data fetching.
`startManager()` and `stopManager()` to control service connection, scheduler execution, and running state.
`_getLocationData(stationID)` to provide location information for known stations (KBOS, KJFK, KORD) or default to generic values for unknown stations.
`processWeatherData()` to request, retrieve, and parse weather data for each station in the polling cycle and notify any attached listener.
setListener(listener) to attach a listener for updates, and `isClientConnected()` to check connection status.

. Created `test_WeatherServiceManager.py` using unittest framework; implemented WeatherServiceManagerTest to:
Initialize a WeatherServiceManager instance.
Start the manager, let it run for ~2 minutes to simulate asynchronous weather data retrieval.
Stop the manager and validate graceful shutdown of scheduler and service connection.



### Unit and/or Integration Tests Executed

List the tests you exercised in validating your functionality for the Lab Module:

1) Instantiated `WeatherDataListener`, `WeatherDataParser`, and called  their workflow methods with and without valid data; confirmed no runtime errors occurred; verified template methods are only called when data is provided.
2) Instantiated `WeatherServiceConnector` with and without a WeatherDataParser, simulated fetching weather data using a dummy subclass of the connector, called `requestCurrentWeatherData()`, and confirmed that `latestRawData`, `latestJsonData`, and `latestWeatherData` were correctly set; also tested `connectToService()` and `disconnectFromService()` and verified that all getters returned expected values.
3) Ran `test_NoaaWeatherServiceConnector.py` using the unittest framework in VS Code and from the command line; verified successful service connection and disconnection, confirmed live NOAA weather data retrieval by station ID, validated non-null JSON output, and ensured connector properties returned expected configuration values.
4) Ran `test_WeatherServiceManager.py` using the unittest framework in VS Code and from the command line; verified successful manager startup and shutdown, confirmed APScheduler executes polling jobs at the configured interval, validated weather data retrieval for configured stations in JSON format, ensured attached listener (if any) receives updates, and confirmed manager handles default stations when no configuration is provided.

EOF.
