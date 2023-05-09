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
    if key + ".mp4" not in os.listdir(src_dir):
        print(f"{key}.mp4 not found in {src_dir}")
        continue
    
    for sub_key in data[key]:
        dest_sub_dir = os.path.join(dest_dir, key, sub_key)
        os.makedirs(dest_sub_dir, exist_ok=True)
        
        for video_id in data[key][sub_key]:
            src_path = os.path.join(src_dir, key + ".mp4")
            dest_path = os.path.join(dest_sub_dir, video_id + '.mp4')
            
            if not os.path.isfile(src_path):
                print(f"{src_path} not found")
                pbar.update(1)
                continue
            
            shutil.copyfile(src_path, dest_path)
            if not os.path.isfile(os.path.join(dest_sub_dir, key + '.mp4')):
                shutil.copyfile(src_path, os.path.join(dest_sub_dir, key + '.mp4'))
            pbar.update(1)
            completed_videos = pbar.n
            remaining_videos = total_videos - completed_videos
            pbar.set_postfix(completed=f"{completed_videos}/{total_videos}", remaining=f"{remaining_videos} videos")
            
pbar.close()
print("Copying complete!")
