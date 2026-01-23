'''
This module tests some simple sequence operations and iterations over strings,
lists, tuples, and ranges.
'''

# Test 1: string iteration
# Declare string and iterate over characters
name = "Batman"
for c in name: 
    print(c)
print()

# Test 2: list iteration and manipulation
# Declare list and append new item
class_items = ["notebook","pen","power supply"]
class_items.append("Laptop")

# Iterate over list items and display list contents
for item in class_items:
    print(f"Item: {item}")
print()

# Test 3: tuple iteration (and failed manipulation)
# Declare immutable tuple
immutable_class_items = ("notebook", "pen", "power supply")

# Iterate over tuple items and display tuple contents
for item in immutable_class_items:
    print(f"Item: {item}")

# Attempt to modify tuple and handle exception
try: 
    immutable_class_items.append("Coffee")
except: 
    print(f"Tuples are immutable! Can't append.")

# Display tuple again to confirm immutability and exception preventing error  
for item in immutable_class_items:
    print(f"Item: {item}")
print()

# Test 4: rangeiteration
# Iteration over simple range
for i in range(7):
    print(f"simple range val: {i}")
print()

# Iteration over bounded range
for i in range(3,7):
    print(f"bounded range val: {i}")
print()

# Iteration over stepwise range
for i in range(0,7,3):
    print(f"Stepwise range val: {i}")





