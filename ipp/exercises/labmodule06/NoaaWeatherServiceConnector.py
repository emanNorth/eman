import json
import requests

from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule06.NoaaWeatherDataParser import NoaaWeatherDataParser
from ipp.exercises.labmodule06.WeatherServiceConnector import WeatherServiceConnector

class NoaaWeatherServiceConnector(WeatherServiceConnector):
    '''
    Service connector for retrieving NOAA weather data.

    Inherits from WeatherServiceConnector and provides 
    implementations of _createRequestUrl() and _getLatestWeatherData()
    specific to NOAA's weather API.
    '''

    def __init__(self):
        '''Initialize the NOAA connector with a NOAA-specific data parser.'''
        super().__init__(dataParser = NoaaWeatherDataParser())
 
    def _createRequestUrl(self, stationID: str = None, locData: LocationData = None):
        '''
        Construct the URL to request the latest weather data for a specific station.

        Args:
            stationID (str): The NOAA station identifier.
            locData (LocationData, optional): Location data object (not used here).

        Returns:
            str: The fully formed URL to request the latest observations.
        '''
        # NOAA API endpoint for latest observations by station
        # GET https://api.weather.gov/stations/{station_id}/observations/latest
        return f"{self.baseUrl}/stations/{stationID}/observations/latest"

    def _getLatestWeatherData(self, requestUrl: str = None, stationID: str = None, locData: LocationData = None) -> dict:
        '''
        Fetch raw weather data from NOAA for a given station.

        Args:
            requestUrl (str): The NOAA API URL for the station.
            stationID (str): The station identifier (optional, for logging).
            locData (LocationData, optional): Location information to attach to response.

        Returns:
            dict: Raw weather data from NOAA with location info added, or None on failure.
        '''
        try:
            print(f"Requesting current weather observations: {requestUrl}")
            
            # Make HTTP GET request using the active session
            weatherResponse = self.clientSession.get(requestUrl, timeout = self.requestTimeout)
            
            # Check for unsuccessful HTTP response
            if weatherResponse.status_code != 200:
                print(f"Failed to get weather data. Response code: HTTP {weatherResponse.status_code}")
                return None
            
            # Parse JSON response
            responseData = weatherResponse.json()
            
            # Add location information to the response
            # (NOAA may not include this, so it prob needs to be added)
            responseData['location'] = {
                'city': locData.city,
                'state': locData.region,
                'country': locData.country
            }
            # Add geometry coordinates
            responseData['geometry'] = {
                'coordinates': [locData.longitude, locData.latitude]
            }

            # Remove JSON-LD specific fields (we won't need them)
            latestRawData = responseData.copy()
            latestRawData.pop('@context', None)
            
            print(f"Successfully retrieved raw weather data")
            return latestRawData
        
        # Handle request timeout    
        except requests.exceptions.Timeout:
            print(f"Request timed out")
            return None
        
        # Handle other HTTP-related errors
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
        # Handle unexpected JSON structure
        except (KeyError, IndexError) as e:
            print(f"Unexpected response format: {e}")
            return None