from scipy.signal import savgol_filter
import numpy as np
import runModel
from runModel import ComplexityDataset, ComplexityNN
import json
import requests
import symbl

def processInferenceHeatmap(arr: list, speedupFactor: float, interval: float = 90)->list:
    """
    Smoothens and normalizes the speedup factor & curve
    """
    smoothenedHeatmap = savgol_filter(arr, 5, 4)
    smoothenedHeatmap = np.array(smoothenedHeatmap)
    maxVal = max(smoothenedHeatmap)
    finalVals = (1-smoothenedHeatmap)/(1-maxVal) * interval * 1/speedupFactor
    return finalVals 

def s

def frontendConnection(videoPath: str, speedupFactor: float):
    """
    The main connection
    """
    
    inputCSV = 'inferenceTable.csv'
    inferredHeatmap = runModel.runInferenceModel('model.pt', 'inferenceTable.csv')
    print(inferredHeatmap)
    proceessedHeatmap = processInferenceHeatmap(inferredHeatmap, speedupFactor, 90)
    print(proceessedHeatmap)


frontendConnection('', 1)