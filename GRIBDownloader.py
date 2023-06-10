import os
from ftplib import FTP
import random

# FTP server details
ftp_host = "usgodae.org"
ftp_user = "anonymous"
ftp_pass = "anonymous"

# Remote folder and file pattern
remote_folder = "/pub/outgoing/fnmoc/models/navgem_0.5/"
file_prefix = "US058GMET-GR1mdl.0018_0056_01200F0RL"
file_suffix = "0100_005000-000000geop_ht"

# Local folders for train and test data
train_folder = "./train/"
test_folder = "./test/"

# Create local folders if they don't exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# Connect to FTP server
ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)

def download_files_from_folder(folder_path):
    # Change to the remote directory
    ftp.cwd(folder_path)

    # Get list of files matching the pattern
    file_list = []
    ftp.retrlines("NLST", file_list.append)

    # Filter files based on pattern
    filtered_files = [filename for filename in file_list if filename.startswith(file_prefix) and filename.endswith(file_suffix)]

    # Calculate the split for train and test files
    total_files = len(filtered_files)
    train_count = int(total_files * 0.9)
    test_count = total_files - train_count

    # Randomly shuffle the file list
    random.shuffle(filtered_files)

    # Download and split the files
    for i, filename in enumerate(filtered_files):
        local_filepath = os.path.join(train_folder if i < train_count else test_folder, filename)
        with open(local_filepath, "wb") as file:
            ftp.retrbinary("RETR " + filename, file.write)

    # Return to the parent directory
    ftp.cwd("..")

# Recursive function to iterate through year folders and subfolders
def explore_year_folders():
    # Change to the remote directory
    ftp.cwd(remote_folder)

    # Get list of year folders
    year_folders = []
    ftp.retrlines("NLST", year_folders.append)

    # Iterate through year folders
    for year_folder in year_folders:
        if year_folder.isdigit() and 2013 <= int(year_folder) <= 2023:
            year_folder_path = os.path.join(remote_folder, year_folder)
            ftp.cwd(year_folder_path)
            subfolders = []
            ftp.retrlines("NLST", subfolders.append)
            for subfolder in subfolders:
                subfolder_path = os.path.join(year_folder_path, subfolder)
                download_files_from_folder(subfolder_path)
            ftp.cwd("..")

# Start exploring the remote directory and download files from subfolders
explore_year_folders()

# Disconnect from the FTP server
ftp.quit()

print("Download completed.")
