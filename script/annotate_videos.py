import os
import json
import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the paths from the configuration file
annotations_file = '/iscc/git/FIVR-200K/dataset/annotation.json'
src_dir = '/iscc/videos720/'
dest_dir = '/iscc/annotated_videos/'

# Read the annotations from the JSON file
with open(annotations_file, 'r') as f:
    annotations = json.load(f)

# Create a new directory for each annotation and save the corresponding files
for annotation in annotations:
    directory_name = annotation
    os.makedirs(os.path.join(dest_dir, directory_name), exist_ok=True)
    for file_id in annotations[annotation]:
        file_name = file_id + '.mp4'
        src_path = os.path.join(src_dir, file_name)
        dest_path = os.path.join(dest_dir, directory_name, file_name)
        os.rename(src_path, dest_path)
