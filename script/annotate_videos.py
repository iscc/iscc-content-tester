import json
import os
import shutil
from tqdm import tqdm

with open('/iscc/git/FIVR-200K/dataset/annotation.json') as f:
    data = json.load(f)

src_dir = '/iscc/videos720/'
dest_dir = '/iscc/annotated_videos/'

total_videos = sum(len(data[key][sub_key]) for key in data for sub_key in data[key])
pbar = tqdm(total=total_videos, desc="Copying videos")

for key in data:
    print(f"Processing key: {key}")
    if not os.path.exists(os.path.join(src_dir, f"{key}.mp4")):
        print(f"Video for key {key} not found in {src_dir}")
        continue
    
    dest_key_dir = os.path.join(dest_dir, key)
    os.makedirs(dest_key_dir, exist_ok=True)
    
    for sub_key in data[key]:
        print(f"Processing sub_key: {sub_key}")
        dest_sub_dir = os.path.join(dest_key_dir, sub_key)
        os.makedirs(dest_sub_dir, exist_ok=True)
        
        for video_id in data[key][sub_key]:
            print(f"Processing video: {video_id}")
            src_path = os.path.join(src_dir, f"{key}.mp4")
            dest_path = os.path.join(dest_sub_dir, f"{video_id}.mp4")
            
            if not os.path.isfile(src_path):
                print(f"Source file {src_path} not found")
                pbar.update(1)
                continue
            
            shutil.copyfile(src_path, dest_path)
            pbar.update(1)
            remaining_videos = total_videos - pbar.n
            pbar.set_postfix(completed=f"{pbar.n}/{total_videos}", 
                             eta=f"{remaining_videos // pbar.refresh_rate:.0f}s")
            print(f"Copied video {video_id} to {dest_path}")
            
print("Copying complete!")
