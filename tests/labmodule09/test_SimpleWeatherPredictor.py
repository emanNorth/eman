import unittest
from ipp.exercises.labmodule09.SimpleWeatherPredictor import SimpleWeatherPredictor

class SimpleWeatherPredictorTest(unittest.TestCase):
    '''
    Unit tests for SimpleWeatherPredictor class.
    Tests basic functionality of weather prediction using KNN algorithm.
    '''
    
    def setUp(self):
        '''
        Set up test fixtures before each test method.
        Creates sample weather history data for testing.
        '''
        self.predictor = SimpleWeatherPredictor(k = 3)
        
        # Create sample weather history with at least 3 records
        self.weatherHistory = [
            {'temperature': 20.0, 'humidity': 65.0, 'pressure': 1013.0},
            {'temperature': 22.0, 'humidity': 60.0, 'pressure': 1015.0},
            {'temperature': 24.0, 'humidity': 55.0, 'pressure': 1017.0},
            {'temperature': 26.0, 'humidity': 50.0, 'pressure': 1019.0},
            {'temperature': 28.0, 'humidity': 45.0, 'pressure': 1021.0}
        ]
    
    def testPrepareTrainingData(self):
        '''
        Test that training data is prepared correctly from weather history.
        Should create feature-target pairs using sliding window approach.
        '''
        trainingData = self.predictor.prepareTrainingData(self.weatherHistory)
        
        # Should have data for all three metrics
        self.assertIn('temperature', trainingData)
        self.assertIn('humidity', trainingData)
        self.assertIn('pressure', trainingData)
        
        # With 5 records, we should have 3 training samples (records 3-5)
        self.assertEqual(len(trainingData['temperature']), 3)
        self.assertEqual(len(trainingData['humidity']), 3)
        self.assertEqual(len(trainingData['pressure']), 3)
    
    def testTrainModel(self):
        '''
        Test that the predictor can be trained successfully.
        After training, isTrained flag should be True.
        '''
        success = self.predictor.train(self.weatherHistory)
        
        self.assertTrue(success)
        self.assertTrue(self.predictor.isTrained)
        self.assertEqual(self.predictor.trainingCount, 1)
    
    def testPredictAfterTraining(self):
        '''
        Test that predictions can be made after training.
        Predictions should return numeric values for all metrics.
        '''
        self.predictor.train(self.weatherHistory)
        
        # Use last 2 records for prediction
        recentData = self.weatherHistory[-2:]
        predictions = self.predictor.predict(recentData)
        
        # Should have predictions for all metrics
        self.assertIsNotNone(predictions['temperature'])
        self.assertIsNotNone(predictions['humidity'])
        self.assertIsNotNone(predictions['pressure'])
        
        # Predictions should be numeric
        self.assertIsInstance(predictions['temperature'], (int, float))
        self.assertIsInstance(predictions['humidity'], (int, float))
        self.assertIsInstance(predictions['pressure'], (int, float))
    
    def testPredictWithoutTraining(self):
        '''
        Test that prediction fails gracefully when model is not trained.
        Should return None values for all predictions.
        '''
        recentData = self.weatherHistory[-2:]
        predictions = self.predictor.predict(recentData)
        
        # Should return None for all predictions when not trained
        self.assertIsNone(predictions['temperature'])
        self.assertIsNone(predictions['humidity'])
        self.assertIsNone(predictions['pressure'])
    
    def testEvaluatePredictions(self):
        '''
        Test that prediction evaluation produces error metrics.
        Should return evaluation dictionary with error measurements.
        '''
        self.predictor.train(self.weatherHistory)
        
        # Make predictions
        recentData = self.weatherHistory[-2:]
        predictions = self.predictor.predict(recentData)
        
        # Actual values (last record in history)
        actual = self.weatherHistory[-1]
        
        # Evaluate predictions
        evaluation = self.predictor.evaluatePredictions(predictions, actual)
        
        # Should have evaluation for all metrics
        self.assertIn('temperature', evaluation)
        self.assertIn('humidity', evaluation)
        self.assertIn('pressure', evaluation)
        
        # Each evaluation should have error metrics
        for metric_eval in evaluation.values():
            self.assertIn('absolute_error', metric_eval)
            self.assertIn('percent_error', metric_eval)


if __name__ == '__main__':
    unittest.main()