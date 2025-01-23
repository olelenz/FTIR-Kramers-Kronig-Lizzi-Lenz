import numpy
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm import tqdm


def kkt_phase_calculations(data: numpy.array, wavelengths: numpy.array):
    output = []
    for row in data:
        output.append(kkt_phase_row(row, wavelengths))
    return numpy.array(output)


def kkt_phase_calculations_concurrent(data: numpy.array, wavelengths: numpy.array):
    with ThreadPoolExecutor(max_workers=8) as executor:
        func = partial(kkt_phase_row, wavelengths=wavelengths)
        results = list(tqdm(executor.map(func, data), total=len(data), desc="Processing Rows Phase"))
    return numpy.array(results)


def kkt_phase_row(row: numpy.array, wavelengths: numpy.array):
    n_col: int = len(row)
    row = numpy.array(1/(10**row))
    row_ln = numpy.log(numpy.sqrt(numpy.array(row)))
    output = [calculate_sumt(n_col, p, row_ln, wavelengths) for p in range(n_col)]
    return numpy.array(output)


def calculate_sumt(n_col: int, p: int, row_ln: numpy.array, wavelengths: numpy.array) -> float:
    a_p_mask = numpy.arange(n_col) != p
    sumt_vec = (row_ln[a_p_mask] / ((wavelengths[a_p_mask] ** 2) - (wavelengths[p] ** 2)))
    first_and_last_mask = numpy.isin(numpy.arange(n_col), [0, n_col - 1])  # to account for multiplying by two in those two cases
    sumt_vec[first_and_last_mask[a_p_mask]] *= 2
    sumt = wavelengths[p] * numpy.sum(sumt_vec) / numpy.pi
    return sumt
