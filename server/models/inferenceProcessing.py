from scipy.signal import savgol_filter

def processInferenceHeatmap(arr: list)->list:
    smoothenedHeatmap = savgol_filter(arr)

