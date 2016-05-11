import sys
import subprocess
from time import time

####################################
##	Print to File
####################################
filename = './data/'  +  str(sys.argv[1]) + '.wav'
print filename
record_args = ["arecord", "-d", "5", "-f", "dat", "-c", "1", "-D", "hw:2,0", filename]
p = subprocess.call(record_args)
print "Finished"
