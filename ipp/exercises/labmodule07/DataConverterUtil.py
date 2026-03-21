import json
import logging
from json import JSONEncoder
from typing import Optional

from ipp.exercises.labmodule07.FileUtil import FileUtil
from ipp.exercises.labmodule05.WeatherData import WeatherData
from ipp.exercises.labmodule07.StatsData import StatsData
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherInfoContainer import CloudLayerData, VisibilityData, WindData


class JsonDataEncoder(JSONEncoder):
    '''
    Custom JSON encoder to convert objects into dictionaries.
    '''
    def default(self, o):
        '''
        Convert object attributes to a dictionary.

        Args:
            o (object): Any Python object.

        Returns:
            dict: Object attributes as a dictionary.
        '''
        return o.__dict__


class DataConverterUtil:
    '''
    Utility class for converting WeatherData and StatsData objects to and from JSON
    and reading and writing them to files.
    '''
    def __init__(self):
        ''' Initialize the DataConverterUtil class.'''
        pass
    
    # The method belongs to the class, not an object
    @classmethod
    def _createObjectFromDict(cls, data_dict: dict, obj_class):
        '''
        Create an object of obj_class and populate its attributes from a dictionary.

        Args:
            data_dict (dict): Dictionary of attribute values.
            obj_class (class): The class type to instantiate.

        Returns:
            object: Instantiated object with attributes set.
        '''
        # Creates an empty object of the class
        obj = obj_class()
        # Call _updateData to populate the dict
        cls._updateData(data_dict, obj)
        return obj
    
    
    @classmethod
    def _updateData(cls, jsonStruct: dict, obj) -> None:
        '''
        Update an object's attributes from a dictionary if the keys match.

        Args:
            jsonStruct (dict): Dictionary of attribute values.
            obj (object): Object to update.
        '''
        # vars() is a built in function. When we pass an object to it: 
        # It returns a dictionary of all the object’s attributes and their current values.
        varStruct = vars(obj)
        
        # It loops through every key in the dictionary passed in.
        for key in jsonStruct:
            # Check if this key actually exists as an attribute in the object.
            if key in varStruct:
                # If the key exists in the object, update the value using setattr.
                setattr(obj, key, jsonStruct[key])
            else:
                logging.warning("JSON data contains key not mappable to object: %s", key)
    
              
    @classmethod
    def weatherDataToJson(cls, weatherData: WeatherData) -> str:
        '''
        Convert a WeatherData object to a JSON string.

        Args:
            weatherData (WeatherData): WeatherData object to convert.

        Returns:
            str: JSON string representation of WeatherData.
        '''
        # Use our custom encoder
        return json.dumps(weatherData, cls=JsonDataEncoder, indent=2)
    
    
    @classmethod
    def jsonToWeatherData(cls, json_string: str) -> Optional[WeatherData]:
        '''
        Convert a JSON string into a WeatherData object.

        Handles nested objects and lists like location, wind, visibility, and cloudLayers.

        Args:
            json_string (str): JSON string to parse.

        Returns:
            WeatherData: Parsed WeatherData object if successful, else None.
        '''
        try:
            # Converts the JSON string into a Python dictionary
            data_dict = json.loads(json_string)
            # Creates an empty WeatherData object to fill with values from the dictionary
            weatherData = WeatherData()
            
            # Map of nested object keys to their class types
            nested_objects = {
                'location': LocationData,
                'wind': WindData,
                'visibility': VisibilityData
            }
            
            # Handle nested objects
            for key, obj_class in nested_objects.items():
                if key in data_dict and isinstance(data_dict[key], dict):
                    # Create an empty object (like WindData())
                    nested_obj = obj_class()
                     # Fill that object using the dictionarY
                    cls._updateData(data_dict[key], nested_obj)
                    setattr(weatherData, key, nested_obj)
                
                    # Delete nested object keys after processing to prevent _updateData() from
                    # overwriting our properly instantiated objects with plain dictionaries
                    del data_dict[key]
            
            # Handle CloudLayerData list
            # Check if "cloudLayers" exists and is a list
            if 'cloudLayers' in data_dict and isinstance(data_dict['cloudLayers'], list):
                weatherData.cloudLayers = [
                    cls._createObjectFromDict(layer_dict, CloudLayerData)
                    for layer_dict in data_dict['cloudLayers']
                ]

                # Delete nested object keys after processing to prevent _updateData() from
                # overwriting our properly instantiated objects with plain dictionaries
                del data_dict['cloudLayers']
            
            # Update remaining simple properties
            cls._updateData(data_dict, weatherData)
            
            return weatherData
            
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON to WeatherData: {e}")
            return None
        # Catches any other errors (not just JSON errors).
        except Exception as e:
            logging.error(f"Error converting JSON to WeatherData: {e}")
            return None
     
       
    @classmethod
    def statsDataToJson(cls, statsData: StatsData) -> str:
        '''
        Convert a StatsData object to a JSON string.

        Args:
            statsData (StatsData): StatsData object to convert.

        Returns:
            str: JSON string representation of StatsData.
        '''
        # Converts the object into a JSON string using the custom encoder.
        return json.dumps(statsData, cls=JsonDataEncoder, indent=2)
    
    
    @classmethod
    def jsonToStatsData(cls, json_string: str) -> Optional[StatsData]:
        '''
        Convert a JSON string into a StatsData object.

        Args:
            json_string (str): JSON string to parse.

        Returns:
            StatsData: Parsed StatsData object if successful, else None.
        '''
        try:
            # Convert JSON string into Python dictionary.
            data_dict = json.loads(json_string)
            
            # Create an empty StatsData object
            statsData = StatsData()
            # Fill the object with values from the dictionary using _updateData method
            cls._updateData(data_dict, statsData)
            
            return statsData
            
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON to StatsData: {e}")
            return None
        
        # Catches any other errors
        except Exception as e:
            logging.error(f"Error converting JSON to StatsData: {e}")
            return None
    
    
    @classmethod
    def writeStatsDataToFile(cls, statsData: StatsData, fileName: str) -> bool:
        '''
        Convert StatsData to JSON and write to a file.

        Args:
            statsData (StatsData): Object to write.
            fileName (str): Path to the file.

        Returns:
            bool: True if successful, False otherwise.
        '''
        try:
            json_string = cls.statsDataToJson(statsData)
            return FileUtil.writeTextFile(fileName, json_string)
        
        except Exception as e:
            logging.error(f"Error writing StatsData to file '{fileName}': {e}")
            return False 
        
          
    @classmethod
    def readStatsDataFromFile(cls, fileName: str) -> Optional[StatsData]:
        '''
        Read JSON from file and convert to StatsData object.

        Args:
            fileName (str): Path to the file.

        Returns:
            StatsData: Parsed object if successful, else None.
        '''
        try:
            json_string = FileUtil.readTextFile(fileName)

            if json_string is not None:
                return cls.jsonToStatsData(json_string)
            return None
        
        except Exception as e:
            logging.error(f"Error reading StatsData from file '{fileName}': {e}")
            return None
     
      
    @classmethod
    def writeWeatherDataToFile(cls, weatherData: WeatherData, fileName: str) -> bool:
        '''
        Convert WeatherData to JSON and write to a file.

        Args:
            weatherData (WeatherData): Object to write.
            fileName (str): Path to the file.

        Returns:
            bool: True if successful, False otherwise.
        '''
        try:
            json_string = cls.weatherDataToJson(weatherData)
            return FileUtil.writeTextFile(fileName, json_string)
        
        except Exception as e:
            logging.error(f"Error writing WeatherData to file '{fileName}': {e}")
            return False
    
    
    # The method belongs to the class, not an object
    @classmethod
    def readWeatherDataFromFile(cls, fileName: str) -> Optional[WeatherData]:
        '''
        Read JSON from file and convert to WeatherData object.

        Args:
            fileName (str): Path to the file.

        Returns:
            WeatherData: Parsed object if successful, else None.
        '''
        try:
            json_string = FileUtil.readTextFile(fileName)
            if json_string is not None:
                return cls.jsonToWeatherData(json_string)
            return None
        
        except Exception as e:
            logging.error(f"Error reading WeatherData from file '{fileName}': {e}")
            return None
        
        
        
        
    
   


