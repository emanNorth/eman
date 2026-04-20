from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData

from ipp.exercises.project.WaterDataParserFile import WaterDataParser


class NwisWaterDataParser(WaterDataParser):
    '''
    This class transforms raw NWIS JSON response data into a structured
    WaterData object by extracting relevant water fields.
    '''
    def __init__(self):
        ''' Initialize the NWIS water data parser.'''
        super().__init__()

    def _createWaterDataFromRawData(self, rawData: dict, siteID: str, siteName: str) -> WaterData:
        '''
        Parse raw NWIS water JSON data into a WaterData object.

        Args:
            rawData (dict): Raw JSON data from NWIS API.
            siteID (str): The ID of the water monitoring location identifier.
            siteName (str): The name of the water monitoring location identifier.

        Returns:
            WaterData: Parsed water data.
        '''
        # Create Water Data object
        water = WaterData()
        
        # Parse location (comes from inputs, NOT JSON)
        water.location = WaterLocationData()
        water.location.siteID = siteID
        water.location.siteName = siteName
        
        features = rawData.get("features", [])
        if not features:
            return water
        
        # Track the most recent timestamp across all features
        latest_time = ""
        
        # Note:
        # The API returns multiple readings per parameter (flow, level, temp), each at different times. 
        # Goal is to keep the most recent reading for each parameter_code
        # Group features by parameter_code, keeping only the latest per code
        
        # Loop through every feature and we extract: 
        # code → what type of data (flow, level, temp), time → when it was recorded
        latest_by_code = {}
        for f in features:
            props = f.get("properties", {})
            code = props.get("parameter_code", "")
            time = props.get("time", "")
            
            # Store this feature if it's the first time seeing this parameter_code
            # or if this feature has a newer timestamp than the one already stored
            if code not in latest_by_code or time > latest_by_code[code].get("properties", {}).get("time", ""):
                latest_by_code[code] = f
            
            if time > latest_time:
                latest_time = time
        
        water.timestamp = latest_time
        
       # Extract each parameter type
        for code, feature in latest_by_code.items():
            props = feature.get("properties", {})
            value = props.get("value")
            value = float(value) if value is not None else 0.0
            
            if code == "00060":
                water.flowRate_cfs = value
            elif code == "00065":
                water.waterLevel_ft = value
            elif code == "00010":
                water.waterTemperature_c = value
       
       # Capture unit/qualifier from last processed 
        water.unit = props.get("unit_of_measure", "")
        water.qualifier = props.get("qualifier", "") 
       
       # Parse geometry from first feature if available
        first_feature = features[0]
        geometry = first_feature.get("geometry") or {}
        coords = geometry.get("coordinates", [])
        if len(coords) >= 2:
            water.location.longitude = coords[0]
            water.location.latitude = coords[1]
        
        water.description = f"NWIS multi-parameter reading for {siteID}"
        
        return water
    

  

    

    
    
    
    
    
    
    
    
    
    
  




        

        

       

        

   
        
        
        
        

                
                
       
    
    
    
    

        

        

    
            

            

          

    

       

     
