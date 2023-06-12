import os
from ftplib import FTP
import random

# FTP server details
ftp_host = "usgodae.org"
ftp_user = "anonymous"
ftp_pass = "anonymous"

# Remote folder and file pattern
remote_folder = "/pub/outgoing/fnmoc/models/navgem_0.5/"
grib_twelve_prefix = "US058GMET-GR1mdl.0018_0056_01200F0RL"
grib_zero_prefix = "US058GMET-GR1mdl.0018_0056_00000F0RL"
grib_suffix = "0100_005000-000000geop_ht"

# Local folders for train and test data
twelve_train_folder = "./train/012/"
twelve_test_folder = "./test/012/"
zero_train_folder = "./train/000/"
zero_test_folder = "./test/000/"

# Create local folders if they don't exist
os.makedirs(twelve_train_folder, exist_ok=True)
os.makedirs(twelve_test_folder, exist_ok=True)
os.makedirs(zero_train_folder, exist_ok=True)
os.makedirs(zero_test_folder, exist_ok=True)

# Connect to FTP server
ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)

def download_files_from_folder(folder_path):
    # Change to the remote directory
    ftp.cwd(folder_path)

    # Get list of files matching the pattern
    file_list = []
    ftp.retrlines("NLST", file_list.append)

    # Separate files based on prefixes
    twelve_files = [filename for filename in file_list if filename.startswith(grib_twelve_prefix) and filename.endswith(grib_suffix)]
    zero_files = [filename for filename in file_list if filename.startswith(grib_zero_prefix) and filename.endswith(grib_suffix)]

    # Calculate the split for train and test files
    twelve_total_files = len(twelve_files)
    twelve_train_count = int(twelve_total_files * 0.9)
    twelve_test_count = twelve_total_files - twelve_train_count

    zero_total_files = len(zero_files)
    zero_train_count = int(zero_total_files * 0.9)
    zero_test_count = zero_total_files - zero_train_count

    # Randomly shuffle the file lists
    random.shuffle(twelve_files)
    random.shuffle(zero_files)

    # Download and split the twelve files
    for i, filename in enumerate(twelve_files):
        local_filepath = os.path.join(twelve_train_folder if i < twelve_train_count else twelve_test_folder, filename)
        with open(local_filepath, "wb") as file:
            ftp.retrbinary("RETR " + filename, file.write)

    # Download and split the zero files
    for i, filename in enumerate(zero_files):
        local_filepath = os.path.join(zero_train_folder if i < zero_train_count else zero_test_folder, filename)
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
        if year_folder.isdigit() and 2013 <= int(year_folder) <= 2022:
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
