import datetime
import time


class TimeAndDateUtil():
    '''
    A utility class with class methods for converting of current time / date to milliseconds
    since the Epoch, and for converting current time or a given time to an ISO 8601 string.
    '''
    
    # Allows to call the method without creating an instance. 
    @classmethod
    def getCurrentLocalDateInMillis(cls):
        '''
        Returns the current time in milliseconds since the Epoch.
        
        Args:
            None
        
        Returns:
            int: The current time in milliseconds since the Epoch.
        '''
        current_millis = int(time.time() * 1000)

        return current_millis
    
    
    # Allows to call the method without creating an instance. 
    @classmethod
    def getCurrentIso8601LocalDate(cls, ignoreMillis: bool = True):
        '''
        Converts current time into ISO 8601 string.
        
        Args:
            ignoreMillis (bool): If True, removes microseconds from datetime object
            before converting to ISO string.
        
        Returns:
            str: ISO 8601 formatted time and date string based on current time.
        '''
        
        # Convert milliseconds to seconds
        current_date = datetime.datetime.fromtimestamp(cls.getCurrentLocalDateInMillis() / 1000)
        
        if ignoreMillis:
            # Removes microseconds from display.
            current_date = current_date.replace(microsecond=0)
        
        # Converts current time into ISO 8601 string.
        formatted_date = current_date.isoformat()

        return formatted_date
    

    # Allows to call the method without creating an instance. 
    @classmethod
    def getIso8601DateFromMillis(cls, millis: int = 0, ignoreMillis: bool = True):
        '''
        Converts a given time into ISO 8601 string.
        
        Args:
            millis (int): Time in milliseconds since the Epoch (must be >= 0)
            ignoreMillis (bool): If True, removes microseconds from datetime object
            before converting to ISO string.

        Returns:
            str: ISO 8601 formatted time and date string,
            based on the passed in milliseconds since the Epoch.
        '''
    
        if millis < 0:
            raise ValueError("Milliseconds must be >= 0")

        # Convert milliseconds to seconds
        any_date = datetime.datetime.fromtimestamp(millis / 1000)

        if ignoreMillis:
            # Removes microseconds from display.
            any_date = any_date.replace(microsecond=0)
        
        # Converts datetime object into ISO 8601 string.
        return any_date.isoformat()
    




