
from dataclasses import dataclass, field
from typing import List, Optional

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.labmodule05.LocationData import LocationData
from ipp.exercises.labmodule05.WeatherInfoContainer import CloudLayerData, VisibilityData, WindData

@dataclass
class WeatherData():
    '''
    Holds information about a weather data.
    '''
    source: str = ""
    url: str = ""
    description: str = ""
    timestamp: str = TimeAndDateUtil.getCurrentIso8601LocalDate()
    temperature: float = 0.0
    humidity: float = 0.0
    pressure: float = 0.0
    windspeed: float = 0.0
    location: LocationData = LocationData()
    conditions: str ='N/A'
    # Can be a string or None.
    icon: Optional[str] = None
    wind: WindData = WindData()
    visibility: VisibilityData = VisibilityData()
    cloudLayers: List[CloudLayerData] = field(default_factory=list)


