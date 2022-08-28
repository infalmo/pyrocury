from scraper import youtubeVideo
from processTestData import chunkVideo
from symblaiTextProcessing import mergeChunkedTranscripts
from finalProcessing import videoProcessing, convertToCSV
from runModel import runInferenceModel, ComplexityNN, ComplexityDataset
import os
import json

def transcriptProcessor(link: str, workingDir: str = 'temp', modelPath: str = 'model.pt')->list:
    """
    Does all the downloading and returns a raw inference heatmap
    """
    video = youtubeVideo(link)
    baseDirectory = f'{workingDir}\\{video.id}'
    os.makedirs(os.path.dirname(baseDirectory), exist_ok=True)
    transcriptFile = baseDirectory + f'\\{video.id}-transcript.json'
    video.saveTranscript(transcriptFile)
    chunkedTranscriptFile = baseDirectory + f'\\{video.id}-chunkedTranscript.json'
    with open(chunkedTranscriptFile, 'w', encoding='utf-8') as chunkFile:
        json.dump(chunkVideo(video.transcript, [], False), chunkFile)
    wholeTranscriptFile = baseDirectory + f'\\{video.id}-wholeTranscript.txt'
    mergeChunkedTranscripts(chunkedTranscriptFile, wholeTranscriptFile)
    dataFile = baseDirectory + f'\\{video.id}-data.json'
    videoProcessing('', chunkedTranscriptFile, wholeTranscriptFile, transcriptFile, video.id,
                    dataFile, includeHeatmap=False)
    csvFile = baseDirectory + f'\\{video.id}-features.csv'
    convertToCSV(workingDir, csvFile, False)
    return runInferenceModel(modelPath, csvFile)
    

    
    

