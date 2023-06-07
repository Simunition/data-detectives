import ProcesssGRIB as pg

grib_input = 'GRIBFiles/US058GMET-GR1mdl.0018_0056_00000F0RL2023012512_0006_000000-000000geop_ht'
x_out = pg.input_conversion(grib_input)
pg.csv_conversion(x_out)
print(x_out)
