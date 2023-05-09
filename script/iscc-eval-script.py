import os

def run_iscc_eval(dir_path, output_dir, binary_path):
    # Create the output directory if it doesn't already exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all subdirectories within the specified directory
    subdirs = [subdir for subdir in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, subdir))]

    for subdir in subdirs:
        # Construct the command to be executed for each subdirectory
        command = f"{binary_path} --verbose match content-code {os.path.join(dir_path, subdir)} 2>&1 | tee {os.path.join(output_dir, f'{subdir}.txt')}"

        # Execute the command
        os.system(command)


# Example usage:
if __name__ == '__main__':
    dir_path = '/iscc/annotated_videos'
    output_dir = '/iscc/iscc-eval-output'
    binary_path = '/iscc/git/iscc-eval'

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    run_iscc_eval(dir_path, output_dir, binary_path)
