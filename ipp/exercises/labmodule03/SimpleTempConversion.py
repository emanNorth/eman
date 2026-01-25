'''
This module contains temperature conversion functions.
'''

min_indoor_temp_F = 65.0
max_indoor_temp_F = 85.0

def isDesiredIndoorTempRange(temp, is_celsius):
    '''
    Check if the given temperature is within the desired indoor range (Fahrenheit).
    Note: 'is_celsius' parameter argument is unused in this exercise; it will be used in later exercises.
    
    Args:
        temp (float): Temperature to check.
        is_celsius (bool): True if input is Celsius, False if Fahrenheit. 
 
    Returns:
        bool: True if temp is within range, False otherwise.
    '''
    if temp >= min_indoor_temp_F and temp <= max_indoor_temp_F:
        print(f"Input temperature (F) is within desired indoor range: {temp}")
        return True   
    print(f"Input temperature (F) is outside of desired indoor range: {temp}") 
    return False

def convertTempFtoC(tempInF: float = 0.0):
    '''
    Convert Fahrenheit to Celsius.
    
    Args:
        tempInF (float): Temperature in Fahrenheit.
        
    Returns:
        float: Temperature in Celsius, rounded to 1 decimal place.
    '''
    
    celsius = round(5 / 9 * (tempInF - 32), 1)
    print(f"Temperature in Fahrenheit {tempInF} converts to {celsius} in Celsius")
    return celsius 

    
def convertTempCtoF(tempInC: float = 0.0):
    '''
    Converts Celsius to Fahrenheit.
   
    Args:
       tempInC (float): Temperature in Celsius.
    
    Returns:
        float: Temperature in Fahrenheit, rounded to 1 decimal place.
    '''
    fahrenheit = round(tempInC * (9 / 5) + 32, 1)
    print(f"Temperature in Celsius {tempInC} converts to {fahrenheit} in Fahrenheit")
    return fahrenheit
    
# Test indoor temperature range
isDesiredIndoorTempRange(70.0, False)
isDesiredIndoorTempRange(50.0, False)

 # Test temperature converters
orig_f_val = 72.0
c_val = convertTempFtoC(orig_f_val)
f_val = convertTempCtoF(c_val)
print(f"Celsius = {c_val} and Fahrenheit = {f_val}. Original Fahrenheit is {orig_f_val}")

if (orig_f_val == f_val):
    print("The temp converter works!")
else:
    print("The temp converter failed!")
    
