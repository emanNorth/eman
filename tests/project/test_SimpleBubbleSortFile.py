import sys
import unittest

from ipp.exercises.project.SimpleBubbleSortFile import SimpleBubbleSort


class SimpleBubbleSortTest(unittest.TestCase):
    '''Unit tests for SimpleBubbleSort implementation.'''

    def setUp(self):
        '''Set up test fixture - runs before each test method.'''
        self.sorter = SimpleBubbleSort()

    def testEmptyList(self):
        '''Test sorting an empty list.'''
        data = []
        expected = []
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testSingleElement(self):
        '''Test sorting a list with single element.'''
        data = [42]
        expected = [42]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testAlreadySorted(self):
        '''Test sorting an already sorted list.'''
        data = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testReverseSorted(self):
        '''Test sorting a reverse sorted list.'''
        data = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testRandomNumbers(self):
        '''Test sorting random integers.'''
        data = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testNegativeNumbers(self):
        '''Test sorting with negative numbers.'''
        data = [3, -1, 4, -5, 2, -3]
        expected = [-5, -3, -1, 2, 3, 4]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testDuplicateValues(self):
        '''Test sorting with duplicate values.'''
        data = [3, 1, 4, 1, 5]
        expected = [1, 1, 3, 4, 5]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testStringSorting(self):
        '''Test sorting strings alphabetically.'''
        data = ["Thor", "Alice", "Diana", "Bob", "Charlie"]
        expected = ["Alice", "Bob", "Charlie", "Diana", "Thor"]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testFloatingPointNumbers(self):
        '''Test sorting floating point numbers.'''
        data = [3.14, 2.71, 1.41, 2.23, 1.73]
        expected = [1.41, 1.73, 2.23, 2.71, 3.14]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)

    def testReverseSorting(self):
        '''Test sorting in descending order using reverse=True.'''
        data = [1, 2, 3, 4, 5]
        expected = [5, 4, 3, 2, 1]
        result = self.sorter.sort(data, reverse=True)
        self.assertEqual(result, expected)

    def testSortByKeyFlowRate(self):
        '''Test sorting using key function (flow rate style data).'''
        data = [{"flow": 10}, {"flow": 5}, {"flow": 20}]

        expected = [{"flow": 5}, {"flow": 10}, {"flow": 20}]

        result = self.sorter.sortByKey(
            data,
            key_func=lambda x: x["flow"]
        )

        self.assertEqual(result, expected)


def main():
    '''Main function to run tests.'''
    test_suite = unittest.TestLoader().loadTestsFromTestCase(SimpleBubbleSortTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())