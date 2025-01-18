import os
import subprocess
import sys
import glob
from tqdm import tqdm

def convert_webm_to_mp4(input_path, output_path, codec="libx264"):
    """
    Converts a WebM file to MP4 using FFmpeg.

    Args:
        input_path (str): Path to the input .webm file.
        output_path (str): Path to the output .mp4 file.
        codec (str): Video codec to use. Defaults to libx264.
    """
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', codec,
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-progress', 'pipe:1',
        output_path
    ]

    try:
        # Run FFmpeg command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Print progress
        for line in process.stdout:
            if 'out_time_ms' in line:
                time = line.split('=')[1].strip()
                print(f"\rConverting {os.path.basename(input_path)}: {int(int(time)/1000000)} seconds processed", end='')
        
        process.wait()
        
        if process.returncode == 0:
            print(f"\nSuccessfully converted: {input_path} -> {output_path}")
        else:
            print(f"\nError converting {input_path}: {process.stderr.read()}")
    except Exception as e:
        print(f"\nError converting {input_path}: {str(e)}")

def batch_convert(directory, codec="libx264"):
    """
    Converts all .webm files in the specified directory to .mp4.

    Args:
        directory (str): Directory containing .webm files.
        codec (str): Video codec to use. Defaults to libx264.
    """
    print(f"Searching for .webm files in: {directory}")
    webm_files = glob.glob(os.path.join(directory, '*.webm'))

    if not webm_files:
        print("No .webm files found in the specified directory.")
        print("Files in the directory:")
        for file in os.listdir(directory):
            print(file)
        return

    print(f"Found {len(webm_files)} .webm files.")
    for webm_file in tqdm(webm_files, desc="Converting files"):
        mp4_file = os.path.splitext(webm_file)[0] + '.mp4'
        convert_webm_to_mp4(webm_file, mp4_file, codec)

def main():
    if len(sys.argv) < 3:
        print("Usage: python convert.py [single|batch] [path]")
        sys.exit(1)

    mode = sys.argv[1]
    path = sys.argv[2]

    # Expand user and get absolute path
    full_path = os.path.abspath(os.path.expanduser(path))
    
    # Insert "/Desktop" into the path if it's not already there
    if "Desktop" not in full_path:
        parts = full_path.split(os.path.sep)
        if "YouTubeScraper" in parts:
            youtube_scraper_index = parts.index("YouTubeScraper")
            parts.insert(youtube_scraper_index, "Desktop")
            full_path = os.path.sep.join(parts)

    print(f"Attempting to access: {full_path}")

    if mode == 'single':
        if not os.path.isfile(full_path):
            print(f"The specified file does not exist: {full_path}")
            sys.exit(1)
        if not full_path.lower().endswith('.webm'):
            print("The input file must have a .webm extension.")
            sys.exit(1)
        output = os.path.splitext(full_path)[0] + '.mp4'
        convert_webm_to_mp4(full_path, output)
    elif mode == 'batch':
        if not os.path.isdir(full_path):
            print(f"The specified directory does not exist: {full_path}")
            parent_dir = os.path.dirname(full_path)
            print(f"Contents of parent directory ({parent_dir}):")
            for item in os.listdir(parent_dir):
                print(item)
            sys.exit(1)
        batch_convert(full_path)
    else:
        print("Invalid mode. Use 'single' to convert one file or 'batch' to convert all .webm files in a directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
