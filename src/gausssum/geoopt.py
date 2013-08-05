#
# GaussSum (http://gausssum.sf.net)
# Copyright (C) 2006-2009 Noel O'Boyle <baoilleach@gmail.com>
#
# This program is free software; you can redistribute and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

import os
import sys
import math

from Tkinter import *
from plot import DisplayPlot
from gnupy import Gnuplot
from tempfile import mkstemp

def GeoOpt(root,screen,logfile,numpts,gnuplotexec):

    screen.write("Starting GeoOpt.py\n")

    deviation = []
    for i in range(len(logfile.geovalues)):
        dev = 0
        for j in range(len(logfile.geotargets)):
            if abs(logfile.geovalues[i][j])>logfile.geotargets[j]:
                dev += math.log(abs(logfile.geovalues[i][j])/logfile.geotargets[j])
        deviation.append(dev)


    if len(logfile.scfenergies)>=numpts+2: # If there are two points to plot
        
        g = Gnuplot(gnuplotexec)
        g.commands("set xlabel 'Optimisation Step'")
        g.commands("set ylabel 'Energy'")
        data = zip(range(len(logfile.scfenergies)-numpts),logfile.scfenergies[numpts:])
        g.data(data,"notitle with lines")
        g.data(data,"notitle")

        DisplayPlot(root,g,"Geometry optimisation")

        if len(deviation)>=numpts+2:

            h = Gnuplot(gnuplotexec)
            h.commands("set yrange [0:]")
            h.commands("set xlabel 'Optimisation Step'")
            h.commands("set ylabel 'Deviation from targets'")
            data = zip(range(len(deviation)-numpts),deviation[numpts:])
            h.data(data,"notitle with lines")
            h.data(data,"notitle")

            DisplayPlot(root,h,"Deviation from targets")
            
    else:
        screen.write("I need at least two points to plot\n")

    screen.write("Finishing GeoOpt.py\n")
