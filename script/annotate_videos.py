import json
import os

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"
dest_dir = "/iscc/annotated_videos/"

with open(annotation_file, "r") as f:
    data = json.load(f)

for video in data["videos"]:
    video_name = video["video_id"] + ".mp4"
    if os.path.isfile(os.path.join(src_dir, video_name)):
        for annotation in video["annotations"]:
            start_time = annotation["segment"][0]
            end_time = annotation["segment"][1]
            dest_path = os.path.join(dest_dir, annotation["query"], video_name)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            src_path = os.path.join(src_dir, video_name)
            os.system(f"ffmpeg -i {src_path} -ss {start_time} -to {end_time} -c:v libx264 -c:a aac -strict experimental -b:a 192k -ac 2 -ar 44100 -vf scale=640:360 {dest_path}")
            print(f"Video '{video_name}' annotated with query '{annotation['query']}' and saved to '{dest_path}'")
    else:
        print(f"Video '{video_name}' not found in '{src_dir}'")
