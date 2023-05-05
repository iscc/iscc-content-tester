import json
import os

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"
dest_dir = "/iscc/annotated_videos/"

with open(annotation_file, 'r') as f:
    data = json.load(f)

for video in data:
    video_id = video["video_id"]
    for segment in video["segments"]:
        start_time = segment["start_time"]
        end_time = segment["end_time"]
        video_file = f"{video_id}.mp4"
        src_path = os.path.join(src_dir, video_file)
        dest_path = os.path.join(dest_dir, video_id, video_file)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        os.rename(src_path, dest_path)
        print(f"Annotated video {src_path} moved to {dest_path}")