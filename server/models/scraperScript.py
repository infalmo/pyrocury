from ytVideoScraper import youtubeVideo
import os

def main():
    with open('links.txt', 'r') as f:
        for url in f.readlines():
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