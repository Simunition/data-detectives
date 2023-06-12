import os
import random
import GRIBDownloader as gd

def get_grib():
    # Check if the test/000 folder exists, if not download the GRIB data for the specified year range
    test_folder = "./download/test/012"
    if not os.path.exists(test_folder):
        gd.download_grib_data(2013, 2013)

    # Get list of files in the test/000 folder
    files = os.listdir(test_folder)

    # Choose a random file from the list and create grib_file variable
    random_file = random.choice(files)
    grib_file = os.path.join(test_folder, random_file)
    return grib_file