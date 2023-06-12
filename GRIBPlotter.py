import cfgrib
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Function to load and plot XArray data
def plot_grib(xarray_input):
    # Load the XArrary and extract the data
    ds = xarray_input
    data = ds.data_vars['gh'].values
    lats = ds.coords['latitude'].values
    lons = ds.coords['longitude'].values

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