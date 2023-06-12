import os
import cfgrib

#Function to convert GRIB input to XArray
def input_conversion(grib_file):
    
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
    met_frame.to_csv('Output/csv_out.csv', index=False)

if __name__ == "__main__":
    # Assuming you already have an XArray dataset, xarray_data
    grib_file = '/home/cfc/Python/GRIBFiles/US058GMET-GR1mdl.0018_0056_00000F0RL2023012512_0006_000000-000000geop_ht'
    xarray_test = input_conversion(grib_file)
    csv_conversion(xarray_test)