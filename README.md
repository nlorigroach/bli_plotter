# bli_plotter

This is a Python program that plots data and extracts association values from BLI-ISA experiments.

### Input 
A 'raw data' csv exported from the Octet Data Analysis software

### Output
* .png files showing the time-series plots of each sample's data, 8 samples per page
* .csv file containing association values matched with each sample's filename and well position

### Usage
`$ python3 bli_plotter.py raw_data.csv`
        

#### Requirements
Python 3 with matplotlib, numpy, and pandas
