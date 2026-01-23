'''
This module tests simple calculations using integers and floats,
including addition, subtraction, multiplication, and remainders.
'''

# Test 1: simple int calcs
# Declare picked_apples, bagged_apples
picked_apples = 30
bagged_apples = 7

# Calculate available_apples as sum
available_apples = picked_apples + bagged_apples

# Declare consumed_apples
consumed_apples = 5

# Calculate remaining_apples as available minus consumed
remaining_apples = available_apples - consumed_apples

# Display results
print(f"Apples collected. Picked: {picked_apples}; Bagged: {bagged_apples}; Available: {available_apples}")
print(f"After eating some apples. Consumed: {consumed_apples}; Remaining: {remaining_apples}")

# Test 2: simple product calcs
# Declare shopping_trips, apples_per_trip
shopping_trips = 3 
apples_per_trip = 4 

# Calculate purchased_apples as product
purchased_apples = shopping_trips * apples_per_trip

# Calculate total_apples as sum
total_apples = remaining_apples + purchased_apples

# Display results
print(f"Apple shopping. Shopping Trips: {shopping_trips}; Apples per Trip: {apples_per_trip}; Purchased: {purchased_apples} ")
print(f"Total Apples: {total_apples}")

# Test 3: remainders
# Declare days_per_week 
days_per_week = 7

# Calculate daily_apples_for_week = int(total_apples / days_per_week)
daily_apples_for_week = int(total_apples / days_per_week)

# Calculate leftovers using modulus and subtraction
left_over_apples_mod =  total_apples % days_per_week
left_over_apples_sub = total_apples - (daily_apples_for_week * days_per_week)

# Display results
print(f"Daily apple consumption. Total: {total_apples}; Apples per day: {daily_apples_for_week} ")
print(f"Leftovers. Using modulus: {left_over_apples_mod}; Using subtraction: {left_over_apples_sub} ")

