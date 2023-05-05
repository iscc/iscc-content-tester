import os
import json

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"
dest_dir = "/iscc/annotated_videos/"

# Load annotation data from JSON file
with open(annotation_file, "r") as f:
    data = json.load(f)

# Loop through videos in the annotation data
for video_id, video_data in data.items():
    video_file = video_data["file_path"].split("/")[-1]
    src_path = os.path.join(src_dir, video_file)
    dest_path = os.path.join(dest_dir, video_data["query"], video_file)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Move video file to destination directory
    os.rename(src_path, dest_path)