from transcriptProcessing import transcriptProcessor
import os
from tempfile import tempdir
from uuid import uuid4
import pytube
import numpy as np
from runModel import ComplexityNN

def download_youtube_video(url: str, workingDir: str):
    os.makedirs(workingDir, exist_ok=True)

    yt = pytube.YouTube(url)
    yt.streams.get_highest_resolution().download(workingDir)

    return os.path.join(workingDir, os.listdir(workingDir)[0])

def convert_raw_heatmap(raw: list[float]):
    # Invert
    H = 10*np.array(raw)
    maxH = max(H)
    K = (1.0-H)/(1.0-maxH)

    # Smoothen (moving average)
    MAVG_WINDOW = 3
    F = []
    
    sum = 0.0
    for i in range(len(K)):
        sum += K[i]
        if i >= MAVG_WINDOW:
            sum -= K[i-MAVG_WINDOW]
        F.append(sum/min(i+1, MAVG_WINDOW))

    return np.array(F)


def process(url:str):
    """
    takes a single YT URL and processes it to send to the frontend.
    """
    rawHeatmap = transcriptProcessor(url)
    download_youtube_video(url, 'temp\\' + os.listdir('temp')[0])
    processedHeatmap = convert_raw_heatmap(rawHeatmap)
    print(processedHeatmap)
    #delete folder when done
    os.removedirs('temp')


process('https://www.youtube.com/watch?v=VYQVlVoWoPY&ab_channel=3Blue1Brown')