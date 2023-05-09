import json
import os
import shutil
from tqdm import tqdm

with open('/iscc/git/FIVR-200K/dataset/annotation.json') as f:
    data = json.load(f)

src_dir = '/iscc/videos720/'
dest_dir = '/iscc/annotated_videos/'

available_videos = []
for key in data:
    if key in os.listdir(src_dir):
        available_videos.extend([key + '/' + video_id for sub_key in data[key] for video_id in data[key][sub_key]])

total_videos = len(available_videos)
pbar = tqdm(total=total_videos, desc="Copying videos")

for video_id in available_videos:
    key, video_id = video_id.split('/')
    for sub_key in data[key]:
        if video_id in data[key][sub_key]:
            src_path = os.path.join(src_dir, key, video_id + '.mp4')
            dest_key_dir = os.path.join(dest_dir, key)
            dest_sub_dir = os.path.join(dest_key_dir, sub_key)
            dest_path = os.path.join(dest_sub_dir, video_id + '.mp4')
            
            os.makedirs(dest_sub_dir, exist_ok=True)
            shutil.copyfile(src_path, dest_path)
            pbar.update(1)
            remaining_videos = total_videos - pbar.n
            pbar.set_postfix(eta=f"{remaining_videos // pbar.avg:.0f}s")
            break
else:
    pbar.close()
