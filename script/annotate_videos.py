import os
import json
import shutil
from tqdm import tqdm

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"
dest_dir = "/iscc/annotated_videos/"

with open(annotation_file) as f:
    data = json.load(f)

total_videos = sum(len(v) for k in data for v in data[k].values())

with tqdm(total=total_videos, unit="videos", dynamic_ncols=True) as pbar:
    for video_id, video_data in data.items():
        video_path = os.path.join(src_dir, video_id + ".mp4")
        if not os.path.exists(video_path):
            pbar.write(f"Skipping {video_id}: file not found")
            continue

        for query, query_videos in video_data.items():
            query_path = os.path.join(dest_dir, query)
            os.makedirs(query_path, exist_ok=True)

            for query_video in query_videos:
                src_path = os.path.join(src_dir, query_video + ".mp4")
                dest_path = os.path.join(query_path, query_video + ".mp4")

                if os.path.exists(dest_path):
                    pbar.write(f"Skipping {dest_path}: file already exists")
                    pbar.update(1)
                    continue

                shutil.copyfile(src_path, dest_path)
                pbar.update(1)
                remaining_videos = total_videos - pbar.n
                pbar.set_postfix(eta=f"{remaining_videos // pbar.avg:.0f}s")
