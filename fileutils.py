"""File utilities
"""
import os
import shutil
import zipfile
import requests
from tqdm import tqdm
import gdown

def zip_directory(folder_path, zip_name):
    """Create .zip directory"""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, rel_path)

def create_or_clear_directory(path):
    """Create a directory, if existing clear its contents"""
    if os.path.exists(path):
        # Clear directory
        print("Clearing directory")
        shutil.rmtree(path)
    # Create empty directory
    os.makedirs(path)

def create_directory(path):
    """Create directory if it does not exist"""
    # Create empty directory
    if os.path.exists(path):
        print("Directoy already exists!")
    else:
        os.makedirs(path)

def datasetdownload_gdown(url, local_filename):
    """Download dataset from google drive"""
    # Download the folder
    gdown.download_folder(url, quiet=False, use_cookies=False)
    with zipfile.ZipFile("./GiantMIDI-PIano/midis_v1.2" + ".zip", 'r') as zip_ref:
        print("\nExtracting...")
        zip_ref.extractall(local_filename)

def datasetdownload(url, local_filename):
    """Download dataset from URL"""
    # Stream download with progress bar
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    with open(local_filename + ".zip", 'wb') as file, tqdm(
        desc="Downloading",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as barval:
        for data in response.iter_content(block_size):
            file.write(data)
            barval.update(len(data))

    # Unzip after download
    with zipfile.ZipFile(local_filename + ".zip", 'r') as zip_ref:
        print("\nExtracting...")
        zip_ref.extractall(local_filename)

    print("Done! Dataset is in the " + local_filename + " folder.")

def get_all_files_recursive(folder):
    """Get contants of a folder recursively"""
    all_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)
    return all_files
