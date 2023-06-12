import os
import random
import shutil
from ftplib import FTP

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
download_folder = "./download/"
train_folder = "./download/train/"
test_folder = "./download/test/"
twelve_train_folder = os.path.join(train_folder, "012")
twelve_test_folder = os.path.join(test_folder, "012")
zero_train_folder = os.path.join(train_folder, "000")
zero_test_folder = os.path.join(test_folder, "000")

# Create local folders if they don't exist
os.makedirs(download_folder, exist_ok=True)
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)
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

    # Filter files based on prefixes
    matching_files = [filename for filename in file_list if (filename.startswith(grib_twelve_prefix) or filename.startswith(grib_zero_prefix)) and filename.endswith(grib_suffix)]

    # Download matching files into the download folder
    for filename in matching_files:
        local_filepath = os.path.join(download_folder, filename)
        with open(local_filepath, "wb") as file:
            ftp.retrbinary("RETR " + filename, file.write)

    # Return to the parent directory
    ftp.cwd("..")


# Recursive function to iterate through year folders and subfolders
def explore_year_folders(start_year, end_year):
    # Change to the remote directory
    ftp.cwd(remote_folder)

    # Get list of year folders
    year_folders = []
    ftp.retrlines("NLST", year_folders.append)

    # Iterate through year folders
    for year_folder in year_folders:
        if year_folder.isdigit() and int(start_year) <= int(year_folder) <= int(end_year):
            year_folder_path = os.path.join(remote_folder, year_folder)
            ftp.cwd(year_folder_path)
            subfolders = []
            ftp.retrlines("NLST", subfolders.append)
            for subfolder in subfolders:
                subfolder_path = os.path.join(year_folder_path, subfolder)
                download_files_from_folder(subfolder_path)
            ftp.cwd("..")

# Function to sort files in the download folder
def sort_files_in_download_folder():
    # Get list of files in the download folder
    files = os.listdir(download_folder)

    # Separate files based on prefixes
    twelve_files = [filename for filename in files if filename.startswith(grib_twelve_prefix)]
    zero_files = [filename for filename in files if filename.startswith(grib_zero_prefix)]

    # Calculate the split for train and test files
    twelve_train_count = int(len(twelve_files) * 0.9)
    zero_train_count = int(len(zero_files) * 0.9)

    # Randomly shuffle the file lists
    random.shuffle(twelve_files)
    random.shuffle(zero_files)

    # Move files to appropriate folders
    for i, filename in enumerate(twelve_files):
        source_path = os.path.join(download_folder, filename)
        if i < twelve_train_count:
            destination_path = os.path.join(twelve_train_folder, filename)
        else:
            destination_path = os.path.join(twelve_test_folder, filename)
        shutil.move(source_path, destination_path)

    for i, filename in enumerate(zero_files):
        source_path = os.path.join(download_folder, filename)
        if i < zero_train_count:
            destination_path = os.path.join(zero_train_folder, filename)
        else:
            destination_path = os.path.join(zero_test_folder, filename)
        shutil.move(source_path, destination_path)

    print("Sorting completed.")

if __name__ == "__main__":
    # Download 2013 data
    explore_year_folders(2013, 2013)
    sort_files_in_download_folder()

# Disconnect from the FTP server
ftp.quit()