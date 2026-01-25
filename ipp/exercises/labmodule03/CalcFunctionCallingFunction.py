'''
This module tests calling a function from another module.
It uses the SimpleDivision module to perform  two number division and handle zero division errors. 
'''

import SimpleDivision

def divideTwoNumbers(numerator: int, denominator: int):
    '''
    A function that calls SimpleDivision.divideTwoNumbersWithExceptionHandling.
    
    Args:
        numerator (int): Number passed as the numerator value.
        denominator (int): Number passed as the denominator value.
        
    Returns:
        float: The result of the division, 0.0 if division by zero occurs.
    '''
    return SimpleDivision.divideTwoNumbersWithExceptionHandling(numerator, denominator)

# Test cases 
divideTwoNumbers(5, 2)
divideTwoNumbers(3, 0)
