import GRIBProcessor as pg
import os
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Function to plot XArray data on a world map
def plot_grib(xarray_data):
    # Extract the data and coordinates
    data = xarray_data['gh'].values
    lats = xarray_data['latitude'].values
    lons = xarray_data['longitude'].values

    # Access the datetime component of the DataArray and create date variables
    time_datetime = xarray_data['time'].dt
    year = time_datetime.strftime('%Y').item()
    month = time_datetime.strftime('%m').item()
    day = time_datetime.strftime('%d').item()

    # Create a plot with a world map using Cartopy
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.stock_img()
    ax.gridlines(draw_labels=True)

    # Compute plot min/max and set the contour value range
    vmin = data.min().item()
    vmax = data.max().item()
    levels = np.linspace(vmin, vmax, 100)

    # Plot the data
    plt.contourf(lons, lats, data, levels=levels, transform=ccrs.PlateCarree())

    # Add colorbar
    cbar = plt.colorbar(shrink=0.642,  pad=0.1)
    cbar.set_label('Geopotential Height (meters)')

    # Set title and labels
    plt.title('500hPa Geopotential Height Zero-Hour Forecast for ' + month + '/' + day + '/' + year)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Save plot
    output_filename = "zero_hour_plot.png"
    output_path = os.path.join('Output/', output_filename)
    plt.savefig(output_path)

if __name__ == "__main__":
    import GRIBTester as tg
    grib_file = tg.get_grib()

    # Convert to XArray and plot
    xarray_data = pg.xarray_conversion(grib_file)
    plot_grib(xarray_data)
