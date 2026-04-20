import json
import requests

from ipp.exercises.project.WaterLocationDataFile import WaterLocationData
from ipp.exercises.project.NwisWaterDataParserFile import NwisWaterDataParser
from ipp.exercises.project.WaterServiceConnectorFile import WaterServiceConnector


class NwisWaterServiceConnector(WaterServiceConnector): 
    '''
    Service connector for retrieving USGS NWIS water data.

    Inherits from WaterServiceConnector and provides 
    implementations of _createRequestUrl() and _getLatestWaterData()
    Uses NWIS OGC API.
    '''      
    def __init__(self):
        '''Initialize the NWIS connector with a NWIS specific data parser.'''
        super().__init__(dataParser = NwisWaterDataParser())
          
    def _createRequestUrl(self, siteID: str = None, locData: WaterLocationData = None, parameter_code: str = None):
        '''
        Construct the URL to request the latest water data for a specific site.

        Args:
            siteID (str): The NWIS site identifier.
            locData (LocationData, optional): Location data object (not used here).

        Returns:
            str: The fully formed URL to request the latest observations.
        '''
        # NWIS API endpoint for latest observations by site
        
        
        # ask for all three parameter codes at once (comma‑separated)
        parameter_list = "00060,00065,00010"
            
        url = (
            f"{self.baseUrl}/collections/latest-continuous/items"
            f"?monitoring_location_id={siteID}"
            f"&parameter_code={parameter_list}"
            f"&limit=10"
            f"&f=json"
        )

        print(">>> REQUEST URL:", url)
        return url     
        
    def _getLatestWaterData(self, requestUrl: str = None, siteID: str = None, locData: WaterLocationData = None) -> dict:
        '''
        Fetch raw water data from USGS NWIS API for a given site.

        Args:
            requestUrl (str): The NWIS API URL for the site.
            siteID (str): The site identifier (optional, for logging).
            locData (LocationData, optional): Location information to attach to response.

        Returns:
            dict: Raw water data from NWIS with location info added, or None on failure.
        '''       
        try:
            print(f"Requesting current water data observations: {requestUrl}")
            
            # Make HTTP GET request using the active session
            waterResponse = self.clientSession.get(requestUrl, timeout = self.requestTimeout)
            
            # Check for unsuccessful HTTP response
            if waterResponse.status_code != 200:
                print(f"Failed to get water data. Response code: HTTP {waterResponse.status_code}")
                return None
            
            # Parse JSON response
            responseData = waterResponse.json()
            
            # NWIS API returns GeoJSON like data (FeatureCollection).
            
            # Remove JSON-LD specific fields (we won't need them)
            latestRawData = responseData.copy()
            latestRawData.pop('@context', None)
            
            print(f"Successfully retrieved raw water data")
            return latestRawData
        
        # Handle request timeout    
        except requests.exceptions.Timeout:
            print(f"Request timed out")
            return None
        
        # Handle other HTTP related errors
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
        # Handle unexpected JSON structure
        except (KeyError, IndexError) as e:
            print(f"Unexpected response format: {e}")
            return None
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        
        





            
            

           
                  
            
            
    
          

            
        
        