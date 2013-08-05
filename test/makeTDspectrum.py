"""
To use this script, first you need to tell Python where to find GaussSum:

   set PYTHONPATH=C:\Tools\GaussSum\branch22x\src;%PYTHONPATH%

Then, run it as follows:

  python makeTDspectrum.py myfile.log
    or
  python makeTDspectrum.py *\*.log
"""

import os
import sys
import glob

gausssumdir = os.path.join("..")
sys.path.append(os.path.join(gausssumdir, "src"))

from gausssum.electrontrans import ET
from gausssum.cclib.parser import ccopen
from gausssum.cclib.parser.utils import convertor

def parse(filename):

    log = ccopen(filename)
    log.logger.setLevel(50) # (logging.ERROR)
    return log.parse()
    
def runone(filename):
    data = parse(filename)
    ET(None, sys.stdout, data, filename, 200, 500, 500, 3000, True,
       None, False)

if __name__ == "__main__":

    if len(sys.argv) == 1:
        sys.exit("You need to specify a file or list of files")

    filenames = sys.argv[1:]
    if len(filenames) == 1 and "*" in filenames[0]:
        filenames = glob.glob(filenames[0])

    for filename in filenames:
        print "\nParsing %s...." % filename
        runone(filename)
        print 
        
