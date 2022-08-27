import json
import requests
import os

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
    
#mergeChunkedTranscripts('processed_test_data\\QOtA76ga_fY.json', 'test.txt')

"""
access_token =
conversation_id = "4602321464459264"

headers = {
  "Authorization": "Bearer " + access_token,
  "Content-Type": "application/json"
}

response = requests.request(
  method="GET", 
  url="https://api.symbl.ai/v1/conversations/" + conversation_id + "/topics?sentiment=true&parentRefs=true",
  headers=headers
)
"""
class symblAITranscript:
    def __init__(self, filepath: str):
        """
        filepath: the filepath to the transcript to be uploaded
        """
        self.filepath = filepath
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

if __name__ == "__main__":
    with open("secrets.txt", 'r') as secrets:
        secretsList = json.loads(secrets.read())
        appId = secretsList["appId"]
        appSecret = secretsList["appSecret"]
        accessToken = secretsList["accessToken"]
    mergeAllChunkedTranscripts("processed_test_data", "new_processed_test_data")