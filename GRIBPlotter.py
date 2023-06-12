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
    plt.title('500hPa on World Map')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Assuming you already have an XArray dataset, xarray_data
    xarray_data = gl.convert_grib('/home/cfc/Python/GRIBFiles/US058GMET-GR1mdl.0018_0056_00000F0RL2023012512_0006_000000-000000geop_ht')
    plot_grib(xarray_data)