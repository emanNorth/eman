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
        sorted_data = data.copy()
        n = len(sorted_data)

        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_data[j] > sorted_data[j + 1]:
                    sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]

        return sorted_data