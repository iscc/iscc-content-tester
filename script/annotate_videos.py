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
    for query in video_data:
        query_dir = os.path.join(dest_dir, query)
        if not os.path.exists(query_dir):
            os.makedirs(query_dir)

        for video_file in video_data[query]:
            src_path = os.path.join(src_dir, video_file + ".mp4")
            dest_path = os.path.join(query_dir, video_file + ".mp4")
            if not os.path.exists(src_path):
                print(f"{src_path} does not exist, skipping...")
                continue

            shutil.copyfile(src_path, dest_path)
            print(f"Video {video_file}.mp4 copied to {query_dir}")