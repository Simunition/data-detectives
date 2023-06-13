import os
import cfgrib

#Function to convert GRIB input to XArray
def xarray_conversion(grib_file):
    
    #Process GRIB file using cfgrib
    return cfgrib.open_datasets(grib_file)[0]

# Function to convert XArray input to CSV file
def csv_conversion(meteo_arr):

    # Rename the variable within the dataset
    meteo_arr = meteo_arr.rename({'gh': 'gh'})

    # Convert to DataFrame
    met_frame = meteo_arr.to_dataframe()

    # Reset index to convert multi-index to columns
    met_frame.reset_index(inplace=True)

    # Convert to CSV
    os.makedirs('Output', exist_ok=True)
    output_path = 'Output/csv_out.csv'
    met_frame.to_csv(output_path, index=False)

def grib_conversion(xarray_data, output_path):
    # Convert XArray dataset to GRIB
    grib_data = xarray_data.to_dask().reset_coords(drop=True)
    
    # Save as GRIB file
    os.makedirs('Output', exist_ok=True)
    output_path = 'Output/grib_out.grib'
    cfgrib.write(grib_data, output_path, index=False)

if __name__ == "__main__":
    import TestGRIB as tg
    grib_file = tg.get_grib()

    #Test XArray Conversion
    xarray_test = xarray_conversion(grib_file)
    print(xarray_test)

    #Test CSV Conversion
    csv_conversion(xarray_test)