import xarray as xr
import cfgrib

#Function to convert GRIB input to XArray
def input_conversion(grib_file):
    
    #Process GRIB file using cfgrib
    with xr.open_dataset(grib_file, engine='cfgrib') as mf:
        return mf.to_array()

#Function to convert XArray input to CSV file
def csv_conversion(meteo_arr):
    meteo_arr.name = 'met_d'

    #Convert to Dataset
    met_data = meteo_arr.to_dataset()
    
    #Convert to Dataframe
    met_frame = met_data.to_dataframe()
    
    #Convert to CSV
    met_frame.to_csv('Output/csv_out.csv')