from asyncore import read
import languageHeuristics as lh
import yakeProcessing
import csv
from readability import Readability
import nltk
import json
import copy
import os

def heatmapMedian(heatmap: str)->float:
    """
    Given a heatmap csv file, return the median of the heatmap values
    """
    with open(heatmap, newline='') as heatmapFile:
        heatmapReader = csv.reader(heatmapFile, delimiter = ',', quotechar='|')
        next(heatmapReader)
        heatVals =  [float(i[1]) for i in heatmapReader]
    return round(sum(heatVals)/100, 2)

def processOverallTranscript(overallTranscript: str, runTime: float)->dict:
    """
    Applies a variety of NLP heuristics to an entire transcript
    overallTranscript: a file path to the overall transcript as a txt file
    runTime: the runtime of
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    with open(overallTranscript, 'r') as transcript:
        transcriptText = transcript.read()
    topics = yakeProcessing.add_topics(transcriptText)
    topicList = [i[0] for i in topics]
    outDict = {
        "dale-challReadabilityScore": Readability(transcriptText).dale_chall().score,
        "lexicalDiversity": lh.lexicalDiversity(transcriptText),
        "posComposition": lh.posFractions(transcriptText),
        "syllableRate": lh.syllablesPerSecond(transcriptText, runTime),
        "topicScores": topics,
        "topicsList": topicList
    }
    return outDict

def processChunk(overallTextData: dict, chunkText: str)->dict:
    """
    given a text and heuristics of its parent, return a dict of heuristics for the chunk
    """
    outDict = dict()
    score = lh.relativeDCReadability(chunkText, overallTextData["dale-challReadabilityScore"])
    outDict["relativeDCReadability"] = score
    outDict["lexicalDiversity"] = lh.lexicalDiversity(chunkText)
    outDict["posComposition"] = lh.posFractions(chunkText)
    chunkTime = 120 #chunks are 2 minutes long
    outDict["syllableRate"] = lh.syllablesPerSecond(chunkText, chunkTime)
    outDict["topicScores"] = yakeProcessing.add_topics(chunkText)
    numTopics = len(outDict["topicScores"]) #from add_topics in yakeProcessing.py
    chunkTopicList = [i[0] for i in outDict["topicScores"]]
    sharedTopics = set(chunkTopicList).intersection(overallTextData["topicsList"])
    if numTopics == 0:
        outDict["topTopicSimilarity"] = 0
    else:
        outDict["topTopicSimilarity"] = len(sharedTopics)/numTopics
    outDict["sharedTopicScores"] = [topic for topic in outDict["topicScores"] if topic[0] in sharedTopics]
    return outDict

def videoProcessing(heatmap: str, chunkedTranscript: str, totalText: str, baseTranscript:str, id:str, outFile: str, includeHeatmap: bool = True):
    """
    Merge all utility functions into a JSON file with features.
    heatmap, timeTranscript, totalText, baseTranscript: file names for heatmap, 
        chunked transcript, the total text file of the entire lecture, and a timed-based transcript
    id: string to identify the video by
    outFile: name of the output file
    """
    dataFile = dict()
    dataFile["metadata"] = dict()
    dataFile["metadata"]["id"] = id
    if includeHeatmap:
        dataFile["metadata"]["avgHeat"] = heatmapMedian(heatmap)
    with open(baseTranscript, 'r') as f:
        loadedBaseTranscript = json.loads(f.read())
    #get runtime through last transcript
    runTime = loadedBaseTranscript[-1]["start"] + loadedBaseTranscript[-1]["duration"]
    dataFile["metadata"]["runtime"] = runTime
    transcriptMetrics = processOverallTranscript(totalText, runTime)
    for key in transcriptMetrics.keys():
        dataFile["metadata"][key] = transcriptMetrics[key]
    dataFile["chunks"] = dict()
    #process transcript chunks
    with open(chunkedTranscript, 'r') as f:
        loadedChunkedTranscript = json.loads(f.read())
    #iterate through chunk
    for chunk in loadedChunkedTranscript:
        tempDict = dict()
        #id is video id plus timestamp when the chunk starts
        tempDict["id"] = f"{id}-" + str(int(chunk["start"]))
        if includeHeatmap:
            tempDict["heat"] = chunk["heat"]
        tempDict["start"] = chunk["start"]
        tempDict["text"] = chunk["text"]
        tempDict["metrics"] = processChunk(dataFile["metadata"], chunk["text"])
        dataFile["chunks"][tempDict["id"]] = copy.deepcopy(tempDict)
    with open(outFile, 'w') as json_file:
        json_file.write(json.dumps(dataFile, indent = 4))


def convertToCSV(convertDir: str, outFile: str, includeHeatMap: bool = True):
    """
    Converts all the written data JSON files into a CSV containing various parameters and labels. Each row is a chunk
    convertDir: directory to find json files in
    outFile: the CSV file to write to
    Columns:
    id: the id of the chunk (str)
    relativeDCReadability: relative readability by the dale-chall test (float)
    lexicalDiversity: the lexical diversity of the chunk (float)
    topTopicSimilarity: the fraction of top topics shared between the overall transcript and the chunk (float)
    syllableRate: the rate of syllables spoken
    posComposition: parts of speech composition (several columns) (float)
    topTopicSimilarityRelativeScores: the relative scores of the top 30 topics (30 columns) (float)
        relative score is calculated by (chunkTopicScore - overallTextTopicScore). 
        A lower score means the topic is more important. A negative score meants that the topic is more important
        in the chunk than in the overall text
    heat: the heat of the chunk (float)
    """
    header = ["id", "relativeReadability", "lexicalDiversity", "topTopicSimilarity", "syllableRate"]
    #posComposition tags
    posTags = ['PRP$', 'VBG', 'VBD', 'VBN', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'NN', 'TO', 'PRP', 'RB',
                   'NNS', 'NNP', 'VB', 'WRB', 'CC', 'CD', 'EX', 'IN', 'WP$', 'MD', 'JJS', 'JJR', "``", "''", ':']
    header.extend(posTags)

    
    for i in range(30):
        header.append(f'topic-{i}')
    header.append("heat")

    #add features
    outCSV = open(outFile, 'w', newline='')
    writer = csv.writer(outCSV)
    writer.writerow(header)
    for id in os.listdir(convertDir):
        print("Processing " + id)
        with open(f'{convertDir}\\{id}\\{id}-data.json', 'r') as f:
            dataFile = json.loads(f.read())
        for chunk in dataFile["chunks"].keys():
            chunkDict = dataFile["chunks"][chunk]["metrics"]
            if includeHeatMap:
                heat = dataFile["chunks"][chunk]["heat"]
            else:
                heat = 0
            rDCR = chunkDict["relativeDCReadability"]
            lD = chunkDict["lexicalDiversity"]
            tTS = chunkDict["topTopicSimilarity"]
            posC = chunkDict["posComposition"]
            syllRate = chunkDict['syllableRate']
            posCList = []
            for tag in posTags:
                if tag in posC:
                    posCList.append(posC[tag])
                else:
                    posCList.append(0)
            chunkTopicScores = dict()
            for row in chunkDict["sharedTopicScores"]:
                chunkTopicScores[row[0]] = row[1]
            sharedTopicScoreList = []
            for topic in dataFile["metadata"]["topicScores"]:
                if topic[0] in chunkTopicScores:
                    relativeDiff = (chunkTopicScores[topic[0]] - topic[1])
                    sharedTopicScoreList.append(chunkTopicScores[topic[0]])
                else:
                    #really high number to indicate no significant topic mention in chunk
                    sharedTopicScoreList.append(5)
            row = [chunk, rDCR, lD, tTS, syllRate]
            row.extend(posCList)
            row.extend(sharedTopicScoreList)
            row.append(heat)
            writer.writerow(row)
    outCSV.close()

if __name__ == "__main__":
    #for id in os.listdir('test_data'):
    #    print("Processing " + id)
    #    if os.path.exists(f'test_data\\{id}\\{id}-data.json') == False:
    #        videoProcessing(f'test_data\\{id}\\{id}-heatmap.csv',
    #                    f'processed_test_data\\{id}.json', 
    #                    f'test_data\\{id}\\{id}-wholeTranscript.txt',
    #                    f'test_data\\{id}\\{id}-transcript.json',
    #                    id, f'test_data\\{id}\\{id}-data.json')
    convertToCSV()
#print(heatmapMedian('test_data\\_eGNSuTBc60\\_eGNSuTBc60-heatmap.csv'))
    
    

