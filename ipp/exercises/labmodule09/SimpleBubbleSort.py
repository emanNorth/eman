class SimpleBubbleSort:
    '''
    Implements a classic bubble sort algorithm for sorting lists.
    '''

    def __init__(self):
        '''
        Initializes the SimpleBubbleSort instance.
        '''
        pass

    def sort(self, data):
        '''
        Sorts the provided list using the bubble sort algorithm.

        Parameters:
        data (list): A list of comparable items (numbers, strings, etc.)

        Returns:
        list: A new sorted list without modifying the original.
        '''
        
        # make a copy so original list is not changed
        sorted_data = data.copy()
        # get number of items in the list
        n = len(sorted_data)


        # repeat going through the list multiple times
        for i in range(n):
            for j in range(0, n - i - 1):
                # check if two neighbors are in the wrong order
                if sorted_data[j] > sorted_data[j + 1]:
                    # swap them if they are wrong
                    sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]

        return sorted_data