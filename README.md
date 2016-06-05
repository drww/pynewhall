# pynewhall - A definite work-in-progress.

For more depth on the nature of the model, see the Java version at: https://github.com/drww/newhall

## Quickstart Guide:

Make sure you already have Python installed on your system.  To quickly check if Python can be found in your operating system's path, open up a terminal and type "python" to see if you get an interpreter (type "exit()" to leave).  If you are on Windows and do not have Python installed, this guide will be helpful: http://www.howtogeek.com/197947/how-to-install-python-on-windows/

1. Either clone the pynewhall git repository, or download as a ZIP and expand the archive.
2. Open up a command line and move to the pynewhall directory.
3. Call "python pynewhall.py --help" to review how to use what's implemented so far:
<pre>
usage: pynewhall.py [-h] [--version] [--debug] [--run RUN] [--whc WHC]
                    [--sao SAO] [--amp AMP]
PyNewhall 0.8 - CLI Interface for the Newhall Simulation Model
optional arguments:
  -h, --help  show this help message and exit
  --version   show version and exit
  --debug     report extra debugging information while running
  --run RUN   input dataset or directory containing several datasets
  --whc WHC   override default waterholding capacity (200 mm)
  --sao SAO   override default soil-air offset (2.5 deg C)
  --amp AMP   override default soil-air relationship amplitude (0.66)
</pre>
4. Run one or all of the datasets in misc/ using the --run option.  Results will output to the terminal.
5. If desired, modify waterholding capacity, soil-air offset relationship, and soil-air amplitude relationship using --whc, --sao, and --amp.  Results will preserve your input parameters.

## Developer Guide:

PyNewhall has no outside dependencies currently, other than what is in Python 2.7.  However, in order to use the unit tests, you will need to install Nose (use pip).  Once installed, when in the root pynewhall directory, you can run them like as follows:

<pre>
% nosetests -v
tests.test_simulation.test_mead89 ... ok
tests.test_simulation.test_column97 ... ok
tests.test_simulation.test_column98 ... ok
tests.test_simulation.test_ajo20008 ... ok
tests.test_simulation.test_pendleton ... ok
tests.test_simulation.test_chadron ... ok
tests.test_simulation.test_pittsburg1950 ... ok
tests.test_simulation.test_piedmont1937 ... ok
----------------------------------------------------------------------
Ran 8 tests in 0.041s
OK
</pre>

## Example:

<pre>
% python pynewhall/pynewhall.py --run misc/PENDLETON.json
INFO:main:Using simulation model default parameters for following simulation runs.
INFO:main:Completed simulation run: Pendleton, OR (1971 - 2000)
========== NEWHALL RESULTS ===============================================
  Water Holding Capacity (mm): 200.0
  Soil-Air Offset (deg C): 2.5
  Soil-Air Amplitude (%): 0.66
  Annual Rainfall (mm): 335.5
  Annual Water Balance (mm): -477.1
  Summer Water Balance (mm): -314.0
  Mean Potential Evapotranspiration (mm): [33.8, 35.3, 44.7, 56.9, 77.2, 93.1, 113.3, 113.6, 96.1, 70.8, 44.5, 33.2]
  # Days Dry post-Summer Solstice: 120
  # Days Moist post-Winter Solstice: 75
  # Cumulative Days Dry: 199
  # Cumulative Days Moist/Dry: 51
  # Cumulative Days Moist: 110
  # Cumulative Days Dry >5C: 199
  # Cumulative Days Moist >5C: 110
  # Cumulative Days Moist/Dry >5C: 51
  # Consecutive Days Mostly Moist: 161
  # Consecutive Days Mostly Moist >8C: 161
  Temperature Regime: Thermic
  Moisture Regime: Xeric
  Regime Subdivision 1: Dry
  Regime Subdivision 2: Xeric
  Input Dataset:
  ========== NEWHALL DATASET ===============================================
    Site Name: Pendleton, OR
    Country: USA
    Latitude (deg): 33.3
    Latitude Hemisphere: N
    Longitude (deg): -117.35
    Longitude Hemisphere: E
    Elevation (m/ft): 75.0
    Start Year: 1971
    End Year: 2000
    Metric Units?: False
    Precipitation (mm/in): [3.0, 2.91, 2.67, 0.81, 0.32, 0.14, 0.08, 0.02, 0.14, 0.46, 0.93, 1.73]
    Temperature (deg C/F): [55.1, 56.0, 56.8, 59.6, 63.3, 66.7, 70.5, 71.9, 70.6, 65.5, 59.1, 55.2]
</pre>
