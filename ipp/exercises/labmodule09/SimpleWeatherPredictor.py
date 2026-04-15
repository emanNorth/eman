from typing import List, Dict, Optional

from ipp.exercises.labmodule09.SimpleKnnAlgorithm import SimpleKnnAlgorithm

class SimpleWeatherPredictor:
    '''
    A simple weather prediction system that uses KNN models
    to predict temperature, humidity, and pressure based on
    recent historical data.
    '''
    
    def __init__(self, k: int = 3):
        '''
        Initializes the weather predictor with separate KNN models
        for each weather metric.

        Args:
            k (int): Number of neighbors to use for predictions.
        '''
        self.k = k
        
        # Create separate KNN models for each weather metric
        self.tempPredictor = SimpleKnnAlgorithm(k)
        self.humidityPredictor = SimpleKnnAlgorithm(k)
        self.pressurePredictor = SimpleKnnAlgorithm(k)
        
        # Flag to check if models are trained
        self.isTrained = False
        # Counter for number of training iterations
        self.trainingCount = 0
        
        
    def prepareTrainingData(self, weatherHistory: List[Dict]) -> Dict[str, List]:
        '''
        Prepares training data from weather history using a sliding window.

        Args:
            weatherHistory (List[Dict]): List of weather records.

        Returns:
            Dict[str, List]: Training data for temperature, humidity,
            and pressure in (features, target) format.
        '''
        if len(weatherHistory) < 3:
            print("Need at least 3 records for training")
            return {}
        
        # Lists to store training samples for each metric
        tempData = []
        humidityData = []
        pressureData = []
        
        # Create training samples using sliding window
        # Use previous 2 readings to predict next value
        for i in range(2, len(weatherHistory)):
            prev2 = weatherHistory[i - 2]
            prev1 = weatherHistory[i - 1]
            current = weatherHistory[i]
            
            # Temperature training data
            if all(r.get('temperature') is not None for r in [prev2, prev1, current]):
                features = [
                    prev2['temperature'],
                    prev1['temperature']
                ]
                target = current['temperature']
                tempData.append((features, target))
            
            # Humidity training data
            if all(r.get('humidity') is not None for r in [prev2, prev1, current]):
                features = [
                    prev2['humidity'],
                    prev1['humidity']
                ]
                target = current['humidity']
                humidityData.append((features, target))
            
            # Pressure training data
            if all(r.get('pressure') is not None for r in [prev2, prev1, current]):
                features = [
                    prev2['pressure'],
                    prev1['pressure']
                ]
                target = current['pressure']
                pressureData.append((features, target))
        
        # Return training data for all three metrics
        return {
            'temperature': tempData,
            'humidity': humidityData,
            'pressure': pressureData
        }
        
        
        
    def train(self, weatherHistory: List[Dict]) -> bool:
        '''
        Trains the KNN models using prepared weather data.

        Args:
            weatherHistory (List[Dict]): Historical weather data.

        Returns:
            bool: True if at least one model was trained successfully,
            otherwise False.
        '''
        # Prepare training data
        trainingData = self.prepareTrainingData(weatherHistory)
        
        if not trainingData:
            return False
        
        # counter for how many models were trained
        trainedModels = 0
        
        # Train temperature predictor if data available
        if 'temperature' in trainingData and trainingData['temperature']:
            self.tempPredictor.setTrainingData(trainingData['temperature'])
            trainedModels += 1
            print(f"Temperature predictor trained with {len(trainingData['temperature'])} samples")
        
         # Train humidity predictor if data available
        if 'humidity' in trainingData and trainingData['humidity']:
            self.humidityPredictor.setTrainingData(trainingData['humidity'])
            trainedModels += 1
            print(f"Humidity predictor trained with {len(trainingData['humidity'])} samples")
            
        # Train pressure predictor if data available
        if 'pressure' in trainingData and trainingData['pressure']:
            self.pressurePredictor.setTrainingData(trainingData['pressure'])
            trainedModels += 1
            print(f"Pressure predictor trained with {len(trainingData['pressure'])} samples")
        
        # Mark as trained if at least one model is trained
        if trainedModels > 0:
            self.isTrained = True
            self.trainingCount += 1
            print(f"Weather predictor training complete (iteration {self.trainingCount})")
            return True
        
        return False
    
    
    def predict(self, recentData: List[Dict]) -> Dict[str, Optional[float]]:
        '''
        Generates predictions for temperature, humidity, and pressure.

        Args:
            recentData (List[Dict]): Most recent weather records.

        Returns:
            Dict[str, Optional[float]]: Predicted values for each metric.
        '''
        # Default predictions
        predictions = {
            'temperature': None,
            'humidity': None,
            'pressure': None
        }
        
        if not self.isTrained:
            print("Predictors not trained yet")
            return predictions
        
        if len(recentData) < 2:
            print("Need at least 2 recent records for prediction")
            return predictions
        
        # Get last 2 records
        prevRecord2 = recentData[-2]
        prevRecord1 = recentData[-1]
        
        # Predict temperature if data available
        if prevRecord2.get('temperature') is not None and prevRecord1.get('temperature') is not None:
            features = [prevRecord2['temperature'], prevRecord1['temperature']]
            predictions['temperature'] = self.tempPredictor.predictRegression(features)
        
        # Predict humidity if data available
        if prevRecord2.get('humidity') is not None and prevRecord1.get('humidity') is not None:
            features = [prevRecord2['humidity'], prevRecord1['humidity']]
            predictions['humidity'] = self.humidityPredictor.predictRegression(features)
        
        # Predict pressure if data available
        if prevRecord2.get('pressure') is not None and prevRecord1.get('pressure') is not None:
            features = [prevRecord2['pressure'], prevRecord1['pressure']]
            predictions['pressure'] = self.pressurePredictor.predictRegression(features)
        
        return predictions
    
    
    def evaluatePredictions(self, predictions: Dict, actual: Dict) -> Dict[str, Dict]:
        '''
        Evaluates prediction accuracy for each weather metric.

        Args:
            predictions (Dict): Predicted values.
            actual (Dict): Actual observed values.

        Returns:
            Dict[str, Dict]: Evaluation results with error metrics.
        '''
        evaluation = {}
        
        # Evaluate temperature
        if predictions.get('temperature') and actual.get('temperature'):
            evaluation['temperature'] = self.tempPredictor.evaluatePrediction(
                actual['temperature'],
                predictions['temperature']
            )
        
        # Evaluate humidity
        if predictions.get('humidity') and actual.get('humidity'):
            evaluation['humidity'] = self.humidityPredictor.evaluatePrediction(
                actual['humidity'],
                predictions['humidity']
            )
        
        # Evaluate pressure
        if predictions.get('pressure') and actual.get('pressure'):
            evaluation['pressure'] = self.pressurePredictor.evaluatePrediction(
                actual['pressure'],
                predictions['pressure']
            )
        
        return evaluation