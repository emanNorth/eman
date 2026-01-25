'''
This module tests importing and calling functions from another module. 
'''

import sys 
import SimpleTempConversion

def doWork():
    '''
    A function that demonstrates using functions from SimpleTempConversion module.
    
    Actions:
        Converts a Fahrenheit temperature to Celsius.
        Converts the Celsius temperature back to Fahrenheit.
        Checks if the original Fahrenheit temperature is within the desired indoor range.
    
    '''
    f_val = 72.0
    
    # Convert Fahrenheit to Celsius
    c_val = SimpleTempConversion.convertTempFtoC(f_val)
    print(f"Converted temperature values: F = {f_val}; C = {c_val}")
    
    # Convert Celsius back to Fahrenheit
    f_val_back = SimpleTempConversion.convertTempCtoF(c_val)
    print(f"Converted back from C to F: {f_val_back}")
    
    # Check if Fahrenheit temperature is within the desired indoor range
    SimpleTempConversion.isDesiredIndoorTempRange(f_val, is_celsius=False)   
    
def main():
    '''
    A function that calls another function doWork()
    
    Actions:
        Prints a greeting.
        Calls doWork() to demonstrate module function usage.
    
    Returns:
        int: Exit code 0
    
    '''
    print("Hello, world!")
    doWork()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
    
