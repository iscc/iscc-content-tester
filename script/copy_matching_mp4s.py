import os
import shutil
from tqdm import tqdm

srcdir1 = "/iscc/videos480"
srcdir2 = "/iscc/videos720"
destdir = "/iscc/same_videos"

# Get a list of all .mp4 files in the first source directory
files = [f for f in os.listdir(srcdir1) if f.endswith(".mp4")]

for file in tqdm(files, desc="Checking files", unit="file"):
    print(f"Checking file: {file}")
    # Check if the file also exists in the second source directory
    if os.path.exists(os.path.join(srcdir2, file)):
        print(f"Found matching file in {srcdir2}")
        # Create a new folder in the destination directory named after the file
        foldername = os.path.splitext(file)[0]
        folderpath = os.path.join(destdir, foldername)
        os.makedirs(folderpath, exist_ok=True)
        print(f"Created folder: {folderpath}")
        
        # Copy the two files into the new folder
        srcpath1 = os.path.join(srcdir1, file)
        dstpath1 = os.path.join(folderpath, file[:-4] + "_480.mp4")
        shutil.copy2(srcpath1, dstpath1)
        print(f"Copied {srcpath1} to {dstpath1}")
        
        srcpath2 = os.path.join(srcdir2, file)
        dstpath2 = os.path.join(folderpath, file)
        shutil.copy2(srcpath2, dstpath2)
        print(f"Copied {srcpath2} to {dstpath2}")
    else:
        print(f"No matching file found in {srcdir2}")
