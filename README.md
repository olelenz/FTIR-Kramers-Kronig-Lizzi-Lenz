<div align="center">
  <h3 align="center">
    FTIR-Kramers-Kronig-Lizzi-Lenz
  </h3>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project
<em>
This code takes a reflectance spectrum and applies the Kramers-Kronig Transformation (as approximated by Lichvar) to calculate the phase shift and the reflective index. From such variables, the absorption spectra are obtained.

The input file needs an equally spaced wavelength on the top row, and the spectra acquisition from the second row on.
</em>

<!-- GETTING STARTED -->
## Getting Started

Install the necessary requirements:
```sh
pip install -r requirements.txt
```

Run the program providing the path to the input .xlsx file as well as the output file:
```sh
python ./src/main.py "./resources/example_input.xlsx" "./output/output.txt"
```
Note that the first argument must be a path to a .xlsx file and the second argument a path to the output file (if the file does not exist, it will be created).
In addition to the results in form of a text file, a subdirectory with a plot for each input line will be created as well.

### Prerequisites
Python version
  * 3.8 or above

<!-- LITERATURE -->
## Literature
P. Lichvár, M. Liška, and D. Galusek, “What is the true Kramers-Kronig transform?,” Ceram. - Silikaty, vol. 46, no. 1, pp. 25–27, 2002.
