# pynewhall - A definite work-in-progress.

For more depth on the nature of the model, see the Java version at: https://github.com/drww/newhall

Quickstart Guide:

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

Developer Guide:

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
