'''
SimplePlatformInfo.py 
A module to test basic functionality of Python's platform module.
Print system name and machine type
'''

# Import the platform module
import platform

# Call platform functions
# Get the operating system name 
system_name = platform.system()

# Get the CPU architecture
machine_type = platform.machine()

# Display the results
print(f"System: {system_name}; Machine: {machine_type}")