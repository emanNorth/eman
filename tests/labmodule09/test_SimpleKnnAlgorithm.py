import unittest

from ipp.exercises.labmodule09.SimpleKnnAlgorithm import SimpleKnnAlgorithm

class SimpleKnnAlgorithmTest(unittest.TestCase):
    '''
    A basic test suite for validating the functionality of the
    SimpleKnnAlgorithm class, including distance calculations,
    training data handling, prediction methods, and evaluation metrics.
    '''
    
    
    def setUp(self):
        '''Set up test fixtures before each test method.'''
        self.knn = SimpleKnnAlgorithm(k = 3)
        
        # Sample training data: (features, target)
        self.regression_data = [
            ([1.0, 2.0], 10.0),
            ([2.0, 3.0], 15.0),
            ([3.0, 4.0], 20.0),
            ([4.0, 5.0], 25.0),
            ([5.0, 6.0], 30.0)
        ]
        
        # Classification data (using integer classes)
        self.classification_data = [
            ([1.0, 1.0], 0),
            ([1.5, 1.5], 0),
            ([2.0, 2.0], 0),
            ([8.0, 8.0], 1),
            ([8.5, 8.5], 1),
            ([9.0, 9.0], 1)
        ]
    
    def testDistanceCalculations(self):
        '''Test both Euclidean and Manhattan distance calculations.'''
        point1 = [0.0, 0.0]
        point2 = [3.0, 4.0]
        
        # Test Euclidean distance: sqrt(3^2 + 4^2) = 5.0
        euclidean = self.knn.calculateEuclideanDistance(point1, point2)
        self.assertAlmostEqual(euclidean, 5.0, places = 5)
        
        # Test Manhattan distance: |3| + |4| = 7.0
        manhattan = self.knn.calculateManhattanDistance(point1, point2)
        self.assertAlmostEqual(manhattan, 7.0, places = 5)
        
        # Test with identical points
        same_point = [1.0, 2.0]
        self.assertAlmostEqual(
            self.knn.calculateEuclideanDistance(same_point, same_point), 
            0.0, 
            places = 5
        )
        
        # Test with mismatched dimensions
        point3 = [1.0, 2.0, 3.0]
        distance = self.knn.calculateEuclideanDistance(point1, point3)
        self.assertEqual(distance, float('inf'))
    
    def testTrainingDataManagement(self):
        '''Test setting and validating training data.'''
        # Test setting valid training data
        self.knn.setTrainingData(self.regression_data)
        self.assertEqual(len(self.knn.trainingData), 5)
        self.assertEqual(self.knn.trainingData, self.regression_data)
        
        # Test with empty data
        empty_knn = SimpleKnnAlgorithm(k = 3)
        empty_knn.setTrainingData([])
        self.assertEqual(len(empty_knn.trainingData), 0)
        
        # Test with None
        none_knn = SimpleKnnAlgorithm(k = 3)
        none_knn.setTrainingData(None)
        self.assertEqual(len(none_knn.trainingData), 0)
    
    def testFindKNearest(self):
        '''Test finding k nearest neighbors with both distance metrics.'''
        self.knn.setTrainingData(self.regression_data)
        test_point = [2.5, 3.5]
        
        # Test with Euclidean distance
        neighbors_euclidean = self.knn.findKNearest(test_point, useEuclidean = True)
        self.assertEqual(len(neighbors_euclidean), 3)
        
        # Verify neighbors are sorted by distance
        for i in range(len(neighbors_euclidean) - 1):
            self.assertLessEqual(neighbors_euclidean[i][0], neighbors_euclidean[i + 1][0])
        
        # Test with Manhattan distance
        neighbors_manhattan = self.knn.findKNearest(test_point, useEuclidean = False)
        self.assertEqual(len(neighbors_manhattan), 3)
        
        # Test with no training data
        empty_knn = SimpleKnnAlgorithm(k = 3)
        neighbors_empty = empty_knn.findKNearest(test_point)
        self.assertEqual(neighbors_empty, [])
    
    def testRegressionPrediction(self):
        '''Test regression prediction functionality.'''
        self.knn.setTrainingData(self.regression_data)
        
        # Test prediction on a point between training points
        test_point = [2.5, 3.5]
        prediction = self.knn.predictRegression(test_point)
        self.assertIsInstance(prediction, float)
        self.assertGreater(prediction, 10.0)
        self.assertLess(prediction, 25.0)
        
        # Test on exact training point
        exact_point = [3.0, 4.0]
        exact_prediction = self.knn.predictRegression(exact_point)
        self.assertAlmostEqual(exact_prediction, 20.0, delta = 2.0)
        
        # Test with no training data
        empty_knn = SimpleKnnAlgorithm(k = 3)
        empty_prediction = empty_knn.predictRegression(test_point)
        self.assertIsNone(empty_prediction)
        
        # Test with Manhattan distance
        manhattan_prediction = self.knn.predictRegression(test_point, useEuclidean = False)
        self.assertIsNotNone(manhattan_prediction)
    
    def testClassificationPrediction(self):
        '''Test classification prediction functionality.'''
        self.knn.setTrainingData(self.classification_data)
        
        # Test point close to class 0
        test_point_class0 = [1.2, 1.2]
        prediction0 = self.knn.predictClassification(test_point_class0)
        self.assertEqual(prediction0, 0)
        
        # Test point close to class 1
        test_point_class1 = [8.2, 8.2]
        prediction1 = self.knn.predictClassification(test_point_class1)
        self.assertEqual(prediction1, 1)
        
        # Test with no training data
        empty_knn = SimpleKnnAlgorithm(k = 3)
        empty_prediction = empty_knn.predictClassification([1.0, 1.0])
        self.assertIsNone(empty_prediction)
        
        # Test with Manhattan distance
        manhattan_prediction = self.knn.predictClassification(
            test_point_class0, 
            useEuclidean = False
        )
        self.assertIn(manhattan_prediction, [0, 1])
    
    def testPredictionEvaluation(self):
        '''Test prediction evaluation metrics.'''
        # Test perfect prediction
        metrics_perfect = self.knn.evaluatePrediction(10.0, 10.0)
        self.assertEqual(metrics_perfect['error'], 0.0)
        self.assertEqual(metrics_perfect['absolute_error'], 0.0)
        self.assertEqual(metrics_perfect['squared_error'], 0.0)
        self.assertEqual(metrics_perfect['percent_error'], 0.0)
        
        # Test under-prediction
        metrics_under = self.knn.evaluatePrediction(10.0, 8.0)
        self.assertEqual(metrics_under['error'], 2.0)
        self.assertEqual(metrics_under['absolute_error'], 2.0)
        self.assertEqual(metrics_under['squared_error'], 4.0)
        self.assertAlmostEqual(metrics_under['percent_error'], 20.0, places = 1)
        
        # Test over-prediction
        metrics_over = self.knn.evaluatePrediction(10.0, 12.0)
        self.assertEqual(metrics_over['error'], -2.0)
        self.assertEqual(metrics_over['absolute_error'], 2.0)
        
        # Test with zero actual value and non-zero prediction
        metrics_zero = self.knn.evaluatePrediction(0.0, 5.0)
        self.assertEqual(metrics_zero['percent_error'], float('inf'))
        
        # Test with both zero
        metrics_both_zero = self.knn.evaluatePrediction(0.0, 0.0)
        self.assertEqual(metrics_both_zero['percent_error'], 0.0)


if __name__ == '__main__':
    unittest.main()