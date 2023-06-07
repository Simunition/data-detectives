import xarray as xr
import cfgrib

def input_conversion(grib_file):
    with xr.open_dataset(grib_file, engine='cfgrib') as mf:
        return mf.to_array()

def csv_conversion(meteo_arr):
    meteo_arr.name = 'met_d'
    met_data = meteo_arr.to_dataset()
    met_frame = met_data.to_dataframe()
    met_frame.to_csv('Output/csv_out.csv')