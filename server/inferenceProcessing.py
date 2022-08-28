import numpy as np
from models import runModel
from models.runModel import ComplexityDataset, ComplexityNN
import json
import requests
import symbl
import speedener

def processInferenceHeatmap(arr: list, speedupFactor: float)->list:
    """
    Smoothens and normalizes the speedup factor & curve
    """
    smoothenedHeatmap = np.array(arr)
    smoothenedHeatmap = smoothenedHeatmap * 10
    maxVal = max(smoothenedHeatmap)
    smoothenedHeatmap = (1.0 - smoothenedHeatmap)/(1.0 - maxVal)
    #calculate moving average
    window_size = 3\
    movingAvgs = []
    for i in range(window):

    
    i = 0
    while i < len(smoothenedHeatmap) - window_size + 1:
  
        # Calculate the average of current window
        window_average = round(np.sum(smoothenedHeatmap[
        i:i+window_size]) / window_size, 2)
        
        # Store the average of current
        # window in moving average list
        movingAvgs.append(window_average)
        
        # Shift window to right by one position
        i += 1
    return movingAvgs

def frontendConnection(videoPath: str, speedupFactor: float):
    """
    The main connection
    """
    
    inputCSV = 'inferenceTable.csv'
    inferredHeatmap = runModel.runInferenceModel('models\\model.pt', 'models\\inferenceTable.csv')
    print(inferredHeatmap)
    proceessedHeatmap = processInferenceHeatmap(inferredHeatmap, speedupFactor)
    print(proceessedHeatmap)
