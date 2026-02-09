import sys

# lists with some duplicates.
petsA = ["dog", "owl", "fox", "goat", "donkey", "skink","python","tarantula", "fox", "owl", "skink"]
petsB = ["cat", "python", "ferret", "owl", "mantis", "donkey", "whale", "gecko", "mantis", "ferret", "python"]

def createSetFromNames(names):
    '''
    Converts a list of names into a set. 
    
    Args:
        names (list): A list of names (strings).
    
    Returns:
        set: A set containing the unique names from the list.
    
    '''
    # Initialize as None in case the input is empty.
    pet_set = None
    
    if names is not None:
        # Convert the list to a set, automatically removing duplicates.
        pet_set = set(names)
    
    return pet_set


def mergeSetNames(*args):
    '''
    Merges two sets together into a single set.
     
    Args:
        args: unspcicifed number of positional arguments, each a set.
    
    Returns:
        set: A new set containing all unique elements from merged sets.
    '''

    # Create an empty set.
    merged_set = set()
    
    # Check that at least one set was passed.
    if args and len(args) > 0: 
        for arg in args:
            if arg is not None:
                print(f"Merging set into main set with {len(arg)} items.")
                # Merge the current set into the main set (union)
                merged_set = merged_set | arg
                print(f"Newly merged set: {merged_set}") 
        
        # Return the newly merged set.        
        return merged_set
    
    # Handle the case when no sets were passed.
    else:
        print("No sets included in arguments to function. Ignoring.")
    
    # Return empty set if nothing was merged.
    return merged_set


def addItemsToSet(pet_set, *args):
    '''
    Add one or more items to a given set.
    
    Args:
        pet_set (set): A set to which items will be added.
        *args: One or more items to add to the set. 
   
    Returns:
        set: A new set containing newly added items to a given set.
    '''
    
    # Check that the set exist.
    if pet_set is not None:
        # Check that at least one item could pass.
        if args and len(args) > 0:
            for arg in args:
                if arg is not None:
                    print(f"Adding item {arg} to set of length {len(pet_set)} items.")
                    # Add item to the set
                    pet_set.add(arg)
                    print(f"New set length: {len(pet_set)}")
    
    # Return the updated set.
    return pet_set


def removeItemsFromSet(pet_set, *args):
    '''
    Remove one or more items to a given set.
    
    Args:
        pet_set (set): A set to which items will be removed.
        *args: One or more items to remove from the set. 
   
    Returns:
        set: Updated set post items removal to a given set.
    '''
    
    # Check that the set exist.
    if pet_set is not None:
        # Check that at least one item could pass.
        if args and len(args) > 0:
            for arg in args:
                if arg is not None:
                    print(f"Removing item {arg} from set of length {len(pet_set)} items.")
                    # Remove item to the set
                    pet_set.discard(arg)
                    print(f"New set length: {len(pet_set)}")
                    
    # Return the updated set.
    return pet_set

def main():
    pet_set = createSetFromNames(petsA)
    pet_set2 = createSetFromNames(petsB)

    # shows unique items from petsA
    print(pet_set) 
    # shows unique items from petsB  
    print(pet_set2)
    
    pet_set = mergeSetNames(pet_set, pet_set2)
    
    # Test adding items: one existing ("owl") and one new ("dragon")
    addItemsToSet(pet_set, "owl", "dragon")
    
    # Test removing items: one existing ("fox") and one non-existent ("shark")
    removeItemsFromSet(pet_set, "fox", "shark")

        
if __name__ == "__main__":
    sys.exit(main())
