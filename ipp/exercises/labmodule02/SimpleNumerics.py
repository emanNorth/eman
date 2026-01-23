'''
This module tests the use of Pythonic numeric types including integers, floats,
absolute values, and basic type conversions.
'''

# Test 1: int
# Declare integer variables 
# alt_large_number: same as large_number using underscore formatting
age = 25 
count = -10 
large_number = 3000000
alt_large_number = 3_000_000 

# Display integer values
print(f"Age: {age}; Count: {count}; Large #: {large_number}; Alt Large #: {alt_large_number}")

# Test 2: float
# Declare float variables
# sci_value: scientific notation 
price = 25.99 
temperature = 10.99 
sci_value = 3.1e-5 

# Display float values
print(f"Price: {price}; Temperature: {temperature}; Scientific Value: {sci_value}")

# Test 3: abs() and conversion
# Calculate absolute value
absolute_count = abs(count)

# Display absolute value
print(f"Absolute Count: {absolute_count}")

# Convert float to int and back to float
price = 15.99 
price_no_cents = int(price) 
price_with_cents = float(price_no_cents) 

# Display conversion results
print(f"Price: {price}; Price - no cents: {price_no_cents}; Price - back to cents: {price_with_cents}")
