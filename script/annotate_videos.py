import os
import shutil
import json
from tqdm import tqdm

# set input and output directories
input_dir = "/iscc/videos720/"
output_dir = "/iscc/annotated_videos/"

# load annotation data
with open('/iscc/git/FIVR-200K/dataset/annotation.json', 'r') as f:
    annotation = json.load(f)

# iterate over each video and copy it to the corresponding directory
total_videos = sum(len(v) for k, v in annotation.items() for kk, vv in v.items() for _ in vv)
with tqdm(total=total_videos, desc="Copying videos") as pbar:
    for video_id, video_data in annotation.items():
        video_dir = os.path.join(output_dir, video_id)
        os.makedirs(video_dir, exist_ok=True)
        for query_type, query_list in video_data.items():
            query_dir = os.path.join(video_dir, query_type)
            os.makedirs(query_dir, exist_ok=True)
            for query in query_list:
                src_path = os.path.join(input_dir, query + ".mp4")
                dest_path = os.path.join(query_dir, query + ".mp4")
                if os.path.exists(src_path):
                    shutil.copyfile(src_path, dest_path)
                    pbar.update(1)
                    remaining_videos = total_videos - pbar.n
                    pbar.set_postfix(eta=f"{remaining_videos // pbar.rate:.0f}s")
                else:
                    print(f"Skipping {src_path}: File does not exist")
