from ytVideoScraper import youtubeVideo
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api.formatters import JSONFormatter
import os
import json

def channelMostViewedScraper():
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    api_service_name = "youtube"
    api_version = "v3"
    #apiKey = API-KEY GOES HERE #environment variable
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = apiKey)
    urlList = []
    videos = []
    #get top 250 ocw video links, which definitely have transcripts and heatmaps
    request = youtube.search().list(
        channelId="UCEBb1b_L6zDS3xTUrIALZOw",
        part = "snippet",
        order = "viewCount",
        maxResults = 50,
        pageToken = "CMgBEAA",
    )
    response = request.execute()
    formatter = JSONFormatter()
    # .format_transcript(transcript) turns the transcript into a JSON string.
    json_formatted = formatter.format_transcript(response)
    with open('ocwPlaylist4.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)  

def loadJSON():
    """
    loads json files parsed from channelMostViewedScraper, extracts video IDs, and writes youtube URLs to ocwlinks.txt
    """
    videoURLs = []
    for i in range(5):
        f = open (f'ocwMostPopularVids\\ocwPlaylist{i}.json', "r")
        data = json.loads(f.read())
        
        for video in data["items"]:
            videoID = video["id"]["videoId"]
            videoURLs.append("https://www.youtube.com/watch?v=" + videoID + "\n")
        f.close()
    with open('ocwlinks.txt', 'w') as f:
        f.writelines(videoURLs)    

def main():
    #channelMostViewedScraper()
    loadJSON()
    #get from links.txt
    with open('ocwlinks.txt', 'r') as f:
        for url in f.readlines():
            urlList.append(url)

    for url in urlList:
        print(f"Downloading data from {url}")
        video = youtubeVideo(url)
        heatmapFilepath = f'test_data/{video.id}/{video.id}-heatmap.csv'
        transcriptFilepath = f'test_data/{video.id}/{video.id}-transcript.json'
        if os.path.exists(transcriptFilepath) == False:
            video.saveTranscript(transcriptFilepath)
        if os.path.exists(heatmapFilepath) == False:
            video.saveHeatmap(heatmapFilepath)


if __name__ == '__main__':
    main()