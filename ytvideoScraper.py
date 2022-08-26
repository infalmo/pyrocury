from youtube_transcript_api import YouTubeTranscriptApi
import re
import urllib
from youtube_transcript_api.formatters import JSONFormatter
import os

class youtubeVideo:
    def __init__(self, link:str):
        self.link = link
        #extract id from url with regex
        url_data = urllib.parse.urlparse(link)
        query = urllib.parse.parse_qs(url_data.query)
        self.id = query["v"][0]
        self.transcript = None
        self.heatmap = None

    def getTranscript(self):
        self.transcript = YouTubeTranscriptApi.get_transcript(self.id, languages=['en'])
        
    def saveTranscript(self):
        if self.transcript == None:
            self.getTranscript()
        formatter = JSONFormatter()
        # .format_transcript(transcript) turns the transcript into a JSON string.
        json_formatted = formatter.format_transcript(self.transcript)
        # Now we can write it out to a file.
        filepath = f'test_data/{self.id}/{self.id}-transcript.json'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json_file.write(json_formatted)



#video = youtubeVideo('https://www.youtube.com/watch?v=LQTSyRrQBVY&ab_channel=SouthChinaMorningPost')
#video.saveTranscript()



