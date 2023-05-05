import json
import os

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"
dest_dir = "/iscc/annotated_videos/"

with open(annotation_file, "r") as f:
    data = json.load(f)

for video_id, video_data in data.items():
    video_file = video_id + ".mp4"
    src_path = os.path.join(src_dir, video_file)
    dest_path = os.path.join(dest_dir, video_data["query"], video_file)
    if os.path.exists(src_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        os.rename(src_path, dest_path)
    else:
        print(f"Video {src_path} not found.")