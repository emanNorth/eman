import math

from typing import List, Tuple, Optional, Dict

class SimpleKnnAlgorithm:
    '''
    A simple implementation of the K-Nearest Neighbors (KNN) algorithm
    for both regression and classification tasks.
    
    Attributes:
        k (int): Number of nearest neighbors to consider.
        trainingData (List[Tuple[List[float], float]]): Training dataset 
            where each entry contains feature values and a target label.
        featureNames (List[str]): Optional list of feature names.
    '''
    
    def __init__(self, k: int = 3):
        '''
        Initializes the KNN algorithm with a specified number of neighbors.

        Args:
            k (int): Number of nearest neighbors to use for predictions.
                    Default is 3.
        '''
        self.k = k
        self.trainingData = []
        self.featureNames = []
        
    def setTrainingData(self, data: List[Tuple[List[float], float]]):
        '''
        Sets the training data for the KNN model.

        Args:
            data (List[Tuple[List[float], float]]): A list where each element
                is a tuple containing:
                - A list of feature values (List[float])
                - A target value (float)
        '''
        if not data:
            print("Warning: No training data provided")
            return
        
        self.trainingData = data
        print(f"KNN trained with {len(data)} samples")
        
        
    def calculateEuclideanDistance(self, point1: List[float], point2: List[float]) -> float:
        '''
        Calculates the Euclidean distance between two data points.

        Args:
            point1 (List[float]): First data point.
            point2 (List[float]): Second data point.

        Returns:
            float: Euclidean distance between the two points.
                Returns infinity if the points have different dimensions.
        '''
        if len(point1) != len(point2):
            return float('inf')
        
        sumSquares = 0.0
        for i in range(len(point1)):
            diff = point1[i] - point2[i]
            sumSquares += diff * diff
        
        return math.sqrt(sumSquares)
    
    
    def calculateManhattanDistance(self, point1: List[float], point2: List[float]) -> float:
        '''
        Calculates the Manhattan (L1) distance between two data points.

        Args:
            point1 (List[float]): First data point.
            point2 (List[float]): Second data point.

        Returns:
            float: Manhattan distance between the two points.
                Returns infinity if the points have different dimensions.
        '''
        if len(point1) != len(point2):
            return float('inf')
        
        sumAbs = 0.0
        for i in range(len(point1)):
            sumAbs += abs(point1[i] - point2[i])
        
        return sumAbs
    
    
    def findKNearest(self, testPoint: List[float], useEuclidean: bool = True) -> List[Tuple[float, float]]:
        '''
        Finds the k nearest neighbors to a given test point.

        Args:
            testPoint (List[float]): The input data point to evaluate.
            useEuclidean (bool): If True, uses Euclidean distance;
                                otherwise uses Manhattan distance.

        Returns:
            List[Tuple[float, float]]: A list of tuples where each tuple contains:
                - Distance to the neighbor (float)
                - Target value of the neighbor (float)
        '''
        if not self.trainingData:
            return []
        
        # Calculate distances to all training points
        distances = []
        for features, target in self.trainingData:
            if useEuclidean:
                dist = self.calculateEuclideanDistance(testPoint, features)
            else:
                dist = self.calculateManhattanDistance(testPoint, features)

            # Append a single tuple
            distances.append((dist, target))
        
        # Sort by distance and return k nearest (Sort based on the first value in each tuple (the distance))
        distances.sort(key = lambda x: x[0])
        return distances[:self.k]
    
    
    def predictRegression(self, testPoint: List[float], useEuclidean: bool = True) -> Optional[float]:
        '''
        Predicts a continuous value using KNN regression.

        Args:
            testPoint (List[float]): The input data point to predict.
            useEuclidean (bool): If True, uses Euclidean distance;
                                otherwise uses Manhattan distance.

        Returns:
            Optional[float]: The predicted value (average of neighbors),
                            or None if no neighbors are found.
        '''
        
        neighbors = self.findKNearest(testPoint, useEuclidean)
        
        if not neighbors:
            return None
        
        # Calculate average of neighbor values
        total = sum(target for _, target in neighbors)
        prediction = total / len(neighbors)
        
        return prediction
    
    def predictClassification(self, testPoint: List[float], useEuclidean: bool = True) -> Optional[int]:
        '''
        Predicts a class label using KNN classification.

        Args:
            testPoint (List[float]): The input data point to classify.
            useEuclidean (bool): If True, uses Euclidean distance;
                                otherwise uses Manhattan distance.

        Returns:
            Optional[int]: The predicted class label (majority vote),
                        or None if no neighbors are found.
        '''
        neighbors = self.findKNearest(testPoint, useEuclidean)
        
        if not neighbors:
            return None
        
        # Count votes for each class
        votes = {}
        for _, target in neighbors:
            targetClass = int(target)
            votes[targetClass] = votes.get(targetClass, 0) + 1
        
        # Return class with most votes
        prediction = max(votes, key = votes.get)
        return prediction
    
    
    def evaluatePrediction(self, actual: float, predicted: float) -> Dict[str, float]:
        '''
        Evaluates the accuracy of a prediction.

        Args:
            actual (float): The true value.
            predicted (float): The predicted value.

        Returns:
            Dict[str, float]: A dictionary containing:
                - 'error': Difference between actual and predicted
                - 'absolute_error': Absolute value of the error
                - 'squared_error': Squared error
                - 'percent_error': Percentage error (handles division by zero)
        '''
        error = actual - predicted
        absError = abs(error)
        
        # Calculate percentage error (avoid division by zero)
        if actual != 0:
            percentError = (absError / abs(actual)) * 100
        else:
            percentError = 0 if predicted == 0 else float('inf')
        
        return {
            'error': error,
            'absolute_error': absError,
            'squared_error': error * error,
            'percent_error': percentError
        }