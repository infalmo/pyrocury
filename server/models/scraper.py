from bs4 import BeautifulSoup
import csv
import os
from requests_html import HTMLSession
import urllib
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter


class Heatmap:
    def extractCurve(
        url: str, renderTime: int = 4, retries: int = 0, maxRetries: int = 2
    ) -> str:
        """
        Given a Youtube URL, returns a string of letters and numbers representing
        a series of bezier curves mapping the heatmap.
        url: the YouTube URL to extract the heatmap from.
        renderTime: the time in seconds for the program to wait for requests_html to render the HTML file.
                    A LOWER VALUE MAY RESULT IN THE FUNCTION NOT WORKING!
        retries: the number of retries this function has taken
                    INTERNAL VARIABLE; MODIFY AT YOUR OWN RISK
        maxRetries: the maximium number of tries this function will take in trying to get the heatmap.
                    INTERNAL VARIABLE; MODIFY AT YOUR OWN RISK
        Throws an exception if the function is unable to find the heatmap after a given number of retries.
        """
        session = HTMLSession()
        response = session.get(url)
        response.html.render(sleep=renderTime)  # needs time to render
        soup = BeautifulSoup(response.html.html, "html.parser")
        heatmapElement = soup.find(class_="ytp-heat-map-path")
        if heatmapElement == None:
            if retries > maxRetries:
                raise Exception(
                    "request_html could not render HTML file or heatmap does not exist. "
                    + "Try incrementing renderTime or double checking if a heatmap does exist for the given url."
                )
            else:
                print(
                    "Unable to get heatmap from the HTML file. Retrying with increased renderTime."
                )
                return Heatmap.extractCurve(url, renderTime * 1.5, retries + 1)
        return heatmapElement["d"]

    def convertCurve(heatmap: str) -> list:
        """
        given a heatmap extracted from extractHeatmapCurve, converts the curve
        into a time-based set of datapoints.
        heatmap: a string of numbers and letters from extractHeatmapCurve
        return: a list of tuples, where the first value of the tuple is time
                of the datapoint as a fraction of the whole video (from 0 to 1)
        """
        datapointsStr = heatmap.split(" ")
        datapointsStr = datapointsStr[5:]  # Shifts list
        # gets every fourth element. The first through 3rd elements are for modelling the bezier curve
        datapointsStr = datapointsStr[::4]
        datapointsStr.pop()  # pop last two elements (2 points at 99.5%) so that we get 100 datapoints evenly spaced.
        datapointsStr.pop()
        datapoints = []
        for datapoint in datapointsStr:
            x, y = datapoint.split(",")
            # convert strings to a floats and normalize values to between 0 and 1
            # x, y = float(x), float(y)
            x = round((float(x) - 5) / 1000, 3)
            y = round((100 - float(y)) / 100, 3)
            datapoints.append((x, y))
        return datapoints

    def getPoints(url: str) -> list:
        """
        Given a YouTube URL with a heatmap, return a list of tuples with viewership datapoints.
        See extractHeatmapCurve and convertHeatmapCurve for further details.
        """
        return Heatmap.convertCurve(Heatmap.extractCurve(url, renderTime=10))


class youtubeVideo:
    def __init__(self, link: str):
        self.link = link
        # extract id from url with regex
        url_data = urllib.parse.urlparse(link)
        query = urllib.parse.parse_qs(url_data.query)
        self.id = query["v"][0]
        self.transcript = None
        self.heatmap = None

    def getTranscript(self):
        """
        Gets a transcript with the given Youtube URL
        """
        self.transcript = YouTubeTranscriptApi.get_transcript(self.id, languages=["en"])

    def saveTranscript(self, filename: str):
        """
        Saves the transcript as a json file.
        filepath: the file path and name to save the transcript to.
        """
        if self.transcript == None:
            self.getTranscript()
        formatter = JSONFormatter()
        # .format_transcript(transcript) turns the transcript into a JSON string.
        json_formatted = formatter.format_transcript(self.transcript)
        # Now we can write it out to a file.

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as json_file:
            json_file.write(json_formatted)

    def getHeatmap(self):
        """
        Gets a heatmap for the provided YouTube URL.
        """
        self.heatmap = Heatmap.getPoints(self.link)

    def saveHeatmap(self, filename: str, header: bool = True):
        """
        Saves the heatmap as a CSV file.
        filepath: the file path and name to save the heatmap to.
        header: specifies whether to include a header row or not.
        """
        if self.heatmap == None:
            self.getHeatmap()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8", newline="") as f:
            write = csv.writer(f)
            if header:
                write.writerow(["Time (Fraction of video)", "Normalized Popularity"])
            write.writerows(self.heatmap)


def download_testdata(link_file: str):
    """Generates and saves testdata (transcript, heatmap) from links in link_file."""

    with open(link_file, "r") as f:
        for url in f.readlines():
            print(f"Downloading data from {url}")
            video = youtubeVideo(url)
            heatmapFilepath = f"test_data/{video.id}/{video.id}-heatmap.csv"
            transcriptFilepath = f"test_data/{video.id}/{video.id}-transcript.json"
            if os.path.exists(transcriptFilepath) == False:
                video.saveTranscript(transcriptFilepath)
            if os.path.exists(heatmapFilepath) == False:
                video.saveHeatmap(heatmapFilepath)


if __name__ == "__main__":
    download_testdata("links.txt")
