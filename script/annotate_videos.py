import json
import os
import shutil
from tqdm import tqdm

with open('/iscc/git/FIVR-200K/dataset/annotation.json') as f:
    data = json.load(f)

src_dir = '/iscc/videos720/'
dest_dir = '/iscc/annotated_videos/'

total_videos = sum(len(data[key][sub_key]) for key in data for sub_key in data[key])
pbar = tqdm(total=total_videos, desc="Copying videos", unit=" video")

for key in data:
    print(f"Processing key: {key}")
    if key + '.mp4' not in os.listdir(src_dir):
        print(f"{key}.mp4 not found in {src_dir}. Skipping...")
        continue
    
    dest_key_dir = os.path.join(dest_dir, key)
    os.makedirs(dest_key_dir, exist_ok=True)
    
    for sub_key in data[key]:
        print(f"Processing subkey: {sub_key}")
        dest_sub_dir = os.path.join(dest_key_dir, sub_key)
        os.makedirs(dest_sub_dir, exist_ok=True)
        
        for video_id in data[key][sub_key]:
            src_path = os.path.join(src_dir, key + '.mp4')
            dest_path = os.path.join(dest_sub_dir, video_id + '.mp4')
            
            if not os.path.isfile(src_path):
                print(f"{src_path} not found. Skipping...")
                pbar.update(1)
                continue
            
            print(f"Copying {src_path} to {dest_path}")
            shutil.copyfile(src_path, dest_path)
            pbar.update(1)
            remaining_videos = total_videos - pbar.n
            pbar.set_postfix(completed=f"{pbar.n}/{total_videos}", eta=f"{remaining_videos // pbar.rate:.0f}s")

print("Done!")
