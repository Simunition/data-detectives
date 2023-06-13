import ProcesssGRIB as pg

#Convert GRIB to XARRAY
def convert_grib(file_name):
    grib_input = file_name

    #Convert GRIB to XArray
    x_out = pg.xarray_conversion(grib_input)
    return x_out

#Testing and CSV Output
def convert_xarray_to_csv(xarray_in):
    #Convert XArray to CSV
    pg.csv_conversion(xarray_in)
    print(xarray_in)