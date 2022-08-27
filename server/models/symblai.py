import json
import os


def cache_data(data_name: str, video_id: str, data: dict):
    file_path = f"new_processed_test_data/{data_name}/{video_id}.json"
    os.makedirs(file_path, exist_ok=True)

    json.dump(data, open(file_path, "w+"))
