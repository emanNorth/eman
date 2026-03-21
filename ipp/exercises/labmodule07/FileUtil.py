import os
import json

from typing import Dict, List, Optional, Union

class FileUtil:
    ''' Utility class for handling file and directory operations.'''
    def __init__(self):
        ''' Initialize the FileUti class.'''
        pass
    
    # The method belongs to the class, not an object
    @classmethod
    def readTextFile(cls, fileName: str, encoding: str = 'utf-8') -> Optional[str]:
        '''
        Reads text content from a file.

        Checks if the file exists before trying to read.
        Handles file errors such as missing files,
        permission issues, and encoding problems.

        Args:
            fileName (str): The path and name of the file to read.
            encoding (str): The encoding format to use (default is 'utf-8').

        Returns:
            Optional[str]: The file content as a string if successful,
                           otherwise None.
        '''
        try:
            # Calls another method in the class to checks if file exists before reading
            if FileUtil.fileExists(fileName):
                # with ensures the file is automatically closed.
                with open(fileName, 'r', encoding=encoding) as f:
                    return f.read()
            else:
                print(f"Can't read text file. File doesn't exist: {fileName}")
        # Handles case where file is missing
        except FileNotFoundError:
            print(f"Error: File '{fileName}' not found")
            return None
        # Handles case where there is no permission to read the file.
        except PermissionError:
            print(f"Error: Permission denied for '{fileName}'")
            return None
        # Handles case where file encoding doesn’t match
        except UnicodeDecodeError:
            print(f"Error: Unable to decode '{fileName}' with encoding '{encoding}'")
            return None
        # Catches any other unexpected error, e stores the error message.
        except Exception as e:
            print(f"Error reading file '{fileName}': {e}")
            return None
        
    # The method belongs to the class, not an object
    @classmethod
    def writeTextFile(cls, fileName: str, content: str, encoding: str = 'utf-8', mode: str = 'w') -> bool:
        '''
        Writes text content to a file.

        Handles file writing, permission issues, and unexpected errors.
        Opens the file using the given mode (default is 'w' for write).

        Args:
            fileName (str): The path and name of the file to write.
            content (str): The text content to write to the file.
            encoding (str): The encoding format to use (default is 'utf-8').
            mode (str): File open mode ('w' for write, 'a' for append, etc.).

        Returns:
            bool: True if writing succeeded, False if an error occurred.
        '''
        
        try:
            # with ensures the file is automatically closed.
            with open(fileName, mode, encoding = encoding) as f:
                f.write(content)
            return True
        # Handles case where there is no permission to write in the file. File may be read-only 
        except PermissionError:
            print(f"Error: Permission denied for '{fileName}'")
            return False
        # Catches other I/O errors, e.g., disk full, network issues
        except IOError as e:
            print(f"Error writing to file '{fileName}': {e}")
            return False
        # Catches any other unexpected error, e stores the error message.
        except Exception as e:
            print(f"Unexpected error writing file '{fileName}': {e}")
            return False
    
    # The method belongs to the class, not an object
    @classmethod
    def fileExists(cls, fileName: str) -> bool:
        '''
        Checks if a file exists.

        Args:
            fileName (str): The path and name of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        '''
        return os.path.isfile(fileName)
    
    # The method belongs to the class, not an object
    @classmethod
    def directoryExists(cls, dirName: str) -> bool:
        '''
        Checks if a directory exists.

        Args:
            dirName (str): The path of the directory to check.

        Returns:
            bool: True if the directory exists, False otherwise.
        '''
        return os.path.isdir(dirName)
