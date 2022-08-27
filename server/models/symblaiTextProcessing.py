import json
import requests
import os
import re
import string
import copy
from typing import Union
from datetime import datetime, timedelta

#url = "https://api.symbl.ai/oauth2/token:generate"
"""
headers = {
  "Content-Type": "application/json"
}

request_body = {
  "type": "application",
  "appId": appId
  "appSecret": appSecret
}

response = requests.post(url, headers=headers, json=request_body)

print(response.json())
"""


def mergeChunkedTranscripts(inputFilePath: str, outputFilePath: str):
    """
    Given a transcript chunked into timestamps, return an overall transcript of the text.
    inputFilePath: the JSON file to read
    outputFilePath: a text file to write the transcript to.
    """
    with open(inputFilePath, 'r') as f:
        chunkedTranscript = json.loads(f.read())
        with open(outputFilePath, 'w') as fw:
            for chunk in chunkedTranscript:
                fw.write(chunk["text"])

def mergeAllChunkedTranscripts(inDir:str, outDir:str):
    """
    merges all chunked transcripts found in a given directory and writes the merged transcripts as text files
    inDir: the directory where the chunked transcripts are stored
    outDir:the directory to store the merged transcripts
    """
    
    for transcript in os.listdir(inDir):
        id = transcript.split('.')[0]
        print(f"processing {id}")
        outFile = f"{outDir}\\{id}\\{id}-wholeTranscript.txt"
        inFile = inDir + '\\' + transcript
        os.makedirs(os.path.dirname(outFile), exist_ok=True)
        mergeChunkedTranscripts(inFile, outFile)

def splitConversationBySpeaker(transcriptPath:str) -> Union[list, str]:
    """
    Turns a text file of a conversation in a list of lists divided by speaker.
    Speakers must be clearly delineated by all-caps and a colon at the end.
    Examples inclde: PROFESSOR:, DAVE:, BILLY BOB:, PROFESSOR LANGDON:, AUDIENCE:, etc. \n
    transcriptPath: the conversation to process \n
    returns a list of dicts containing the speaker and the . Also returns a set of unique speakers.
    If no speakers are found, all text goes into a single sublist and is associated with NARRATOR:.
    Any words before a speaker is found are tagged as NARRATOR:.
    """
    with open(transcriptPath, 'r') as f:
        transcript = f.read()
    #finds all speakers with a single word or two words (e.g. PROFESSOR:, DAVE:, BILLY BOB:)
    speakers = re.findall(r'[A-Z]{2,} \b[A-Z]{2,}:|[^A-Z] \b[A-Z]{2,}:', transcript)
    if len(speakers) > 0: 
        lowerCase = set(string.ascii_lowercase + string.punctuation)
        for speakerIdx in range(len(speakers)):
            #remove additional characters needed for regex matching
            if speakers[speakerIdx][0] in lowerCase:
                speakers[speakerIdx] = speakers[speakerIdx][2:]
        #split transcript by speakers
        uniqueSpeakers = set(speakers)
        splitRegex = '|'.join(map(re.escape, uniqueSpeakers))
        splitConversation = re.split(splitRegex, transcript)
        #check if there is any content before the lecture and remove it.
        if (len(splitConversation) - len(speakers)) == 1:
            speakers.insert(0, "NARRATOR:")
        elif (len(splitConversation) - len(speakers)) > 1:
            raise Exception("Speaker and splitConversation do not match!")     
    else:
        #if there are no speakers, assume only the narrator is speaking
        speakers.append("NARRATOR")
    #match speaker to the corresponding text
    speakerSpeechMatch = []
    for excerptIdx in range(len(splitConversation)):
        speakerSpeechMatch.append({"name": speakers[excerptIdx], "content": splitConversation[excerptIdx]})
    return speakerSpeechMatch, set(speakers)

def convertToConversation(fullTranscriptPath:str, timedTranscriptPath:str, outFile: str):
    """
    Turns a text file into a conversation JSON file for symbl.ai.
    fullTranscriptPath: a text file containing the full transcript.
    timedTranscriptPath: a JSON file containing a transcript with timestamps
    outFile: the JSON file to write to.
    """
    id = fullTranscriptPath.split('-')[0]
    splitConversation, uniqueSpeakers = splitConversationBySpeaker(fullTranscriptPath)
    #match speaker and text to timestamps
    with open(timedTranscriptPath, 'r') as f:
        timedTranscript = json.loads(f.read())
    speakerIdx = 0
    currentTime = datetime.today()
    #adds timestamps to the speakers
    if uniqueSpeakers == {"NARRATOR:"}:
        #special case for no speaker in transcript
        splitConversation[0]["startTime"] = currentTime
        finalTime = timedelta(seconds=timedTranscript[-1]["start"] + timedTranscript[-1]["duration"])
        splitConversation[0]["endTime"] = currentTime + finalTime
    else:
        if "NARRATOR:" in uniqueSpeakers:
            #special case for words before any speaker in transcript.
            splitConversation[0]["startTime"] = currentTime
            speakerIdx += 1
        for line in timedTranscript:
            if any(word in line["text"] for word in uniqueSpeakers):
                #starttime has to be in datetime format, so add seconds of YT video to the current datetime.
                splitConversation[speakerIdx]["startTime"] = currentTime + timedelta(seconds=line["start"])
                #set endtime for the previous entry as a hundredth of a second before the current entry's start time
                if speakerIdx > 0:
                    splitConversation[speakerIdx - 1]["endTime"] = currentTime + timedelta(seconds=line["start"]-0.01)
                #set endTime for the last speaker as the final timestamp plus duration
                if speakerIdx == len(splitConversation) - 1:
                    finalTime = timedelta(seconds=timedTranscript[-1]["start"] + timedTranscript[-1]["duration"])
                    splitConversation[speakerIdx]["endTime"] = currentTime + finalTime
                speakerIdx += 1
    #write to symbl.ai JSON format
    outJSONDict = dict()
    outJSONDict["name"] = id #conversation name
    outJSONDict["messages"] = []
    for part in splitConversation:
        messageDict = {
            "payload": {
                "content": part["content"]
            },
            "from": {
                "userId": part["name"],
                "name": part["name"]
            },
            "duration": {
                "startTime": str(part["startTime"]),
                "endTime": str(part["endTime"])
            }
        }
        outJSONDict["messages"].append(copy.deepcopy(messageDict))
    with open(outFile, 'w') as json_file:
        json_file.write(json.dumps(outJSONDict, indent = 4))


class symblAITranscript:
    def __init__(self, filepath: str, appId, appSecret, accessToken):
        """
        filepath: the filepath to the transcript to be uploaded (as a properly formatted JSON file)
        """
        self.filepath = filepath
        self.appId = appId
        self.appSecret = appSecret
        self.accessToken = accessToken
    def uploadToSymblAI(self):
        pass
        


if __name__ == "__main__":
    with open("secrets.txt", 'r') as secrets:
        secretsList = json.loads(secrets.read())
        appId = secretsList["appId"]
        appSecret = secretsList["appSecret"]
        accessToken = secretsList["accessToken"]
    testScriptId = 'uNKDw46_Ev4'
    convertToConversation('new_processed_test_data\\4RX_lpoGRBg\\4RX_lpoGRBg-wholeTranscript.txt', 'test_data\\4RX_lpoGRBg\\4RX_lpoGRBg-transcript.json','temp.json')