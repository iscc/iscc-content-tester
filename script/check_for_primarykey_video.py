import os

primary_keys = ["ytHe8aJyjfk", "QXNIyKLfbJ4"]
video_dir = "/iscc/videos720"

available_videos = {}
missing_videos = {}

for key in primary_keys:
    video_files = []
    for subkey, subvalue in data.get(key, {}).items():
        video_files += [f"{key}_{subkey}_{video}.mp4" for video in subvalue]
    
    available_videos[key] = []
    missing_videos[key] = []

    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        if os.path.isfile(video_path):
            available_videos[key].append(video_file)
        else:
            missing_videos[key].append(video_file)

print("Available videos:")
for key, videos in available_videos.items():
    print(f"{key}: {len(videos)} videos")
    for video in videos:
        print(video)

print("\nMissing videos:")
for key, videos in missing_videos.items():
    print(f"{key}: {len(videos)} videos")
    for video in videos:
        print(video)
