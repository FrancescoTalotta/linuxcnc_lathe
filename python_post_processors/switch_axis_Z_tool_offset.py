#!/usr/bin/python
# This routine performs the X->Z and Z->X axis switching for the lathe on the normale XYZ machine
# and then adds additional g-code
from __future__ import print_function

__author__ = 'francesco'

import sys, os

BASE = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
sys.path.insert(0, os.path.join(BASE, "lib", "python"))

import re

passthrough = []

replace = []


def progress(a, b):
    if os.environ.has_key("AXIS_PROGRESS_BAR"):
        print >> sys.stderr, "FILTER_PROGRESS=%d" % int(a * 100. / b + .5)
        sys.stderr.flush()


def main():
    global feedrate, feedrat, radius
    feedrate  = 0
    feedrate2 = 0
    radius    = 0
    is_on     = True
    infile = sys.argv[1]
    f = open(infile, "r")
    for line in f:

# First switch 
        match_X_Z = re.match("(.*)X(.*)Z(.*)", line)
        if match_X_Z:
            before = match_X_Z.group(1)
            center = match_X_Z.group(2)
            last   = match_X_Z.group(3)
            string = (before + 'Z' + center + 'X' + last).replace("\r", "").replace("\n", "")
            print(string)
        elif not match_X_Z:
            match_X = re.match("(.*)X(.*)", line)
            if match_X:
                before = match_X.group(1)
                coord  = match_X.group(2)
                string = (before + 'Z' + coord).replace("\r", "").replace("\n", "")
                print(string)
            elif not match_X:
               match_Z = re.match("(.*)Z(.*)", line)
               if match_Z:
                   before = match_Z.group(1)
                   coord  = match_Z.group(2)
                   string = (before + 'X' + coord).replace("\r", "").replace("\n", "")
                   print(string)
               else:

# Then add additional code
                 match = re.match("T(\d{1,2})(.*)M(\d.*)", line)
                 if match:
                     tool = int(match.group(1))
                     print("M101 P%d" % tool)
                     print("T%d M6" % tool)
                     print("O100 call [%d]" % tool)
                 else:
                    print(line.replace("\r", "").replace("\n", ""))
         
                 match = re.match("(.*)STOCK RADIUS=(\d[.]\d\d)(.*)", line)
                 if match:
                    radius = float(match.group(2))
         
                 match = re.match("(.*)G21(.*)", line)
                 if match:
                    #print("G21")
                    print("O100 sub")
                    print("  G49")
                    print("  G54")
                    print("  #<probe_height> =", radius+19.32)
                    print("  G0 Z40")
                    print("  (MSG,Insert Z Probe, then press S)")
                    print("  M0")
                    print("  G38.2 Z-30 F140")
                    print("  G10 L10 P#1 Z[#<probe_height>]")
                    print("  G0 Z40")
                    print("  G43")
                    print("  (MSG,Remove Z Probe, then press S)")
                    print("  M0")
                    print("O100 endsub")
                    print("(MSG, Hai fatto il 'Centra Asta'? Se hai gia fatto il 'Centra Asta', premi S per continuare. Altrimenti premi ESC per uscire dal programma e premi il pulsante 'Centra Asta' a destra. Quindi esegui dinuovo il programma premendo R.)")
                    print("M0")
                    print("G28.1")
                    print("M102")
                    if radius>0:
                       print("M106")
         
                 match = re.match("(.*)G96(.*)", line)
                 if (match and is_on):
                     speed = 20000
                     secs  = speed/1200
                     print('S' + str(speed) + ' M3')
                     print("G4 P%d" % secs)
                     is_on = False
         	  
                 match = re.match("M5(.*)", line)
                 if match:
                     is_on= True
         
                 match = re.match("M100", line) 
                 if match:
                     if radius>0:
                        print("M107")

if __name__ == '__main__':
    main()

# vim:sw=4:sts=4:et:
