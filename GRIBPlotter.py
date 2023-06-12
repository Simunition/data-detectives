import GRIBLoader as gl
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Function to plot XArray data on a world map
def plot_grib(xarray_data):
    # Extract the data and coordinates
    data = xarray_data['gh'].values
    lats = xarray_data['latitude'].values
    lons = xarray_data['longitude'].values

    # Extract the date
    # Access the datetime component of the DataArray
    time_datetime = xarray_data['time'].dt
    # Extract the year, month, and day as strings
    year = time_datetime.strftime('%Y').item()
    month = time_datetime.strftime('%m').item()
    day = time_datetime.strftime('%d').item()

    # Create a plot with a world map using Cartopy
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.stock_img()
    ax.gridlines(draw_labels=True)

    # Plot the data
    plt.contourf(lons, lats, data, transform=ccrs.PlateCarree())

    # Set title and labels
    plt.title('500hPa Geopotential Height Zero-Hour Forecast for ' + month + '/' + day + '/' + year)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    output_filename = "zero_hour_plot.png"
    output_path = os.path.join('Output/', output_filename)
    plt.savefig(output_path)

if __name__ == "__main__":
    import os
    import random
    import re
    import datetime
    import GRIBDownloader as gd

    # Check if the test/000 folder exists
    test_folder = "./download/test/012"
    if not os.path.exists(test_folder):
        # Download the GRIB data for the specified year range
        gd.download_grib_data(2013, 2013)

    # Get list of files in the test/000 folder
    files = os.listdir(test_folder)

    # Choose a random file from the list
    random_file = random.choice(files)

    # Create the full path to the chosen file
    grib_file = os.path.join(test_folder, random_file)

    # Assuming you already have an XArray dataset, xarray_data
    xarray_data = gl.convert_grib(grib_file)
    plot_grib(xarray_data)
