from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule05.WeatherInfoContainer import CloudLayerData, VisibilityData, WindData

from ipp.exercises.labmodule06.WeatherDataParser import WeatherDataParser

class NoaaWeatherDataParser(WeatherDataParser):
    '''
    This class transforms raw NOAA JSON response data into a structured
    WeatherData object by extracting relevant weather fields.
    '''

    def __init__(self):
        ''' Initialize the NOAA weather data parser.'''
        super().__init__()

    def _createWeatherDataFromRawData(self, rawData: dict, stationID: str, stationName: str) -> WeatherData:
        '''
        Parse raw NOAA weather JSON data into a WeatherData object.

        Args:
            rawData (dict): Raw JSON data from NOAA API.
            stationID (str): Weather station ID.
            stationName (str): Weather station name.

        Returns:
            WeatherData: Parsed weather data.
        '''
        
        props = rawData.get('properties', {})
        geometry = rawData.get('geometry', {})
        
        # Create WeatherData object
        weather = WeatherData()
        
        # Parse location
        coords = geometry.get('coordinates', [])
        latitude = coords[1] if len(coords) > 1 else None
        longitude = coords[0] if len(coords) > 0 else None
        elevation = props.get('elevation', {}).get('value')
        
        weather.location = LocationData()

        weather.location.nameID = stationID
        weather.location.name = stationName
        weather.location.latitude = latitude
        weather.location.longitude = longitude
        weather.location.elevation = elevation
        
        # Parse basic info
        weather.timestamp = props.get('timestamp')
        weather.conditions = props.get('textDescription', 'N/A')
        weather.icon = props.get('icon')
        
        # Parse temperature
        tempC = props.get('temperature', {}).get('value')
        weather.temperature = tempC if tempC is not None else 0.0
        
        print(f"{weather.location.nameID} -> {weather.conditions}: {weather.temperature}")

        # Parse dewpoint
        dewpointC = props.get('dewpoint', {}).get('value')
        weather.dewpoint = dewpointC if dewpointC is not None else 0.0
        
        print(f"  ==> dewpointC = {dewpointC}")

        # Parse wind
        windSpeed = props.get('windSpeed', {}).get('value')
        windGust = props.get('windGust', {}).get('value')
        windDirection = props.get('windDirection', {}).get('value')

        print(f"  ==> windSpeed = {windSpeed}; windGust = {windGust}")

        weather.wind = WindData()
        weather.wind.speedKph = windSpeed if windSpeed is not None else 0.0
        weather.wind.gustKph = windGust if windGust is not None else 0.0
        weather.wind.directionDegrees = windDirection if windDirection is not None else 0.0
        
        # Parse humidity
        humidityVal = props.get('relativeHumidity', {}).get('value')
        weather.humidity = humidityVal if humidityVal is not None else 0.0
        
        print(f"  ==> humidity = {humidityVal}")

        # Parse visibility
        visibilityM = props.get('visibility', {}).get('value')
        weather.visibility = VisibilityData()
        weather.visibility.meters = visibilityM if visibilityM is not None else 0.0
        
        # Parse pressure
        pressurePa = props.get('barometricPressure', {}).get('value')
        
        print(f"  ==> pressure = {pressurePa}")
        weather.pressure = pressurePa if pressurePa is not None else 0.0
        
        # Parse cloud layers
        cloudLayers = props.get('cloudLayers', [])
        
        for layer in cloudLayers:
            baseData = layer.get('base', {})
            baseMeters = baseData.get('value')
            amount = layer.get('amount', '')

            print(f"  ==> cloud baseMeters = {baseMeters}; cloud amount = {amount}")

            cloudLayer = CloudLayerData()
            cloudLayer.amount = amount if amount is not None else 0.0
            cloudLayer.baseMeters = baseMeters if baseMeters is not None else 0.0

            weather.cloudLayers.append(cloudLayer)
        
        return weather
    
    