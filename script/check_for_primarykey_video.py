import os
import json

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"

with open(annotation_file, "r") as f:
    data = json.load(f)

for primary_key in data:
    print(f"\nVideos for primary key '{primary_key}':")
    for secondary_key in data[primary_key]:
        for video_id in data[primary_key][secondary_key]:
            video_path = os.path.join(src_dir, f"{video_id}.mp4")
            if os.path.exists(video_path):
                print(f" - {video_id}.mp4 is available")
            else:
                print(f" - {video_id}.mp4 is missing")