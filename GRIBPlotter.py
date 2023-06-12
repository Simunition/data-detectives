import GRIBLoader as gl
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Function to plot XArray data on a world map
def plot_grib(xarray_data):
    # Extract the data and coordinates
    data = xarray_data['gh'].values
    lats = xarray_data['latitude'].values
    lons = xarray_data['longitude'].values

    # Create a plot with a world map using Cartopy
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.stock_img()
    ax.gridlines(draw_labels=True)

    # Plot the data
    plt.contourf(lons, lats, data, transform=ccrs.PlateCarree())

    # Set title and labels
    plt.title('500hPa Geopotential Height')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    import os
    import random
    import GRIBDownloader as gd

    gd.download_grib_data(2013, 2013)
    
    # Get list of files in the test/000 folder
    folder_path = "./download/test/000"
    files = os.listdir(folder_path)

    # Choose a random file from the list
    random_file = random.choice(files)

    # Create the full path to the chosen file
    grib_file = os.path.join(folder_path, random_file)

    # Assuming you already have an XArray dataset, xarray_data
    xarray_data = gl.convert_grib(grib_file)
    plot_grib(xarray_data)