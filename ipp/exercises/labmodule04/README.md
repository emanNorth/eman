# Programming in Python - An Introduction: Lab Module 04

### Description

Briefly describe the objectives of the Lab Module:

1) Demonstrate how float and double arrays work in Python, including creation, display, iteration, and memory representation (including size, Hex, and binary representation).  

2) Demonstrate how a list converted to a set, and perform basic set operations including, merge sets together, add items, and remove items.

3) Demonstrate how a dictionary created from lists, and perform basic operations incluing, merges multiple dictionaries, adds key value pairs, and remove keys to a existing dictionary.


### Exercise Activities

List the actions you took in implementing the Lab Module:

1) Created the `SimpleArrays.py` module with functions to display float and double arrays, print the arrays, and show size, hex, and binary representations of each element. 

Observations: 
**Float array values:**  
The float values are odd because 32 bit floats cannot exactly represent some decimal fractions. Stored as the closest binary approximation, this results in rounding differences when printed.  

**Double array values:**  
The double values represented the way they are because 64 bit doubles have higher precision, though very small rounding errors can still occur due to binary floating point representation.


2) Created the `simpleSet.py` module with functions to convert a list to a set, merged two sets together into a single set, added and removed new and duplicate items to a set.

Observations:
**In `createSetFromNames` function**:
Converts a list to a set, which automatically removes duplicate values, because sets don't allow duplicates. 
**In `mergeSetNames` function**:
Each set is merged using union (|) operator. The result is one set with only unique values.
*args: allows the function to accept multiple positional arguments (any number of sets), 
and packing them as a tuple so the function can loop over them.
**In `addItemsToSet` function**:
Items added using set.add(), if one or more items added of the same name, nothing changes as sets ignore duplicates. 
**In `removeItemsFromSet` function**:
Items removed using set.discard(), if an item doesn't exist, no error is raised. 


3) Created the `SimpleDictionaries.py` module with functions to create a dictionary from lists, merges multiple dictionaries into a single dictionary, adds key value pairs, and removes keys.

Observations:
**`createDictionaryFromKeyValuePairs` function**: potential issues in code:
- Duplicate keys: If a key appears more than once, the dictionary overwrites the previous value, keeping only the last one. Fix: Store values in a list for each key.
- Manual indexing: Using an index to access elements works but is unnecessary. Fix: Using zip() is a cleaner way to write the code.
- Silent failure on wrong input: If the lists are of different lengths or None, the function only prints a message and returns None. It doesn’t stop or handle the error. Fix: Raise an exception.
**`mergeDictionaries` function**:
- Merges multiple dictionaries into a single dictionary. It loops through each dictionary passed to the function and adds its key value pairs to one main dictionary. 
- *args allows any number of dictionary arguments. All the dictionaries passed in are stored together as a tuple, which lets the function loop through them and merge them.
**`addItemsToDictionary` function**:
- Function adds key value pairs to a dictionary using any number of named arguments.
- If one or more items added at the same name? If a key appears more than once, the dictionary overwrites the previous value, keeping only the last one.
**`removeItemsFromDictionary` function**:
- Removes one or more keys from a dictionary using any number of keys as arguments, then removes each key using pop so the function doesn’t raise an error if the key isn’t found.
- if an item removed doesn't exist in the dictionary: The function uses pop(key, None), which means that if the key is not in the dictionary, it just does nothing and continues without raising an exception.


### Unit and/or Integration Tests Executed

List the tests you exercised in validating your functionality for the Lab Module:

1) Ran `SimpleArrays.py` from within my IDE (using the Run icon) to create float and double arrays, verified that arrays were created and displayed, and took note of memory size, hex, and binary representations to observe precision differences.

2) Ran `simpleSet.py` to create a set from a list, verified that sets were created and displayed, merged sets together and tested adding or removing one existing and one new item to verify set behavior. 

3) Ran `SimpleDictionaries.py` to create a dictionary from lists, merged multiple dictionaries, added new key value pairs, and removed keys. Verified that all functions worked correctly, including handling duplicate keys and removing non existent keys.

EOF.
