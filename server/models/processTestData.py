import csv
import json
from math import ceil
import os
import statistics
from unicodedata import name


def chunkVideo(transcript: list, heatmap: list) -> list:
    """Merges transcript and heatmap as 2 minute chunks

    output:
    [{"text": "...", start: 240.0, heat: 0.35}, ...]
    """

    output = []

    l_bound = 0.0
    merged_ts = {"text": "", "start": l_bound}
    for ts in transcript:
        while l_bound + 120 <= ts["start"]:
            output.append(merged_ts)

            l_bound += 120
            merged_ts = {"text": "", "start": l_bound}

        merged_ts["text"] += " " + ts["text"]
    output.append(merged_ts)

    for o in output:
        o["text"] = o["text"].replace("\n", " ")

    interval_cnt = ceil(len(output) / 100)
    for i in range(len(output)):
        l = i * interval_cnt

        vals = []
        for x in range(l, min(l + interval_cnt, len(heatmap))):
            vals.append(float(heatmap[x][1]))
        vals.sort()

        if vals == []:
            output[i]["heat"] = 0.0
        else:
            output[i]["heat"] = statistics.median(vals)

    return output


def processTestData(testDataDir: str):
    os.makedirs("processed_test_data", exist_ok=True)

    for f in os.listdir(testDataDir):
        print("Processing:", f)

        if os.path.exists(f"processed_test_data/{f}.json"):
            print("Cached data found. Skipping...")
            continue

        # Assumes only folders in testDataDir.
        transcriptFile = f"{testDataDir}/{f}/{f}-transcript.json"
        heatmapFile = f"{testDataDir}/{f}/{f}-heatmap.csv"

        transcript = json.load(open(transcriptFile))

        heatmap = []
        cnt = 0
        for row in csv.reader(open(heatmapFile), delimiter=","):
            cnt += 1
            if cnt == 1:
                continue

            heatmap.append(row)

        data = chunkVideo(transcript, heatmap)

        with open(f"processed_test_data/{f}.json", "w+") as o:
            json.dump(data, o)

        print("Processed.\n")


if __name__ == "__main__":
    processTestData("test_data")
