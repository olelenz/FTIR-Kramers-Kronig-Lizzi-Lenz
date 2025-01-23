import math
import numpy
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm import tqdm


def kkt_absorbance_calculations(data: numpy.array, wavelengths: numpy.array, phase: numpy.array):
    absorbance = []
    zipped_data = zip(data, phase)
    for zipped_point in zipped_data:
        absorbance.append(kkt_absorbance_row(zipped_point, wavelengths))
    return absorbance


def kkt_absorbance_calculations_concurrent(data: numpy.array, wavelengths: numpy.array, phase: numpy.array):
    zipped_data = zip(data, phase)
    with ThreadPoolExecutor(max_workers=8) as executor:
        func = partial(kkt_absorbance_row, wavelengths=wavelengths)
        results = list(tqdm(executor.map(func, zipped_data), total=len(data), desc="Processing Rows Absorbance"))
    return numpy.array(results)


def kkt_absorbance_row(raw_and_phase: tuple, wavelengths: numpy.array):
    raw_data = raw_and_phase[0]
    row_phase = raw_and_phase[1]
    len_data: int = len(raw_data)
    raw_data = numpy.array(1 / (10 ** raw_data))
    max_data: float = max(x for x in raw_data if x > 0)
    data_scaled = [0.85 * x / max_data for x in raw_data]
    data_sqrt = numpy.sqrt(data_scaled)
    ene = [((1 - data_scaled[p]) / (1 + data_scaled[p] - 2 * data_sqrt[p] * numpy.cos(row_phase[p])))
           if p < len(data_scaled) and p < len(row_phase)
           else None
           for p in range(len_data)]
    ka = [(2 * data_sqrt[p] * (numpy.sin(row_phase[p])) / (
            1 + data_scaled[p] - 2 * data_sqrt[p] * numpy.cos(row_phase[p])))
          if p < len(data_scaled) and p < len(row_phase)
          else None
          for p in range(len_data)]

    min_ene = min(x for x in ene if x is not None)
    min_ka = min(x for x in ka if x is not None)

    if any(x <= 0 for x in ene):
        ene = [x - min_ene for x in ene if x is not None]

    if any(x <= 0 for x in ka):
        ka = [x - min_ka for x in ka if x is not None]

    data_abs = [2 * math.pi * wavelengths[p] * ka[p] * numpy.log(math.exp(1))
                for p in range(len_data)]

    # normalize
    max_abs = max(data_abs)
    if max_abs != 0:
        return [x / max_abs for x in data_abs]
    else:
        return data_abs
