'''
This module tests string operations: concatenation, multiplication,
and formatting strings using format() and f-strings.
'''

# Test 1: String append test
# Declare a string and append additional text
salutation = "Hello, World!"
new_salutation =  salutation + " Good to meet you."

# Display results
print(new_salutation)
print("New Salutation Length: ",len(new_salutation))

# Test 2: String multiplication test
# Create repeated string using multiplication
lots_of_apples = "apples " * 2 
print(lots_of_apples)

# Test 3: String formatting test
# Create formatted string using format()
selling_apples = "{0} {1} {2}".format("i'm selling", lots_of_apples, "!")

# Display formatted strings
print(selling_apples)

# calling the capitalize() function on the string and display results
print(selling_apples.capitalize())

# Test 4: String formatting with arguments test
# Create formatted string using named arguments
school_info = "Location: {school}, {city}".format(school = "MIT", city = "Boston")

# Display results and append state to school_info
print(school_info)
school_info = f"{school_info}, MA"
print(school_info)
