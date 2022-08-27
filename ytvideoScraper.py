from youtube_transcript_api import YouTubeTranscriptApi
import re
import urllib
from youtube_transcript_api.formatters import JSONFormatter
import heatmapExtractor
import os
import csv

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
        """
        Gets a transcript with the given Youtube URL
        """
        self.transcript = YouTubeTranscriptApi.get_transcript(self.id, languages=['en'])
        
    def saveTranscript(self):
        """
        Saves the transcript as a json file.
        """
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

    def getHeatmap(self):
        """
        Gets a heatmap for the provided YouTube URL.
        """
        self.heatmap = heatmapExtractor.getHeatmapPoints(self.link)
    def saveHeatmap(self, header:bool = True):
        """
        Saves the heatmap as a CSV file.
        header: specieifes whether to include a header row or not.
        """
        if self.heatmap == None:
            self.getHeatmap()
        filepath = f'test_data/{self.id}/{self.id}-heatmap.csv'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            write = csv.writer(f)
            if header:
                write.writerow(["Time (Fraction of video)", "Normalized Popularity"])
            write.writerows(self.heatmap)

video = youtubeVideo('https://www.youtube.com/watch?v=LQTSyRrQBVY&ab_channel=SouthChinaMorningPost')
video.saveTranscript()
video.saveHeatmap()



