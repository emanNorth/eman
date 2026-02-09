import sys

pets_names = ["dog", "owl", "fox", "goat", "donkey", "skink","python","tarantula", "fox", "owl", "skink"]
pets_locations = ["sea", "mountain", "river", "earth", "pond", "donkey", "river", "grass", "cave", "earth", "pond"]

def createDictionaryFromKeyValuePairs(names, locations):
    ''' 
    Shows how to create a dictionary of names and locations..
        
    Args: 
        names (list): List of names (keys)
        locations (list): List of locations (values)
            
    Returns:
       (dictionary): Dictionary with names as keys and locations as value pairs. 
    '''
    itemDict = None

    # Checks if both lists are not None and have the same length.
    if names is not None and locations is not None:
        if len(names) == len(locations):
            # Creates an empty dictionary
            itemDict = {}

            print(f"Length of item names and item locations are the same. Creating dictionary of size {len(names)}")
            
            # Iterates through names, using an index to get the corresponding element from locations
            index = 0
            for n in names:
                itemDict[n] = locations[index]
                index = index + 1
        else:
            print(f"Can't create dictionary of names and locations. Lengths of lists are different.")
            
    # Returns the dictionary
    return itemDict


def mergeDictionaries(*args):
    """
    Merges two or more dictionaries into a single dictionary.

    Args:
        *args: One or more dictionaries passed into the function.

    Returns:
        dict: A single dictionary containing all key value pairs
              from the input dictionaries.
    """
    # Create an empty dictionary 
    mergedDict = dict()

    # Check that at least one dictionaries was passed
    if args and len(args) > 0:
        # Loop through each dictionary argument
        for arg in args:
            if arg is not None:
                print(f"Merging dictionary into main dictionary with {len(arg)} items.")
                
                # Merge current dictionary into mergedDict
                mergedDict = mergedDict | arg
                
                print(f"Newly merged dictionary: {mergedDict}")

        return mergedDict
    else:
        print("No dictionaries included in arguments to function. Ignoring.")

    return mergedDict


def addItemsToDictionary(itemDict, **kwargs):
    """
    Adds one or more key value pairs to a given dictionary.

    Args:
        itemDict (dict): The dictionary to add items to.
        **kwargs: One or more key value pairs to be added.

    Returns:
        dict: The updated dictionary with the new items added.
    """
    
    # Check that the dictionary exists 
    if itemDict is not None:
        # Check if any keyword arguments passed
        if kwargs and len(kwargs) > 0:
            # Loop through each key value pair
            for k, v in kwargs.items():
                # Make sure both key and value are valid
                if k is not None and v is not None:
                    print(f"Adding key {k} and value {v} to dictionary of length {len(itemDict)} items.")
                    itemDict[k] = v
                    print(f"New dictionary length: {len(itemDict)}")

    # Return the dictionary
    return itemDict


def removeItemsFromDictionary(itemDict, *args):
    """
    Removes one or more keys from a dictionary without causing an error if the key does not exist.

    Args:
        itemDict (dict): The dictionary to remove items from.
        *args: One or more keys to remove from the dictionary.

    Returns:
        dict: The updated dictionary after the keys were removed.
    """
    # Check that the dictionary exists 
    if itemDict is not None:
        # Check if any keyword arguments passed
        if args and len(args) > 0:
            # Loop through each key to remove
            for arg in args:
                if arg is not None:
                    print(f"Removing key {arg} from dictionary of length {len(itemDict)} items.")
                    
                    # Remove the key with pop() with default None avoids exceptions
                    itemDict.pop(arg, None)
                    
                    print(f"New dictionary length: {len(itemDict)}")

    # Return the dictionary
    return itemDict

def main():
    fruitNames = ["apples", "peaches", "pineapples", "apples", "blueberries", "oranges", "kiwi"]
    fruitLocations = ["Massachusetts", "Georgia", "Hawaii", "Washington", "Maine", "Florida", "California"]
    
    # Create dictionary
    fruitDict = createDictionaryFromKeyValuePairs(fruitNames, fruitLocations)
    
    # Merge dictionaries
    moreFruits = {"mango": "Florida", "banana": "Ecuador"}
    mergedDict = mergeDictionaries(fruitDict, moreFruits)
    
    # Add items
    updatedDict = addItemsToDictionary(mergedDict, cherry="Michigan", apple="New York")
    
    # Remove items
    finalDict = removeItemsFromDictionary(updatedDict, "banana", "pineapples", "grape")
    
    # Return the final dictionary 
    return finalDict

if __name__ == "__main__":
    main()


