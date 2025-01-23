import numpy
import pandas as pd


def get_raw_data_and_wavelengths(path: str):
    df = pd.read_excel(path, header=None)
    np_array = df.to_numpy()
    wavelengths = numpy.array(np_array[0])
    data = numpy.array(np_array[1:])
    return data, wavelengths
