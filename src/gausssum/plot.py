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

# This class takes a string containing commands to Gnuplot
# and creates a window showing the Gnuplot

# Changing from gifs to pngs

import os
import time
import shutil
import tkinter.filedialog
import tkinter.messagebox     # For the Error Dialog
from tempfile import mkstemp

from tkinter import *
from PIL import Image # Python Imaging Library
from PIL import ImageTk      # Python Imaging Library
from .gnupy import Gnuplot

# Kludge necessary for using PIL when using py2exe
# (see http://www.py2exe.org/index.cgi/PIL_and_py2exe)
from PIL import PngImagePlugin # Python Imaging Library
Image._initialized = 2

class DisplayPlot(object):
    def __init__(self,root,g,title):

        self.filedes,self.filename=mkstemp() # filedes is the "file descriptor"

        status = g.plot(self.filename)
        if status==1: # i.e. gnuplot executable not present
            messagebox.showerror(
                title = "Check the path to Gnuplot in Settings",
                message = "No plot was created as the Gnuplot executable cannot be found.\n"
                          "Go to 'File'/'Settings' and set the correct path."
                )
            return

        self.popup=Toplevel(root)
        self.popup.focus_set()

        self.popup.title(title)
        self.title=title # do this better

        self.popup.resizable(False,False)
        self.frame1=Frame(self.popup)
        self.frame1.grid()
        # To create the examples use the following instead:
        # self.canvas2 = Canvas(self.frame1,width=490,height=370,background="blue")
        self.canvas2 = Canvas(self.frame1,width=650,height=490,background="blue")
        self.canvas2.pack(side=TOP)
          
        frame2=Frame(self.frame1)
        frame2.pack(side=TOP)

        try:
            image = Image.open(self.filename)
            self.graph = ImageTk.PhotoImage(image)

            self.item2 = self.canvas2.create_image(7,7,anchor=NW,image=self.graph)
            Label(self.frame1,text="").pack(side=TOP)

        except IOError:
            # This happens anytime that gnuplot doesn't create a graph
            # (for some reason...e.g. bad input)
            messagebox.showerror(title="The script is complaining...",
                                   message="No graph has been created. This may be due \
to a problem with your gnuplot installation or with your \
input file. Contact the author if you think GaussSum is the problem.")
            self.close()
            return
        else:
            # Only put the save button there if there's something to save
            Button(frame2,text="Save As",underline=0,command=self.save).pack(side=LEFT)
            self.popup.bind("<Alt-s>",self.save)

        Button(frame2,text="Close",underline=0,command=self.close).pack(side=LEFT)

        frame3=Frame(self.frame1)
        frame3.pack(side=TOP)
        Label(self.frame1,text="").pack(side=TOP)
    
        self.popup.bind("<Return>",self.close)
        self.popup.bind("<Escape>",self.close)

        self.popup.bind("<Alt-c>",self.close)

        self.popup.protocol("WM_DELETE_WINDOW", self.close)

    def close(self,event=None):
        os.close(self.filedes)
        os.remove(self.filename)
        self.popup.destroy()

    def save(self,event=None):
        filename = filedialog.asksaveasfilename(filetypes=[("PeNGuin",".png")],
                                                parent=self.popup,
                                                defaultextension=".png"
                                                )
        if filename!="":
            if filename.find(".")==-1:
                filename=filename+".png"
            shutil.copyfile(self.filename,filename)
            
            self.popup.title(self.title+" - "+filename)

 


if __name__=="__main__":

    line='plot sin(x)\n'
    root=Tk()
  
    app=Gnuplot(root,line,"Test plot")
    mainloop()
    
