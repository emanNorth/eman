import sys
import struct
from array import array 

values = [3.01, 5.01, 7.01, 9.01]

def displaySizingInfo(val):
    ''' 
    Shows how a float is stored in memory, including it's size, Hex form, and binary IEEE 754 representation.
        
    Args: 
        val (float): the floating point value to inspect.
            
    Returns:
        None.
    '''
        
    # Get memory size in bytes
    sample_bits = sys.getsizeof(val)
        
    # Get Hex representation of float 
    sample_hex = val.hex()
        
    # Get binary representation of float (IEEE 754)
    sample_bin = struct.unpack("!I", struct.pack("!f", val))[0]
        
    print(
        "-> Sizing info: value =", val, ", bytes =", sample_bits,
        ", hex =", sample_hex, ", binary=", f"{sample_bin:032b}"
        )
        
def createItemPriceArrayUsingFloats():
    '''
    Demonstrate basic operations on float array, including creation, 
    display and iteration.
            
    Actions:
        Creates a float array from the values list. 
        Display the array object directly.
        Display the array converted to a Python list.
        Iterate over the array and pass each value to displaySizingInfo().
                
            
    Returns:
        array: A float array created from the values list. 
    '''
            
    # Create a float array from a value list
    item_prices = array("f", values)
            
    # Display the array object directly
    print(item_prices)
            
    # Display the array converted to a Python list
    print(item_prices.tolist())
            
    # Iterate over the array and passes each value to displaySizingInfo()
    for i, val in enumerate(item_prices):
        displaySizingInfo(val)
            
    # Return the float array created from values list     
    return item_prices

def createItemPriceArrayUsingDoubles():
    '''
    Demonstrate basic operations on double array, including creation, 
    display and iteration.
            
    Actions:
        Creates a double array from the values list. 
        Display the array object directly.
        Display the array converted to a Python list.
        Iterate over the array and pass each value to displaySizingInfo()
                
            
    Returns:
        array: A double array created from the values list. 
    '''
    
    # Create a double array from a value list
    item_prices = array("d", values)
    
    # Display the array object directly
    print(item_prices)
            
    # Display the array converted to a Python list
    print(item_prices.tolist())
    
    # Iterate over the array and passes each value to displaySizingInfo()
    for i, val in enumerate(item_prices):
        displaySizingInfo(val)
            
    # Return the double array created from values list     
    return item_prices
    
def main():
    createItemPriceArrayUsingFloats()
    createItemPriceArrayUsingDoubles()
        
if __name__ == "__main__":
    sys.exit(main())
         
        