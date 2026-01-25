'''
This module tests simple division calculations. 
'''

def divideTwoNumbersWithExceptionHandling(numerator: int, denominator: int):
    '''
    Tests division of two numbers and handles division by zero errors.
    
    Args:
        numerator (int): Number passed as the numerator value.
        denominator (int): Number passed as the denominator value.
        
    Returns:
        float: The result of the division, 0.0 if division by zero occurs.
    '''
    try:
        result = numerator / denominator
        print(f"Divided {numerator} by {denominator}: {result}")
        
        return result


    except ZeroDivisionError: 
        print(f"Can't divide {numerator} by {denominator}: ZeroDivisionError!")
        
        return 0.0
        