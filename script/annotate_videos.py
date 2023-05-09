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
    if not os.path.exists(os.path.join(src_dir, key+'.mp4')):
        print(f"Skipping primary key {key}. Video file not found.")
        continue
    
    dest_key_dir = os.path.join(dest_dir, key)
    os.makedirs(dest_key_dir, exist_ok=True)
    
    for sub_key in data[key]:
        dest_sub_dir = os.path.join(dest_key_dir, sub_key)
        os.makedirs(dest_sub_dir, exist_ok=True)
        
        for video_id in data[key][sub_key]:
            src_path = os.path.join(src_dir, key, video_id + '.mp4')
            dest_path = os.path.join(dest_sub_dir, video_id + '.mp4')
            
            if not os.path.isfile(src_path):
                print(f"Skipping video {src_path}. File not found.")
                pbar.update(1)
                continue
            
            shutil.copyfile(src_path, dest_path)
            pbar.update(1)
            remaining_videos = total_videos - pbar.n
            pbar.set_postfix(eta=f"{remaining_videos // pbar.avg:.0f}s")

print("Finished copying videos.")
