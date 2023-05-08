import os
import json
import shutil

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"
dest_dir = "/iscc/annotated_videos/"

# Load annotation data from JSON file
with open(annotation_file, "r") as f:
    data = json.load(f)

# Loop through videos in the annotation data
for video_id, video_data in data.items():
    for event_type, event_videos in video_data.items():
        for video_file in event_videos:
            src_path = os.path.join(src_dir, video_file + ".mp4")
            dest_path = os.path.join(dest_dir, event_type, video_file + ".mp4")
            shutil.copyfile(src_path, dest_path)