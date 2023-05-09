import os
import json

# Set the path to the video directory
video_dir = '/iscc/videos720'

# Set the path to the annotation file
annotation_file = '/iscc/git/FIVR-200K/dataset/annotation.json'

# Load the annotation file
with open(annotation_file, 'r') as f:
    data = json.load(f)

# Get the list of primary keys
primary_keys = list(data.keys())

# Initialize lists to store available and missing videos
available_videos = []
missing_videos = []

# Loop through the primary keys
for key in primary_keys:
    # Get the file name for the primary key video
    file_name = key + '.mp4'

    # Check if the video file exists in the video directory
    if os.path.isfile(os.path.join(video_dir, file_name)):
        available_videos.append(key)
    else:
        missing_videos.append(key)

# Print the results
print('Available videos:')
print(available_videos)
print()
print('Missing videos:')
print(missing_videos)
