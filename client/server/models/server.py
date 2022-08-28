from .transcriptProcessing import transcriptProcessor
import os
import pytube
import numpy as np
from .runModel import ComplexityNN
from moviepy.editor import *
import shutil

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


def speeden_video(video_file_path: str, speeds: list[float], outFile: str = "pyrocury-output.mp4") -> str:
    video = VideoFileClip(video_file_path)
    output = None

    l = 0.0
    for x in range(len(speeds)):
        r = None
        if x != len(speeds)-1:
            r = l+90.0

        sub_video: VideoClip = video.subclip(l, r)
        sub_video = sub_video.set_fps(video.fps*speeds[x])
        sub_video = sub_video.fx(vfx.speedx, speeds[x])

        if output == None:
            output = sub_video
        else:
            output = concatenate_videoclips([output, sub_video])

    output.write_videofile(outFile)
    return outFile



def process(url:str):
    """
    takes a single YT URL and processes it to send to the frontend.
    """
    #clear cache
    if 'temp' in os.listdir():
        shutil.rmtree('temp')
    rawHeatmap = transcriptProcessor(url)
    videoPath = download_youtube_video(url, 'temp\\' + os.listdir('temp')[0])
    print(processedHeatmap)
    processedHeatmap = convert_raw_heatmap(rawHeatmap)
    print(videoPath)
    return speeden_video(videoPath, processedHeatmap)
    

