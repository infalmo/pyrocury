from scipy.signal import savgol_filter
import numpy as np
import runModel
import json
import requests
import symbl

def processInferenceHeatmap(arr: list, interval: float = 90, speedupFactor: float)->list:
    """
    Smoothens and normalizes the speedup factor & curve
    """
    smoothenedHeatmap = savgol_filter(arr, 7, 6)
    smoothenedHeatmap = np.array(smoothenedHeatmap)
    maxVal = max(smoothenedHeatmap)
    finalVals = (1-smoothenedHeatmap)/(1-maxVal)
    return finalVals * interval * 1/speedupFactor

def frontendConnection(videoPath: str, speedupFactor: float):
    """
    The main connection
    """
    
    inputCSV = 'inferenceTable.csv'
    inferredHeatmap = runModel.runInferenceModel('model.pt', 'inferenceTable.csv')
    print(inferredHeatmap)
    proceessedHeatmap = processInferenceHeatmap(inferredHeatmap, 90, speedupFactor)