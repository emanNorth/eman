class CalculationsUtil():
    '''
    A utility class with class methods for temperature conversion and division.
    '''
    
    # This method can be called on the class itself, not an instance
    @classmethod
    def convertTempFtoC(cls, tempInF: float = 0.0):
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
    

    # This method can be called on the class itself, not an instance
    @classmethod
    def convertTempCtoF(cls, tempInC: float = 0.0):
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
    
    
    # This method can be called on the class itself, not an instance
    @classmethod
    def divideTwoNumbers(cls, numerator: float, denominator: float):
        '''
        Tests division of two numbers and handles division by zero errors.
    
        Args:
            numerator (float): Number passed as the numerator value.
            denominator (float): Number passed as the denominator value.
        
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
   