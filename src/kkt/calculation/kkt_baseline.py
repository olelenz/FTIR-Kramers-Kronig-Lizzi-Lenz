import numpy
import matplotlib
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm import tqdm
import os
from datetime import datetime

matplotlib.use('Agg')


def init_plots(output_path: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subdirectory_name = f"plots_{timestamp}"
    output_path = os.path.join(output_path, subdirectory_name)
    os.makedirs(output_path, exist_ok=True)
    return output_path


def kkt_baseline_correction(data: numpy.array, wavelengths: numpy.array, output_dir: str):
    output_path = init_plots(output_dir)
    idx_800 = numpy.argmin(numpy.abs(wavelengths - 968))
    idx_1800 = numpy.argmin(numpy.abs(wavelengths - 1200))
    indexed_data = zip(data, range(len(data)))

    data_corrected = []
    for data_point in indexed_data:
        data_corrected.append(kkt_baseline_correction_row(data_point, wavelengths, idx_800, idx_1800, output_path))

    return data_corrected


def kkt_baseline_correction_concurrent(data: numpy.array, wavelengths: numpy.array, output_dir: str):
    output_path = init_plots(output_dir)
    idx_800 = numpy.argmin(numpy.abs(wavelengths - 968))
    idx_1800 = numpy.argmin(numpy.abs(wavelengths - 1200))
    indexed_data = zip(data, range(len(data)))
    with ThreadPoolExecutor(max_workers=8) as executor:
        func = partial(kkt_baseline_correction_row, wavelengths=wavelengths, left_idx=idx_800, right_idx=idx_1800, output_path=output_path)
        results = list(tqdm(executor.map(func, indexed_data), total=len(data), desc="Processing Rows Baseline"))
    return results


def kkt_baseline_correction_row(indexed_data_point: tuple, wavelengths: numpy.array, left_idx: float, right_idx: float, output_path: str):
    data_row = indexed_data_point[0]
    cur_index = indexed_data_point[1]
    y1 = data_row[left_idx]
    y2 = data_row[right_idx]

    x1 = wavelengths[left_idx]
    x2 = wavelengths[right_idx]

    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    baseline = numpy.poly1d([slope, intercept])
    data_row_corrected = data_row - baseline(wavelengths)

    output_path = os.path.join(output_path, f"KKT_{cur_index}.png")

    fig, ax = plt.subplots()
    ax.plot(wavelengths, data_row, label='Original', linestyle='--')
    ax.plot(wavelengths, baseline(wavelengths), label='Baseline')
    ax.plot(wavelengths, data_row_corrected, label='Corrected')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title(f'Baseline Correction for Row {cur_index}')
    ax.legend()
    fig.savefig(output_path)
    plt.close(fig)

    return data_row_corrected
