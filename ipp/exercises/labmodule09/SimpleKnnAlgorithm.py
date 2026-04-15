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
        # if points are not the same size, can't compare them
        if len(point1) != len(point2):
            # return infinity (very large distance)
            return float('inf')
        
        sumSquares = 0.0
        for i in range(len(point1)):
            diff = point1[i] - point2[i]
            sumSquares += diff * diff
        
        # return square root of total (final distance)
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
        # check if points have the same number of dimensions
        if len(point1) != len(point2):
            # return infinity if they don't match
            return float('inf')
        
        sumAbs = 0.0
        for i in range(len(point1)):
            sumAbs += abs(point1[i] - point2[i])
        
        # return the total absolute difference
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
        # Go through each training data point
        for features, target in self.trainingData:
            # Choose which distance to use
            if useEuclidean:
                dist = self.calculateEuclideanDistance(testPoint, features)
            else:
                dist = self.calculateManhattanDistance(testPoint, features)

            # Append a single tuple (Store the distance and the target value as a tuple).
            distances.append((dist, target))
        
        # Sort by distance and return k nearest (Sort based on the first value in each tuple (the distance))
        distances.sort(key = lambda x: x[0])
        # Return the k closest points
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
        # Find the k nearest neighbors of the test point
        neighbors = self.findKNearest(testPoint, useEuclidean)
        
        # If no neighbors are found, return None
        if not neighbors:
            return None
        
        # Calculate average of neighbor values
        total = sum(target for _, target in neighbors)
        # Calculate the average value (this is the regression prediction)
        prediction = total / len(neighbors)
        
        # Return the predicted value
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
        # Find the k nearest neighbors of the test point
        neighbors = self.findKNearest(testPoint, useEuclidean)
        
        # If no neighbors are found, return None
        if not neighbors:
            return None
        
        # Count votes for each class
        votes = {}
        for _, target in neighbors:
            # convert target to integer class
            targetClass = int(target)
            # increment vote count
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
        # Calculate the difference between actual and predicted
        error = actual - predicted
        # absolute value of the error
        absError = abs(error)
        
        # Calculate percentage error (avoid division by zero)
        if actual != 0:
            percentError = (absError / abs(actual)) * 100
        else:
            # if actual is 0, percent error is 0 if prediction is also 0,
            # otherwise it is considered infinite
            percentError = 0 if predicted == 0 else float('inf')
        
        # Return a dictionary with different error measures
        return {
            'error': error, # signed error
            'absolute_error': absError,     # how far off prediction is
            'squared_error': error * error, # emphasizes larger errors
            'percent_error': percentError   # error as a percentage
        }