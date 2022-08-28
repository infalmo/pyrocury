from scipy.signal import savgol_filter
import numpy as np
from models import runModel
from models.runModel import ComplexityDataset, ComplexityNN
import json
import requests
import symbl

def processInferenceHeatmap(arr: list, speedupFactor: float, interval: float = 90)->list:
    """
    Smoothens and normalizes the speedup factor & curve
    """
    smoothenedHeatmap = np.array(arr)
    smoothenedHeatmap *= 10
    smoothenedHeatmap = savgol_filter(smoothenedHeatmap, 7, 5)
    maxVal = max(smoothenedHeatmap)
    finalVals = (1.0 - smoothenedHeatmap)/(1.0 - maxVal) * float(interval) * 1.0/speedupFactor
    return list(finalVals)


def frontendConnection(videoPath: str, speedupFactor: float):
    """
    The main connection
    """
    
    inputCSV = 'inferenceTable.csv'
    inferredHeatmap = runModel.runInferenceModel('models\\model.pt', 'models\\inferenceTable.csv')
    print(inferredHeatmap)
    proceessedHeatmap = processInferenceHeatmap(inferredHeatmap, speedupFactor, 90)
    print(proceessedHeatmap)
    


frontendConnection('', 1)