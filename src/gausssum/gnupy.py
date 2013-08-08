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

"""gnupy.py
"""

# For Gnuplot
import os, sys
from tempfile import mkstemp

# For DisplayImage
from tkinter import *


class Gnuplot(object):
    """Simple interface to Gnuplot that uses os.system.

    >>> g = Gnuplot()
    >>> g.data( [(1,1),(2,2),(3,0)],"notitle with lines" )
    >>> g.data( [(1,0.5),(2,1.9),(3,1)],"title 'Hey' with linespoints" )
    >>> g.function( 'sin(x)', "title 'sin(x)' with lines" )
    >>> g.function3d( 'sin(x+y)', "notitle")
    >>> g.commands("set title 'Testing'")
    >>> g.plot("tmp.png")
    """
    def __init__(self,gnuplotexec=None):
        """Initialise the Gnuplot object.

        Parameters:
          filename -- a filename is required
          gnuplotexec -- the location of the gnuplot executable (optional)
        """
        if not gnuplotexec:
            if sys.platform=='win32':
                gnuplotexec = "pgnuplot.exe"
            else:
                gnuplotexec = "gnuplot"
        self.gnuplotexec = gnuplotexec
        self.filedata = []
        self.plotcommand = []
        self.splotcommand = []
        self.settings = []

    def commands(self,*listofcommands):
        """Add a list of commands for the plot."""
        self.settings.extend(listofcommands)

    def data(self, mtuples, style):
        """Save the data to a temporary file."""
        filedes, filename = mkstemp() # filedes is the "file descriptor"

        self.filedata.append( (filedes,filename) )

        output = open(filename,"w")
        for mtuple in mtuples:
            line = map(str, mtuple)
            output.write("\t".join(line)+"\n")
        output.close()

        self.plotcommand.append( '"%s" %s' % (self._fixname(filename),style))

    def function(self,function,style):
        """Remember function information."""
        self.plotcommand.append( '%s %s' % (function,style) )

    def function3d(self,function,style):
        """Remember splot function information."""
        self.splotcommand.append( '%s %s' % (function,style) )

    def plot(self,filename):
        """Plot the graph."""
        self.settings.extend(["set terminal png small",
                              'set output "%s"' % self._fixname(filename)])
	# To create the examples uncomment the following:
	# self.settings.extend(['set size 0.75,0.75'])
                              
        filedes, filename = mkstemp()

        output = open(filename,"w")
        output.write("\n".join(self.settings))
        output.write("\n")
        if self.plotcommand:
            output.write('plot %s \n' % ",".join(self.plotcommand))
        elif self.splotcommand:
            output.write('splot %s \n' % ",".join(self.splotcommand))
        output.close()
        
        # Double quotation marks needed here, esp. for Windows where there
        # may be spaces in the path to gnuplotexec
        status = 0
        if os.path.isfile(self.gnuplotexec):
            os.system('"%s" %s' % (self.gnuplotexec,filename))
        else:
            status = 1

        os.close(filedes)
        os.remove(filename)

        return status

    def __del__(self):
        """Remove temporary files."""
        for mtuple in self.filedata:
            os.close(mtuple[0]) # Close the file descriptor
            os.remove(mtuple[1]) # Remove the temporary file

    def _fixname(self,filename):
        """Replace " and \ by their escaped equivalents."""
        # Taken from gnuplot-py (Michael Haggerty)
        for c in ['\\', '\"']:
            filename = filename.replace(c, '\\' + c)

        return filename


if __name__=="__main__":
    import doctest,gnupy
    doctest.testmod(gnupy)
