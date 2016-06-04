# pynewhall - A definite work-in-progress.

For more depth on the nature of the model, see the Java version at: https://github.com/drww/newhall

Quickstart Guide:

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
