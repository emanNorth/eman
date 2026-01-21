'''
SimpleSystemInfo.py 
A module to test basic functionality of Python's sysm module.
Print Python version and version data
'''
# Import the sys module
import sys 

# Call the sys functions
# Get the Python version as a readable string
python_version = sys.version

# Get the Python version as a structured data 
version_data = sys.version_info

# Display results 
print(f"Python Version: {python_version}")
print(f"Version Info: {version_data}")