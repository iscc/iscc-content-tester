import os
import json
import shutil
from tqdm import tqdm

annotation_file = "/iscc/git/FIVR-200K/dataset/annotation.json"
src_dir = "/iscc/videos720/"
dest_dir = "/iscc/annotated_videos/"

with open(annotation_file, "r") as f:
    data = json.load(f)

for key, values in tqdm(data.items()):
    for sub_key, sub_values in values.items():
        sub_folder = os.path.join(dest_dir, sub_key)
        os.makedirs(sub_folder, exist_ok=True)
        for video_id in sub_values:
            src_path = os.path.join(src_dir, f"{video_id}.mp4")
            dest_path = os.path.join(sub_folder, f"{video_id}.mp4")
            if not os.path.isfile(src_path):
                tqdm.write(f"{src_path} does not exist. Skipping...")
                continue
            shutil.copyfile(src_path, dest_path)
    os.rename(os.path.join(dest_dir, key + ".mp4"), os.path.join(dest_dir, sub_folder, key + ".mp4"))

remaining_videos = sum(len(v) for v in data.values())
with tqdm(total=remaining_videos, desc="Copying files") as pbar:
    for key, values in data.items():
        for sub_key, sub_values in values.items():
            for video_id in sub_values:
                src_path = os.path.join(src_dir, f"{video_id}.mp4")
                dest_path = os.path.join(dest_dir, sub_key, f"{video_id}.mp4")
                if not os.path.isfile(src_path):
                    pbar.write(f"{src_path} does not exist. Skipping...")
                    remaining_videos -= 1
                    pbar.total = remaining_videos
                    continue
                shutil.copyfile(src_path, dest_path)
                pbar.update(1)
                remaining_videos -= 1
                pbar.total = remaining_videos
                pbar.set_postfix(eta=f"{remaining_videos // pbar.n * pbar.refresh_rate:.0f}s")
