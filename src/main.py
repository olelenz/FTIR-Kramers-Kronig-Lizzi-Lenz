import numpy
import sys
import os
from pathlib import Path

from kkt import kkt_utils
from kkt.calculation import kkt_phase as phase, kkt_absorbance as absorbance, kkt_baseline as baseline

RAW_DATA_INPUT_PATH: str = "INPUT_PATH"
FINAL_DATA_OUTPUT_PATH: str = "OUTPUT_PATH"


def main():
    if len(sys.argv) < 3:
        raise ValueError("The input path as well as the output path must be provided!")

    # get raw data
    global RAW_DATA_INPUT_PATH
    RAW_DATA_INPUT_PATH = sys.argv[1]
    if not Path(RAW_DATA_INPUT_PATH).exists():
        raise ValueError("Did not find the raw data file!")

    # check dir
    global FINAL_DATA_OUTPUT_PATH
    FINAL_DATA_OUTPUT_PATH = sys.argv[2]
    output_dir = os.path.dirname(FINAL_DATA_OUTPUT_PATH)
    if not os.path.exists(output_dir):
        raise ValueError("Did not find the output directory!")

    # import wavelengths from excel and save data in required format
    data, wavelengths = kkt_utils.get_raw_data_and_wavelengths(RAW_DATA_INPUT_PATH)

    # calculate phase:
    kkt_phase = phase.kkt_phase_calculations_concurrent(data, wavelengths)

    # calculate absorbance:
    kkt_absorbance = absorbance.kkt_absorbance_calculations_concurrent(data, wavelengths, kkt_phase)

    # calculate baseline corrected:
    kkt_baseline_corrected = baseline.kkt_baseline_correction_concurrent(kkt_absorbance, wavelengths, output_dir)

    # save results
    numpy.savetxt(FINAL_DATA_OUTPUT_PATH, kkt_baseline_corrected)


if __name__ == '__main__':
    main()
