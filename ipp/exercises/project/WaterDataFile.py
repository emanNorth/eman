from dataclasses import dataclass, field

from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData


@dataclass
class WaterData():
    '''
    Holds information about a single water data record.
    '''
    source: str = ""
    url: str = ""
    description: str = ""
    timestamp: str = field(default_factory=TimeAndDateUtil.getCurrentIso8601LocalDate)
    location: WaterLocationData = field(default_factory=WaterLocationData)
    waterLevel_ft: float = 0.0
    flowRate_cfs: float = 0.0            
    waterTemperature_c: float = 0.0
    variable: str = ""
    qualifier: str = ""
    unit: str = ""
    
    
   



    
 